# Custom Assets — Sam's World-folio

Every visual in the world is a **slot** you can override with your own
`.glb` model. Interactions (dialogue, quests, teleport, walking, bobbing)
live in the code and keep working no matter what the model looks like.

## Quick start

```bash
# see all slots and what's installed
python3 set-asset.py --list

# install a custom model (copies the file into assets/ and registers it)
python3 set-asset.py island-home ~/Blender/exports/my-home-isle.glb
# or use the per-asset shortcut:
./scripts/set-home-isle.sh ~/Blender/exports/my-home-isle.glb

# go back to the built-in model
python3 set-asset.py --remove island-home
```

Then refresh the browser (**Cmd+R**). If a file fails to load, the game
logs a warning in the console and falls back to the built-in model.

## Export settings (Blender)

- Export as **glTF Binary (.glb)** — single file, textures embedded.
- **+Y up** (Blender's glTF exporter does this by default).
- **Apply transforms** before export (Ctrl+A → All Transforms).
- Real scale: 1 Blender unit = 1 world unit. The character is ~2.2 tall.

## Slot conventions

| Slot | Shortcut script | Origin should be at | Faces | Rough size |
|---|---|---|---|---|
| `island-home` | `set-home-isle.sh` | island center, **sea level** | any | 8–11 across, land top ~0.7 up |
| `island-signal` | `set-signal-peaks.sh` | 〃 | any | 〃 (its mountains can be taller) |
| `island-crypto` | `set-crypto-cove.sh` | 〃 | any | 〃 |
| `island-skills` | `set-toolbox-tundra.sh` | 〃 | any | 〃 |
| `island-contact` | `set-hello-harbor.sh` | 〃 | any | 〃 |
| `npc-kappy` | `set-kappy-turtle.sh` | waterline under the model | **+Z** | ~1.3 long |
| `npc-gully` | `set-gully-seagull.sh` | waterline (include the perch!) | **+Z** | ~2.2 tall |
| `npc-bloop` | `set-bloop-whale.sh` | waterline | **+Z** | ~3 long |
| `npc-iggy` | `set-iggy-penguin.sh` | waterline (include the floes!) | **+Z** | floe ~3.5 across |
| `prop-tree` | — | ground under trunk | any | 1.5–2.5 tall |
| `prop-palm` | — | ground under trunk | any | ~2 tall |
| `prop-snowtree` | — | ground under trunk | any | 1.5–2.5 tall |
| `prop-mountain` | — | ground under base | any | ~3 tall, base ~2.5 wide |
| `prop-lighthouse` | — | ground under base | any | ~3 tall |
| `boat` | `set-boat.sh` | waterline | +Z | ~2.5 long |
| `character` | `set-character.sh` | **under the feet** | **+Z** | ~2.2 tall |

Notes:

- **Islands**: your model replaces the terrain *and* all props on it, so
  include your own trees/decorations in the file. Every mesh in it becomes
  walkable — the character stands on whatever topology you build. The
  floating name label, dialogue trigger, and passport teleport stay.
- **NPCs**: the model bobs on the waves automatically. Meshes are walkable
  (needed for Iggy's floes). Voice, dialogue, and the FRIENDS stamp remain.
- **Props**: one model replaces *every placed instance* of that type at its
  existing spot and rotation. Author at final size — placement doesn't
  rescale. If the built-in prop was climbable (mountain), yours will be too.
- **Character**: walk bob, turning, hop and the intro wave-turn still run,
  but the built-in arm-wave animation only exists on the built-in body.
  The ground shadow and the 100%-quest crown are kept and re-attached.

## Animations (optional)

Animations baked into a `.glb` play automatically. Name your Blender
Actions with these (case-insensitive) names and push each one down to an
NLA track before exporting:

| Clip name | Who | When it plays |
|---|---|---|
| `idle` | any slot | loops whenever nothing else is playing (NPCs/boat/islands: loops always) |
| `walk` | character | crossfades in while moving |
| `wave` | character | during the intro hello (and whenever the character faces the screen) |

Rules:

- A model with **no** clips keeps working exactly as before — fully static
  models stay valid. Missing clips fall back silently (no `walk`? the
  container walk-bob still applies).
- If a non-character model has exactly **one** clip, it's treated as
  `idle` regardless of its name.
- Container motion (wave-bobbing, walk-bob, hop, turning) composes with
  clips — don't re-animate whole-body bobbing, only part-level movement
  (arms, head, tail, flags).
- Props (`prop-*`) don't support clips — they're cloned per placed
  instance.
- Export with **Animation** enabled in the glTF exporter; check the
  console log line `[assets] custom character ← … (clips: …)` to confirm
  the clips made it into the file.

## How it works

`assets/manifest.json` maps slots → files (written by `set-asset.py`;
don't edit by hand unless you want to). On page load the game fetches the
manifest, loads each `.glb` with GLTFLoader, and swaps it into the scene —
removing the procedural version from rendering *and* from the walkable-
terrain raycaster, then registering your meshes instead. File URLs carry a
`?v=` timestamp so browser caching never shows you a stale model.
