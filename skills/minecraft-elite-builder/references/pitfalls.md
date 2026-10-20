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
| A block the server's resource pack redraws (mud bricks drawn as a dungeon's mossy rock) | It shows the pack's texture everywhere, so a brick chimney came out green in patches | Before choosing palettes, ask which vanilla blocks the server's pack overrides and keep them out of every build. |
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
| A spire set on a wider plank cornice read as a pagoda, its rings like tiers of a cake | Start the spire at its own eave, a block proud of the belfry, with no brim under it, in even steps of two. |
| A spire's heart is hollow: `d.spire` fills each ring down only to the ring outside it | The hollow is a dark room a mob can spawn in. Fill the inner columns after drawing it. |
| A cross gable over a room hung tiles at the room's ceiling | `d.roof` fills under its first stair down to the eave; inside a building that fill hangs in the room. Dump the plane and clear those cells. |
| A lantern base clad in plaster where it rose through the roof read as a chimney | Hang it with the roof's own tiles (slate-hung); keep plaster for walls under the eaves. |
| A long roof slope facing the square read bare | Break any slope over about ten blocks that faces the path with a dormer: its wall carried up through the eave, its own small gable. |
| Roofs drawn one over another (a hall between two cross-wings, dormers) left one roof's tiles hanging in the other's attic and its gable end standing through the other's slope | Draw each roof alone into an empty cell map, then merge: in every column two roofs share, the higher surface wins and the lower roof's cells there go. That is a valley. A roof's cells under its own surface never overwrite a wall already drawn. |
| A gable's verge overhanging the hill at a building's back covered the slope far below it, and every grass cell under it was dark | Over a hillside, end the roof in the back gable's own plane (no overhang there), and raise the slope to meet any eave that hangs within six blocks of it. |
| Paired chimney shafts with a corbel ring each, a block apart, merged into one wide slab at the crown | Space the shafts so their rings don't touch (a gap of three between 2×2 shafts). |

## Composition and scale

| Trap | Rule |
|---|---|
| A trial alchemist's house: every part present, but at the old size and without the reference's mass of stone. It read as busy, not rich. | Match the proportions and density first, then the parts. |
| A fat house (11 wide under a 1-in-1 roof) | Narrow and tall; the roof is about half the building's height. Count from a known small block. |
| A tower base as tall as the shaft reads stubby | Keep the base low (8) and the shaft tall (to 25). |
| Farrier's stocks 4 high and 5 long read as a gazebo | Keep things at real size. |
| A marketplace of many stalls drawn for one keeper | Every counter implies someone working it; in a game, a character. Ask how many keepers there are before drawing stalls, and dress the rest as unmanned. |
| Mossy voussoirs and moss blocks in a rubble face hid its arches | Arches in rough walls get dressed, paler voussoirs so they read. Moss goes in patches on the wall, never on the arch ring. |
| A woodshed hid the wheel from the hero corner | Keep the hero line clear: nothing at higher u and lower v than the feature. |
| A thin ring with three-wide paddles read as a crate | A wheel has two shrouds and buckets between them. |
| A cliff at the site's edge | Taper the hill at both ends and at the back. |
| Rock salted over every slope | Rock only on steps of 3 or more and in rare two-by-two outcrops. |
| A taper that subtracts from the hill still left cliffs where the hill stood tall | Scale the height instead: `h * clamp(distance to the edge / 6, 0, 1)`. |
| "From scratch" rebuilt an old reference | When the user asks for one's own design, trace no reference; name the inspirations. |

## Drawing

| Trap | Rule |
|---|---|
| A spoke or diagonal line floats | `d.line` can join cells at an edge only. Step one axis at a time (`bridge_line`), because `look.floating` needs faces to touch. |
| A jetty's floor band, drawn across a party wall, cut a plank stripe through the older stone wall it ran over | Redraw the older wall after the jetties, or stop the floor at its face. |
| Tie beams run out to the wall line replaced the eave tiles at both ends | Stop beams a block inside the outer walls; a roof's eave sits in that column. |
| Brackets under a jetty, written at the ground wall's v, landed in the wall | A bracket goes in the jetty's own plane, one block under its cove, facing the wall below. |
| A flight of stairs drew fine, but the floor above it was never reached | A player jumps from step to step and needs three clear blocks over each step, not two: clear the floor above the top steps too. |
| A timber storey with posts every three blocks, a sill rail, a head rail and a window in every bay left no infill: it read as a dark grid | Wide bays (four or five), one window framed in infill in each, no sill rail on a storey that already has a jetty band under it. |
| Stall posts stopped under an awning of top-half trapdoors, which floated half a block above them in game | Run the corner posts up into the awning's own cells (fences there, the carpet on their tops); the render hides a half-block gap. |
| Diagonal truss struts floated | The same edge-only join. Use queen posts and a collar: upright and level members only. |
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
| A cut at the ceiling's own y showed a solid floor | The ymax must be under the ceiling's y; one too high shows the floor above. |
| Belfries, lofts and roof hollows were dark, and no render showed it | Mobs spawn at block light 0 under any roof. Flood-fill block light from every lamp and fire; every covered cell a mob could stand in needs light 1 or more. A hidden `light` under a bell is fair. |
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
