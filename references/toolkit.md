# The toolkit: scripts/

The tools are plain Python 3.9+ with numpy. Copy them into the project's build folder once (see
`SKILL.md`, Setup); every build is one script beside them that imports them.

| File | What it does |
|---|---|
| `draw.py` | The drawing: cells in the building's own frame, with palettes, boxes, lines, profiled roofs, spires and arches; `shutter`, `toward`, `octo`, `hash01`. |
| `look.py` | Turns a drawing into blocks (`resolve`) and sets the states a paste needs (`connect`). Checks it (`check`) and renders PNGs (`render`, `close`, `iso`, `elevation`). |
| `schem.py` | `write(blocks, path, origin)` writes a Sponge v2 schematic for FAWE (DataVersion 4903, Paper 26.2). `read(path)` loads one back, including ones the user gives us. |
| `review.py` | Closer looks at any build: `close`, `cut` (a cutaway) and `dump` (one plane's cells as letters). |

## The frame

- **u** runs across the front. **+u is the left hand** of a player on the path looking at the
  building, so low u is on the right. Name sides by their u or v in comments, never "left" alone.
- **v** runs back into the hill; the path is at negative v.
- **y 0** is the ground's own layer, so a player standing on it is at y 1. Floors are flush with
  the ground.
- **Facings are written in the file's frame**, where the front faces west:

  | Facing | Direction in the drawing |
  |---|---|
  | west | -v: out of the front, toward the path |
  | east | +v: into the hill |
  | north | +u: the player's left |
  | south | -u: the player's right |

  `look.DIRS` maps a facing to (du, dv): north (1, 0), south (-1, 0), east (0, 1), west (0, -1).
- **Log axes**: `axis=y` is upright; `axis=z` is a beam along u; `axis=x` is a beam along v.
- **The file frame** is x = v and z = -u. The schematic's offset is its minimum corner minus the
  origin.

## draw.Drawing

| Call | Does |
|---|---|
| `d.set(u, y, v, block)` / `d.get` / `d.clear` | One cell. `block` is an id with props (`'oak_stairs[facing=west,half=bottom]'`), a palette reference (`'@stone'`, `'@tiles[facing=north,half=bottom]'`), or `'air'`. An `'air'` cell is written: it cuts the hill. |
| `d.box(u0, y0, v0, u1, y1, v1, block, hollow=False)` | Fills a box. Note the argument order. `block` may be a function `(u, y, v) -> block`, which is how a gradient goes on. |
| `d.line(a, b, block)` | Cells from a to b, each a (u, y, v). It can join cells at an edge only, so a spoke drawn this way floats: step one axis at a time instead. |
| `d.palette(key, '50%stone_bricks,30%andesite,20%tuff')` | A weighted mix, used as `@key`. `look.resolve` picks from it in patches about two blocks across, with some speckle. |
| `d.roof(a0, a1, b0, b1, y, profile, keys, under, along='v', verge=None)` | A gable roof with a profile. It spans a0..a1 (overhang included) and runs b0..b1 along the ridge's axis `along`, with eaves at y. Returns `{a: (surface y, lowest y)}`: **fill each gable up to the surface y**, so the plaster shows under the barge board. |
| `d.spire(cu, cv, r, y, profile, keys, under)` | A square pyramid roof with a profile; the last entry is the tip. |
| `d.arch(cell, a0, a1, spring, bottom=1, ends=('south','north'), ...)` | A round-headed opening: jambs, a half circle, upside-down stairs or a top slab where the curve falls half-way through a block, voussoirs, a key and imposts. `cell(a, y) -> (u, y, v)` lays it in any wall. Call it once for each layer of a two-thick wall. |
| `shutter(on, wood, half)` | An open trapdoor lying flat on the block on its `on` side. It works out the facing. |
| `toward(du, dv)` | The facing from a ring cell to the ring's centre. Use it for corbels and set-offs round towers. |
| `octo(du, dv, r)` | Inside an octagon (a square of radius r with its corners cut): a tower's plan. |
| `hash01(*key)` | A stable number in [0, 1). Every "random" choice uses it, so each run is identical. |

**Profiles** are a table `[(dy, kind)]` from the eave inward. `kind` is one of:

| kind | Draws |
|---|---|
| `'slab'` | a bottom slab |
| `'top'` | a top slab |
| `'stair'` | a stair facing the ridge |
| `'block'` | a full block (the ridge) |

Under each entry, the roof fills down to the outer neighbour's height, so a steep step shows a face
of roof, never a hole.

`keys` is `(stairs, slab, block)`. Each may be a function of k (the column's distance from the
eave), which gives a gradient: in the forge, moss tiles where k ≤ 2.

`verge` is the same three for the two gable rows. Pass dark oak there for thin barge boards.

## look

| Call | Does |
|---|---|
| `resolve(d)` | `{(u, y, v): block}`, with palette references picked. |
| `connect(blocks)` | Panes, bars, fences and walls joined to their neighbours, and stair corner shapes, using vanilla's rules. It prints any pane that joins nothing. **Always run it before checking, rendering or writing.** |
| `check(blocks, start, floors)` | Prints the floating blocks, things hung on nothing, flammables by lava, and, for each `(name, cells)` floor, how many cells a player reaches from `start`. Returns True when all are clean. |
| `render(Volume(blocks), prefix)` | Writes four PNGs: `-hero` (big, front left, sub-block shapes), `-iso` (front right, back right, back left), `-sides` (front, left, back and right elevations, whole cubes) and `-top`. |
| `close(blocks, prefix, (u0, u1, v0, v1), corners=(3, 2), s=24)` | Iso views cropped to the box, in sub-block shapes. |
| `iso(vol, corner, s)`, `elevation(vol, side, s)`, `fine(vol, 4)`, `write_png(path, rgb)` | The pieces, for custom views. `fine` cuts each block into 4×4×4 sub-cells in its rough shape (stairs, slabs, panes, fences, lanterns, plants). |
| `floating`, `unattached`, `fire_risk`, `walk` | The checks one at a time. |

Corners: 3 front left (the hero angle), 2 front right, 1 back right, 0 back left.

Renders colour each block by its name, with no textures. Judge shape, value and composition from
them; the real textures are in game.

## review.py

```bash
python builds/review.py builds/<build>.py close <prefix> u0 u1 v0 v1 [3,2]
python builds/review.py builds/<build>.py cut <prefix> ymax u0 u1 v0 v1 [corner]
python builds/review.py builds/<build>.py dump v 0 0 10 -7 7
```

`dump v 0 0 10 -7 7` prints the wall plane at v 0, y 10 down to 0, u 7 to -7 (the player's left to
right), one letter per block, with a key. Use it whenever a render looks wrong in a way the code
says it can't be.

## A build script's shape

Copy the layout of `examples/forge_legendary.py`:

```python
"""<Name>, <tier> (asked for by the user, <date>). <One line on what it is.>

Inspiration: <real buildings>, <famous RPGs> (named, none copied).

The story, which sets every material: <generations or phases, each with its material>.

Breakdown (the four heads):
Footprint and orientation. <entrance, facing, the path, shape, the dig, sizes in u/v>
Walls. <palettes as %, what stands proud and by how much, the window style>
Roof. <profiles, overhang, trim, dormers, chimneys and their crowns>
Props. <the trade's working parts inside and out, light, the yard>
Cost: <n> campfires, <n> lava, <n> water; no entities.

Frame (draw.py): u across the front, +u the player's left; v into the hill; y 0 the ground.
Run: python builds/<name>.py [render prefix]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import Drawing, hash01, octo, shutter, toward  # noqa: E402

d = Drawing("<title>")
d.palette('plinth', '...')                     # one palette per material, 3-4 close blocks
GATE = (0, 1, -20)                             # the paste origin: a player's feet on the path

# Then the volumes, big to small, each in its own section:
#   walls (with a gradient function like forge_legendary.stone), then the roof (keep its return
#   value), then gables filled to the surface y, then details, then the interior.
# After every roof: towers, stacks and turrets that pierce it.
# Then water, the yard, the hill (only into empty cells), trees, and a ground pass at y 0.

if __name__ == '__main__':
    import look
    import schem
    blocks = look.connect(look.resolve(d))
    floors = [('ground floor', [(u, 1, v) for u in range(-5, 6) for v in range(1, 10)])]
    good = look.check(blocks, GATE, floors)
    if len(sys.argv) > 1:
        print(look.render(look.Volume(blocks), sys.argv[1]))
        print(look.close(blocks, sys.argv[1] + '-main', (-10, 10, -8, 14)))
    schem.write(blocks, os.path.join(os.path.dirname(os.path.abspath(__file__)), '<name>.schem'), GATE)
    print('good' if good else 'NOT GOOD')
```

Useful patterns from the forge:

- **A gradient by height with jitter:**

  ```python
  def stone(u, y, v):
      t = y + (hash01('stone', u, y, v) - 0.5) * 1.6
      return '@plinth' if t < 1.5 else '@stone-lo' if t < 3.5 else '@stone'
  ```

- **A hill as a function**, from `hill`, `dug` and `height` in the forge. Rise behind the
  building, taper at the ends, and return 0 where the yard and the building are dug in. Then, per
  column:
  - fill the column with earth up to grass, into empty cells only;
  - use retaining stone next to the dug area;
  - put rock only where the step is 3 or more, or in rare two-by-two outcrops;
  - add ferns, grass and bushes by hash on top.
- **A ground pass last.** Every empty cell at y 0 becomes path, cobble, skirt or grass by zone,
  with ragged edges by hash.

## In game

The user does the in-game steps. Tell them:

- `//schem load <name>`, then `//paste` standing on the GATE spot. Face east to look at the
  front.
- A plain paste clears the box, because empty cells are air; `//paste -a` keeps what stands there.
  `//undo` takes it back.
- If the user edits the build in game, get their changes back (a schematic of the edited build,
  read with `schem.read`, diffed against the script's blocks) and fold them into the script as an
  `EDITS` list applied last.
