# Wingfoil

A small wingfoiling simulator in the browser: live at https://wing.corentinbel.com

Single `index.html`, Three.js from a CDN, everything procedural (no downloaded assets): Gerstner-wave ocean with wind chop, sky, board + foil, inflatable wing or parawing, rider (capsule rig + 2-bone IK), spray, wake, wind streaks.

## Controls
Simple (default): A/D steer · W more power · S less power · Space pump (keep a rhythm) · Q wing ⇄ parawing · C camera · P autopilot · R record .webm · Tab pro controls.
Pro: W/S front/back foot · ↑/↓ or wheel wing power · Space leg pump · E wing pump (together = combo) · T foot assist · M wind map.
Touch: autopilot first; tap to take over, hold left/right edge to steer, tap the middle to pump, two fingers = autopilot.

URL flags: `?inspect=wing|para&ang=deg&elev=deg` (gear alone, for modelling), `&dolphins=N` (first pod after N s), `?auto`, `&cam=0|1|2`, `&gear=para`, `&pro`, `&warm=30` (pre-simulate 30 s), `&log` (state log in the console), `?test=breach` (back foot, no assist: must breach and crash).

## Physics (toy)
- Wind field: 15 kn base, gust patches drifting downwind + a stronger zone, same formula in JS and in the water shader (gusts = dark rough patches, whitecaps only in strong wind).
- Wing / parawing: sheet sets the angle of attack, lift stalls past ~16° / 14°; drive depends on apparent wind angle (no-go < 28°). Pose follows the apparent wind; gear kept ≥ 40 cm above the hull and 30 cm above the water.
- Foil: board pitch from feet (+ assist) → lift = ½ρv²S·CL; lift fades near the surface. Breach (front wing above the local water) and hard touchdown are crashes.
- Waves: 70 m downwind swell + chop; gravity along the slope speeds you up down a swell face.
- Wildlife: a gull flock follows the rider (two more sit on buoys); a pod of 2-4 dolphins surfaces every ~35-80 s and porpoises alongside.
- Pumping: leg pump (thrust + unweighting) and wing pump (weaker with the parawing); rhythm-limited, stamina cost.

Run locally: `python3 -m http.server 8765` in this folder, open http://localhost:8765.
