# Wingfoil

A small wingfoiling simulator in the browser: live at https://wing.corentinbel.com

Single `index.html`, Three.js from a CDN, everything procedural (no downloaded assets): Gerstner-wave ocean with wind chop, sky, board + foil, inflatable wing or parawing, rider (capsule rig + 2-bone IK), spray, wake, wind streaks.

## 3D wing model
The inflatable wing is a real 3D asset: `models/wing-casamoderna.glb`, built from **“Wing Foil surf 4m”** (https://sketchfab.com/3d-models/wing-foil-surf-4m-de7220b1b4ec4337b325cd02d5742b11) by **casamoderna** (https://sketchfab.com/casamoderna), licensed **CC BY 4.0** (http://creativecommons.org/licenses/by/4.0/).
Modified: re-oriented to the game's axes, split into canopy / leading-edge tube / handles, UVs added for the paint scheme, leading edge bent into a deeper arch (0.75 m at the tips); a strut tube is added in the game. Credit shown on the page and stored in the GLB.
Rebuild (numpy + scipy): `python tools/wing2glb.py <scene.gltf from Sketchfab> models/wing-casamoderna.glb tools 0.75`. `?procedural` uses the old procedural wing; the parawing stays procedural.

## Controls
Simple (default): A/D steer · W/S more / less power · Space pump (keep a rhythm) · J jump · Q wing ⇄ parawing · G mode · L light · C camera · P autopilot · Tab pro controls.
Pro: W/S front/back foot · ↑/↓ or wheel wing power · Space leg pump · E wing pump (together = combo) · T foot assist · M wind map.
Toolbar (top): mode (Free ride / Slalom race / Downwinder), time of day (Day / Golden hour / Sunset / Night), 🎨 colours, 📷 photo mode (O; drag orbit, wheel zoom, Enter/Save PNG), 🔊 sound (N), ⏺ record .webm (R).
Touch: autopilot first; tap to take over, hold left/right edge to steer, tap the middle to pump, swipe up to jump, two fingers = autopilot.

URL flags: `?inspect=wing|para&ang=deg&elev=deg`, `&dolphins=N`, `&mode=slalom|downwind`, `&tod=0..3`, `&jumpAt=T`, `&photo`, `&colors`, `?auto`, `&cam=0|1|2`, `&gear=para`, `&pro`, `&warm=30`, `&log`, `?test=breach`.

## What's in it
- Physics (toy): wind field with gust patches (same formula in JS and the water shader), wing/parawing lift with stall, foil lift from board pitch, ventilation near the surface, breach / nose-dive / hard-landing crashes, swell you can ride, rhythm-limited pumping, jumps (bigger off a swell face, wing gives hang time).
- AI riders: Marin, Lou (parawing) and Sam run the same physics; they reach near you, race the slalom in their own lanes and jump now and then.
- Slalom: 8 gates across the wind, timer from gate 1, best time + ghost of your best run (browser storage).
- Downwinder: bigger swell and wind; scores distance downwind and the longest glide without pumping.
- Sound: synthesised with WebAudio (wind, foil hiss, hull slosh, gulls, splashes, gate beeps); starts after the first key / tap.
- Wildlife: gull flock + gulls on buoys, dolphin pods every ~35–80 s.

Run locally: `python3 -m http.server 8765` in this folder, open http://localhost:8765.
