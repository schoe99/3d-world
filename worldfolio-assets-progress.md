# Worldfolio Asset Replacement — Progress

**Goal:** Replace the three.js-made assets in `replace_assets/` (moved into this repo 2026-07-13) with improved Blender rebuilds.
Each asset folder gets: `original.png` (old screenshot) + `final.png` (new render) + `model.glb` (exportable for three.js).

**Workflow rule (per Sam):** build one asset → get approval → only then move to the next. Diagnose what's wrong out loud *before* making changes, and actually look at renders/references rather than iterating blind.

## Pipeline / tooling

- Blender driven via MCP (`execute_blender_code`), all helpers installed in-session as the `wf` Python module (persists in `sys.modules['wf']` while Blender stays open — **re-run the helper install script if Blender restarts**).
- `wf` provides: `clear, mat, assign, sphere, cyl, cone, cube, torus, jitter, blob, join, setup, frame(d=view dir), render, export`.
- Render setup: EEVEE, transparent background, 1024×1024, Standard view transform, key sun 1.9 + fill 0.55 + weak ambient.
- Palm-island demo scene from earlier session saved at scratchpad `ac-island-demo.blend`.
- Inspection renders (front/side views) go to scratchpad, not the asset folders.

## Asset status

| Asset | Status | Notes |
|---|---|---|
| worldfolio-boat | ✅ **approved** | Round hull, rim, deck, bench, curved billowing sail (solidified for three.js), pennant. |
| worldfolio-character | ✅ **finished & installed** | Bear finished by Sam in Blender (2026-07-13), installed into the `character` slot via `set-asset.py`. Static — no rig/animation clips yet. |
| worldfolio-island-home | 🔶 built, awaiting verdict | Clover grass blobs + sand base, stacked-sphere apple tree, tufts, flowers. Built before verify-first rule; user has not yet approved/rejected. |
| worldfolio-island-contact | ⏸ not started (task in progress) | Lighthouse island. Blocked on bear approval. |
| worldfolio-island-crypto | ⏸ not started | Desert island, 2 palms. Reuse palm builder from demo. |
| worldfolio-island-signal | ⏸ not started | Mountain + snow cap island. |
| worldfolio-island-skills | ⏸ not started | Snowy island, frosted trees. |
| worldfolio-npc-bloop | ⏸ not started | Whale NPC. |
| worldfolio-npc-gully | ⏸ not started | Seagull on buoy NPC. |
| worldfolio-npc-iggy | ⏸ not started | Penguin on ice floes NPC. |
| worldfolio-npc-kappy | ⏸ not started | Turtle NPC. |

## Bear character — iteration history (v1→v30)

Current design: brown fur bear, cream muzzle/belly/inner-ears, black oval eyes (no highlights), pink blush,
smile arc, **coral scarf** (slim torus + knot + flat teardrop ribbon), **squat honey pot sitting on top of head**
with drip down the pot side, cream **slipper-oval feet** (ACNH cub style), thin short legs, stubby tapered
mitten arms, flat painted-style belly oval (smooth ellipsoid barely proud of chest), tail nub.

Key user feedback applied along the way:
- No shirt (tried teal tee + sleeves — removed), no sprout, no crossbody satchel (strap rendered as floating hoop).
- No eye highlights; black ovals only.
- Honey pot: was held in hand → now sits ON TOP of the head (base resting on crown, not sunk).
- Belly: one smooth oval (not snowman, not diaper, not pixel-edged, not bulging) — solved via ellipsoid that
  tracks torso curvature ~0.02 proud; torso taper must be a smooth quadratic (kinks pinch the boundary).
- Anatomy: AC cub reference (Nookipedia Maple) — huge head, compact pear torso, stubby arms,
  tiny thin legs + distinct cream slipper feet; legs must be socketed into the hip (no gaps).
- Legs went through: too long → too chunky ("horrible") → match arm ratio → shorter → skinnier → v30 reference-based.

**Where we are RIGHT NOW:** user says v30 "looks nothing like" an AC cub. I was in the middle of downloading an
actual Maple render to visually compare (Nookipedia and Fandom both bot-block plain curl; Fandom page came back
5.7KB stub — next options: `static.wikia.nocookie.net` direct image URL patterns, the animalcrossingworld.com
render pack, or ask Sam to drop a reference image into a folder). **Next step: obtain a real reference image,
Read it visually, list concrete differences vs our model, get approval on the diff list, then rebuild.**

## Reference links (AC cubs)

- https://nookipedia.com/wiki/Maple (official NH render)
- https://animalcrossing.fandom.com/wiki/Maple
- https://animalcrossingworld.com/2020/02/250-high-resolution-animal-crossing-new-horizons-villager-special-character-renders/
- https://game8.co/games/Animal-Crossing-New-Horizons/archives/284154 (all cub villagers)

## File locations

- Assets: `/Users/wang/Downloads/replace_assets/<asset-name>/{original.png, final.png, model.glb}`
- Scratchpad (inspection renders, saved demo .blend): `/private/tmp/claude-501/-Users-wang-Desktop-code/85014079-533f-4ef8-9adb-2ad74aab19db/scratchpad/`
- Bear build script: fully regenerated each version inside the Blender MCP calls (deterministic; latest = v30).
