# Wingfoil sim (v1)

Single-file Three.js wingfoil sim. Everything is procedural (no downloaded assets): Gerstner-wave ocean shader, sky, board + foil, inflatable wing, rider (capsule rig + 2-bone IK), spray, wake.

Run: `cd ~/git/games/wingfoil && python3 -m http.server 8765` then open http://localhost:8765 (needs internet for the three.js CDN).

Controls: A/D steer · W/S front/back foot pressure · ↑/↓ or mouse wheel sheet in/out (analog) · Space leg pump · E wing pump (together within 0.25 s = combo ×1.5) · T foot assist on/off · C camera · M wind map · P autopilot · R record .webm · mouse drag orbit.
URL flags: `?auto` autopilot, `&cam=1` camera mode, `&warm=30` pre-simulate 30 s, `&log` state log to console, `?test=breach` back foot without assist (must breach and crash).

Physics (toy, v2):
- Wind field: 15 kn base, gust patches drifting downwind + a stronger zone (same formula in JS and in the water shader → gusts = dark rough patches, whitecaps only in strong wind, streaks in the air, wind map).
- Wing: sheet sets angle of attack (-4..28°), lift curve stalls above ~17°; drive depends on apparent wind angle (no-go < 28°). Wing pose comes from the apparent wind + angle of attack; canopy billows with load and flaps when luffing.
- Foil: board pitch from feet (+ optional assist) → foil lift = ½ρv²S·CL(pitch); lift fades as the front wing nears the surface. Breach = front wing above the local water surface → crash. Hard touchdown (vy < -1.4 m/s) → nose-dive crash.
- Waves: a 70 m downwind swell + chop; gravity along the local slope speeds you up down a swell face.
- Pumping: leg pump (thrust + unweighting + board pitch stroke), wing pump (thrust + wing pulled in); rhythm-limited, stamina cost.
