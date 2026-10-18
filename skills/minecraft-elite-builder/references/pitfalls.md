# Pitfalls: every trap already paid for

Each one cost a rejected build or a render pass. Read this before drawing, and add every new trap
after each build.

## Paste physics

A schematic pastes block states exactly as written, with no neighbour updates until something
nearby changes. Then vanilla takes over.

| Trap | What happens | Rule |
|---|---|---|
| Panes, bars, fences and walls without their sides | Thin posts, and gaps in railings | Run `look.connect` on every build before checking, rendering or writing. |
| Stair corners | Straight stairs where a corner should turn | `look.connect` sets `shape` (ported from vanilla). |
| Flowing water | Spreads on the first update | Only `water[level=0]` sources, in level channels closed on every side. No waterfalls. |
| `furnace[lit=true]` or `blast_furnace[lit=true]` | Goes out on its first tick | Get the glow from lava, magma, campfires or `light`. |
| Anvils, gravel, sand, concrete powder | Fall | Set them on something solid. |
| Leaves | Decay away from logs | Always `persistent=true`. |
| Vines | Grow on random ticks and creep over walls between resets | Don't use them. Put moss in the stone where it's damp. |
| Empty cells | Paste as air and clear the box | The drawing holds its own ground and hill. `'air'` cells cut on purpose. |
| Doors, beds | Half a door or bed breaks | Write both halves. |
| Entities (armour stands, item frames, minecarts) | Cost every tick | Never. Make the same meaning from blocks. |
| Chest contents, sign text | A design carries no block-entity data | Leave them empty, or say so. |

## Facings

| Trap | Rule |
|---|---|
| A trapdoor ring round a chimney stood a block clear of it, because the facing pointed *at* the chimney | An open trapdoor's panel is opposite its facing: use `shutter(on)`. The same goes for ladders, buttons, wall signs and banners (`look.unattached` catches them). |
| "Windows set a block in" put the pane in the room | Panes and bars stay in the wall's own cell. Only a two-thick wall has a reveal. `look.connect` prints a pane that joins nothing. |
| Sides named "left" and "right" swapped | +u is the player's left, so low u is the right. Name sides by u or v. |
| A lantern on a fence written as hanging | Hanging needs a block above; standing needs one below. |

## Roofs

| Trap | Rule |
|---|---|
| Heavy dark triangles round the gables | A barge board is thin (`verge=` in `d.roof`): fill the gable to the surface y, not to the roof's lowest y. |
| Two roofs read as one long roof | Never start a lower roof on the line of a higher one's slope. Give each its own gable at its own beam. |
| A tower or stack cut by a roof drawn later | Draw roofs first, then whatever pierces them. |
| A squat spire | A steep pyramid ending in a block, a wall post and a rod. Moss on a spire looks wrong; keep it at eaves. |

## Composition and scale

| Trap | Rule |
|---|---|
| A trial alchemist's house: every part present, but at the old size and without the reference's mass of stone. It read as busy, not rich. | Match the proportions and density first, then the parts. |
| A fat house (11 wide under a 1-in-1 roof) | Narrow and tall; the roof is about half the building's height. Count from a known small block. |
| A tower base as tall as the shaft reads stubby | Keep the base low (8) and the shaft tall (to 25). |
| Farrier's stocks 4 high and 5 long read as a gazebo | Keep things at real size. |
| A woodshed hid the wheel from the hero corner | Keep the hero line clear: nothing at higher u and lower v than the feature. |
| A thin ring with three-wide paddles read as a crate | A wheel has two shrouds and buckets between them. |
| A cliff at the site's edge | Taper the hill at both ends and at the back. |
| Rock salted over every slope | Rock only on steps of 3 or more and in rare two-by-two outcrops. |
| "From scratch" rebuilt an old reference | When the user asks for one's own design, trace no reference; name the inspirations. |

## Drawing

| Trap | Rule |
|---|---|
| A spoke or diagonal line floats | `d.line` can join cells at an edge only. Step one axis at a time (`bridge_line`), because `look.floating` needs faces to touch. |
| A pendant on a corbel ring floated | The ring's centre was empty. Fill it (a plank) so the pendant hangs on something. |
| Fences near lava | Use iron bars within 2 sideways and 5 above lava (`look.fire_risk`). |
| A decoration overwrote a door's surround | Later `set` calls overwrite. Guard them with `if d.get(...) is None`, or draw the decoration first. |
| Ivy coordinates landed inside the house | Check a decoration's cells against the walls; prefer a hash rule placed only into empty cells. |
| A hill filled the hall | Draw the hill after the buildings, and only into empty cells. |

## Reviewing

| Trap | Rule |
|---|---|
| The front looked missing in an iso view, but a cell dump showed it whole (foreshortening) | Never "fix" what a render misreads. Check it first with `review.py dump`. |
| Site-wide renders too small to judge | Use close views cropped to each volume plus a few blocks, `s=24` to `28`, from two corners. |
| Interiors can't be seen | `review.py cut` with a ymax just under the ceiling. |
| A render's colour isn't the block's texture | Renders colour by name. Judge shape and value; the real textures show in game. |
| The schematic file hash changes on every run | It's the gzip timestamp. To compare two builds, hash the uncompressed bytes (`gzip.open(...).read()`). |

## Time

The legendary forge took a long time: about 1,050 lines, five render passes, plus new tooling (the
profiled roof, thin verges, the sub-block renderer) and the method notes. To be faster next time:

- Block out and fix the composition before any detail. Most rework came from composition found
  late: the woodshed, the tower's proportion, the hill's edge.
- In each pass, fix every defect seen before rendering again; don't render after each one.
- Reuse what's in `draw.py` and this vocabulary; only new shapes need new code.
- Keep each volume in its own section with its own constants (`HU`, `TU`, `XU0`), so moving one
  is a one-line change.
