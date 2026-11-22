"""Load the Sketchfab glTF wing, weld vertices, split into connected components, report them."""
import json, sys, struct, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

def load(path):
    g = json.load(open(path)); base = path.rsplit('/', 1)[0]
    binb = open(f"{base}/{g['buffers'][0]['uri']}", 'rb').read()
    def acc(i):
        a = g['accessors'][i]; bv = g['bufferViews'][a['bufferView']]
        off = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        n = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[a['type']]
        dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}[a['componentType']]
        stride = bv.get('byteStride', 0)
        if stride and stride != n * np.dtype(dt).itemsize:
            raw = np.frombuffer(binb, np.uint8, count=stride * a['count'], offset=off).reshape(a['count'], stride)
            return raw[:, :n * np.dtype(dt).itemsize].copy().view(dt).reshape(a['count'], n)
        return np.frombuffer(binb, dt, count=a['count'] * n, offset=off).reshape(a['count'], n) if n > 1 else np.frombuffer(binb, dt, count=a['count'], offset=off)
    prim = g['meshes'][0]['primitives'][0]
    pos = acc(prim['attributes']['POSITION']).astype(np.float64)
    idx = acc(prim['indices']).astype(np.int64).reshape(-1, 3) if 'indices' in prim else np.arange(len(pos)).reshape(-1, 3)
    return pos, idx

def weld(pos, idx, eps=1e-4):
    key = np.round(pos / eps).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    newpos = np.zeros((inv.max() + 1, 3)); newpos[inv] = pos
    return newpos, inv.reshape(-1)[idx]

def components(npos, tri):
    n = len(npos)
    e = np.concatenate([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]])
    A = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n))
    nc, lab = connected_components(A, directed=False)
    return nc, lab

if __name__ == '__main__':
    pos, idx = load(sys.argv[1])
    npos, tri = weld(pos, idx)
    nc, lab = components(npos, tri)
    tl = lab[tri[:, 0]]
    print(f'verts {len(pos)} -> welded {len(npos)}, tris {len(tri)}, components {nc}')
    sizes = np.bincount(tl, minlength=nc)
    for c in np.argsort(-sizes)[:40]:
        v = npos[np.unique(tri[tl == c])]
        print(c, sizes[c], 'min', v.min(0).round(2), 'max', v.max(0).round(2), 'ext', (v.max(0) - v.min(0)).round(2))
