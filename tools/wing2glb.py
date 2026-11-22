"""Convert the Sketchfab wing into a game asset: our axes, parts split (canopy / tube / handles), UVs, optional arch bend.
Our frame: X span (strut at 0), Y rider side (handles), Z toward the leading edge (LE at 0, chord toward -Z)."""
import json, struct, sys, numpy as np
sys.path.insert(0, sys.argv[3]); from wingparts import load, weld, components
src, out, _, bend = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
pos, idx = load(src); P, T = weld(pos, idx); nc, lab = components(P, T)
tl = lab[T[:, 0]]; big = np.bincount(tl).argmax()
XC, YLE = -0.115, P[:, 1].max()
Q = np.stack([P[:, 0] - XC, -P[:, 2], P[:, 1] - YLE], 1)          # model (x, y, z) -> ours (x, -z, y - yLE)
half = np.abs(Q[:, 0]).max()
Q[:, 1] += bend * (Q[:, 0] / half) ** 2                              # arch: tips curl toward the rider
# leading/trailing edge per span bin (big part only) -> tube band + chord fraction
bv = Q[lab == big]
bins = np.linspace(-half, half, 41); cen = (bins[:-1] + bins[1:]) / 2
zf = np.array([bv[(bv[:, 0] >= a) & (bv[:, 0] <= b), 2].max() if ((bv[:, 0] >= a) & (bv[:, 0] <= b)).any() else np.nan for a, b in zip(bins[:-1], bins[1:])])
zb = np.array([bv[(bv[:, 0] >= a) & (bv[:, 0] <= b), 2].min() if ((bv[:, 0] >= a) & (bv[:, 0] <= b)).any() else np.nan for a, b in zip(bins[:-1], bins[1:])])
ok = ~np.isnan(zf); front = np.interp(Q[:, 0], cen[ok], zf[ok]); back = np.interp(Q[:, 0], cen[ok], zb[ok])
s = np.abs(Q[:, 0]) / half
tubeDepth = 0.30 * (1 - 0.45 * s ** 1.5)
fromLE = front - Q[:, 2]
isTube = fromLE < tubeDepth
u = (Q[:, 0] + half) / (2 * half); v = 1 - np.clip(fromLE / np.maximum(front - back, 0.05), 0, 1)
part = np.where(lab == big, np.where(isTube, 1, 0), 2)                # 0 canopy, 1 tube, 2 handles
tpart = np.array([np.bincount(part[t], minlength=3).argmax() for t in T])
def normals(V, F):
    n = np.zeros_like(V); fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    for k in range(3): np.add.at(n, F[:, k], fn)
    return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
# one primitive per part, own vertex arrays (a vertex on a part boundary is duplicated)
bin_, views, accs, prims = bytearray(), [], [], []
def add(arr, target=None, minmax=False):
    off = len(bin_); b = arr.tobytes(); bin_.extend(b); bin_.extend(b'\0' * (-len(bin_) % 4))
    views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(b), **({'target': target} if target else {})})
    a = {'bufferView': len(views) - 1, 'count': len(arr), 'componentType': 5125 if arr.dtype == np.uint32 else 5126,
         'type': {1: 'SCALAR', 2: 'VEC2', 3: 'VEC3'}[1 if arr.ndim == 1 else arr.shape[1]]}
    if minmax: a['min'] = arr.min(0).tolist(); a['max'] = arr.max(0).tolist()
    accs.append(a); return len(accs) - 1
for k, name in enumerate(['canopy', 'tube', 'handles']):
    F = T[tpart == k]; used, Fi = np.unique(F, return_inverse=True); Fi = Fi.reshape(-1, 3)
    V = Q[used].astype(np.float32); N = normals(V.astype(np.float64), Fi).astype(np.float32)
    UV = np.stack([u[used], v[used]], 1).astype(np.float32)
    prims.append({'attributes': {'POSITION': add(V, 34962, True), 'NORMAL': add(N, 34962), 'TEXCOORD_0': add(UV, 34962)},
                  'indices': add(Fi.astype(np.uint32).reshape(-1), 34963), 'material': k})
    print(name, 'tris', len(F), 'verts', len(V), 'ext', (V.max(0) - V.min(0)).round(2))
# handle centres (for the hands), sorted front to back
hc = sorted([Q[lab == c].mean(0).round(3).tolist() for c in range(nc) if c != big], key=lambda p: -p[2])
credit = ('This work is based on "Wing Foil surf 4m" (https://sketchfab.com/3d-models/wing-foil-surf-4m-de7220b1b4ec4337b325cd02d5742b11) '
          'by casamoderna (https://sketchfab.com/casamoderna) licensed under CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/). '
          'Modified: re-oriented, split into parts, UVs added, arch bent.')
gl = {'asset': {'version': '2.0', 'generator': 'wing2glb.py', 'copyright': credit},
      'scene': 0, 'scenes': [{'nodes': [0]}], 'nodes': [{'name': 'wing', 'mesh': 0, 'extras': {'handles': hc, 'half': float(half)}}],
      'meshes': [{'name': 'wing', 'primitives': prims}],
      'materials': [{'name': n} for n in ['canopy', 'tube', 'handles']],
      'buffers': [{'byteLength': len(bin_)}], 'bufferViews': views, 'accessors': accs}
js = json.dumps(gl).encode(); js += b' ' * (-len(js) % 4)
with open(out, 'wb') as f:
    f.write(struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(bin_)))
    f.write(struct.pack('<II', len(js), 0x4E4F534A)); f.write(js)
    f.write(struct.pack('<II', len(bin_), 0x004E4942)); f.write(bin_)
print('handles (x, y, z):', hc); print('wrote', out, 12 + 16 + len(js) + len(bin_), 'bytes')
