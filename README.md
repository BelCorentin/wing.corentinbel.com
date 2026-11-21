# Wingfoil sim (v1)

Single-file Three.js wingfoil sim. Everything is procedural (no downloaded assets): Gerstner-wave ocean shader, sky, board + foil, inflatable wing, rider (capsule rig + 2-bone IK), spray, wake.

Run: `cd ~/git/games/wingfoil && python3 -m http.server 8765` then open http://localhost:8765 (needs internet for the three.js CDN).

Controls: A/D steer · W power · S depower · Space pump · C camera (chase/cinematic/drone) · P autopilot · R record .webm · mouse drag orbit.
URL flags: `?auto` autopilot, `&cam=1` camera mode, `&warm=30` pre-simulate 30 s (for screenshots).

Physics (toy): gusty 14-19 kn wind from +Z; apparent wind drives a drive coefficient vs apparent wind angle (no-go < 28°); displacement drag vs foiling drag; takeoff above 5 m/s; foil height rises with speed and breaches (crash) above 88 cm → depower in gusts.

Headless screenshot:
`~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome --headless=new --use-angle=swiftshader --enable-unsafe-swiftshader --window-size=1280,720 --virtual-time-budget=15000 --screenshot=out.png "http://localhost:8765/index.html?auto&warm=30"`
