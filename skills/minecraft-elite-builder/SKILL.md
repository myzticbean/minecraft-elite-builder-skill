---
name: minecraft-elite-builder
description: Design and build a Minecraft structure in code at the level of the best professional build teams, as a Python drawing that exports a Sponge .schem for WorldEdit/FAWE, checked by numbers and by renders Claude reads. Use when asked to build, design, upgrade or review a Minecraft house, workshop, landmark or set piece as a schematic, from reference images or from Claude's own design, at a basic or legendary tier.
---

# Minecraft elite builder

Claude can't see the game. So a building is a **Python script** that places every block by
coordinates in the building's own frame, then tools turn it into blocks, check it by numbers, draw
it as PNGs that Claude looks at, and write the `.schem` the user pastes with WorldEdit or FAWE. The
loop is: **draw → resolve → connect → check → render → look → fix**, several times, before anything
goes in game.

The toolkit is in this skill's `scripts/` folder (Python 3.9+ and numpy). The worked example is
`examples/forge_legendary.py`: a water-powered hammer mill of three generations, 62 by 51 by 28,
about 16,100 blocks, about 1,050 lines, all checks clean.

## Setup, once per project

If the project has no copy of the toolkit yet, make one:

1. Copy `scripts/draw.py`, `look.py`, `schem.py` and `review.py` into a build folder in the project
   (for example `builds/`). Build scripts live beside them, and the project owns its copy from then
   on.
2. Check that numpy imports: `python -c "import numpy"`. Use plain `python`, not `-I`, if numpy is in
   the user's site packages.
3. If the server isn't on Minecraft 26.2, set `DATA_VERSION` in `schem.py` to the server's data
   version.

## Before any code

1. **Art direction is the user's.** Ask which it is:
   - **reference images**: then the breakdown is measured from them (every view, counted from a
     known small block);
   - **"your own design"**: then no reference is traced; name two or three inspirations (real
     buildings and famous RPGs) and copy none of them 1:1.

   Also ask the tier (trial or legendary), the trade or purpose, and the site (which way the slope
   runs, how much room). Don't invent the look unasked.
2. **Read the project's own rules** (CLAUDE.md or similar). They win over this skill.
3. **Read** `references/method.md` (how an expert thinks) and skim `references/pitfalls.md` (every
   trap already paid for). Keep `references/vocabulary.md` (block recipes and facings) and
   `references/toolkit.md` (the API) open while drawing.
4. **Write the design notes first**, in the script's docstring:
   - the story (who built it, when, how it grew);
   - the inspirations;
   - the parts list of the trade (what the work really needs);
   - the four heads:
     - **footprint and orientation**: where the entrance is, which way it faces, how it meets the
       path, its shape, the dig;
     - **walls**: weighted `%` palettes, how far each frame stands proud, the window style;
     - **roof**: its profile, overhang, trim, dormers, chimneys;
     - **props**.

   Every block afterwards has a reason.

## The loop

| Pass | What | Done when |
|---|---|---|
| 1. Block-out | Volumes only, in plain blocks: every mass, roof envelopes, the tallest landmark, the dig. Render. | From the hero corner the silhouette has a clear order (one landmark, one main mass, lower supports, accents), shapes contrast, no two roofs run into one another. Fix composition **now**: it is the cheapest it will ever be. |
| 2. Structure | Walls in planes, frames, roofs by profile (`d.roof`, `d.spire`), arches (`d.arch`), towers (`octo`), floors at human scale. | `look.check` reaches every floor; renders read as the block-out did. |
| 3. Depth | Three layers on every face: the plane, structure a block proud, projections and recesses. No plane over about 6 long without a change of depth. | Every side is dressed, and each one differently. |
| 4. Texture | Palettes on gradients with a reason: dirty at the foot, soot near fire, moss where water runs, patches rather than salt. | Values contrast between materials (dark roof, pale plaster, mid stone, dark timber). |
| 5. Detail and interior | Micro-blocks that each mean something; the trade's working parts in working order; visible structure inside (trusses, corbels). | Every prop tells a story of work. |
| 6. Ground | The hill, built after the buildings and only into empty cells; the dig, retaining walls, worn paths, water, clutter thinning out, greenery at wall feet. | No cliff at the site's edge; the building grows out of the slope. |
| 7. Light | Lanterns where people walk (every 4 to 6 blocks), fire where the work is, hidden `light` only in dark corners. | No dark pocket a mob could spawn in. |
| 8. Review | All checks clean, then the hero, iso and close views of each volume, a cutaway of each interior, and a cell dump for any doubt. | Nothing left that a top builder would point at. |

A legendary build takes several review passes (the forge took five). A trial takes one or two.

## Running it

```bash
python <build folder>/<build>.py <scratch folder>/<prefix>
```

The script:

- prints the checks;
- writes `<prefix>-hero.png`, `-iso.png`, `-sides.png`, `-top.png` and the close views;
- writes `<build>.schem`.

Write renders to a scratch folder, never into the project. Read the PNGs with the Read tool and
judge them. For closer looks, use `review.py` (close, cut, dump; see `references/toolkit.md`).

`look.check` must print zeros and `good`:

- **floating blocks: 0**: everything joins the ground face to face.
- **hung on nothing: 0**: trapdoors, ladders, buttons, signs, banners and lanterns all touch a
  block.
- **flammable by lava: 0**: nothing burnable within 2 sideways or 5 above.
- **every floor reached** from the paste origin.

`look.connect` prints any pane that joins nothing; that is a window in the wrong cell.

## Hard rules

- **Built things belong where they stand**: dug into the slope, stepped with the floor, never on a
  raised platform or a levelled pad.
- **Cheap to run**:
  - no entities (armour stands, item frames, minecarts);
  - count every ticking block in the docstring (campfires, lava, water);
  - no vines (they grow on random ticks).
- **Facings come from helpers, never by hand**: `shutter(on)`, `toward(du, dv)`, `d.arch(ends=)`
  (`references/vocabulary.md`).
- **A schematic pastes with no neighbour updates.**
  - Every pane, fence, wall and stair corner gets its state from `look.connect`.
  - Water is only source blocks in closed, level channels.
  - A lit furnace goes out.
  - Leaves need `persistent=true`.
  - Anvils and gravel need something solid under them.
- **Roofs before what pierces them.** Draw towers, stacks and turrets after the roofs they come
  through, because a roof's surface overwrites.
- **Don't fix what a render misreads.** An isometric view foreshortens; check a doubt with
  `review.py dump` first.
- **The user judges it in game.** Don't commit or ship a build before they have.

## Delivering

1. Send the user the hero render and the iso sheet, plus a close view if one tells the story
   better.
2. Give the paste steps:
   - put `<build>.schem` in the WorldEdit/FAWE `schematics` folder;
   - `//schem load <build>`;
   - stand where the drawing's `GATE` is (a player's feet on the path, in front of the entrance);
   - `//paste`.

   Points to tell the user:
   - The front faces west: face east to see it, or `//rotate` the clipboard first.
   - Empty cells paste as air, so a plain `//paste` clears the box (`-a` keeps what stands there).
   - `//undo` takes it back.
3. Write down what the build taught: add every new trap to `references/pitfalls.md`.
4. If the user tunes it in game, fold their edits back into the script as an `EDITS` list applied
   last. Each edit is a lesson for this skill.

