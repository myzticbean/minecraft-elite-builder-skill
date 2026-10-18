# Block vocabulary: recipes that worked

Every recipe here is in a build that the user liked. Coordinates are in the drawing's frame
(`toolkit.md`). Line numbers drift, so find each recipe in `examples/forge_legendary.py` by its
comment.

## Facings: the cheat sheet

| Block | Rule | How to write it |
|---|---|---|
| Stair | `facing` is its **high** side (the full back). | A roof stair faces the ridge. A step faces up the slope. |
| Upside-down stair (`half=top`) | The lower half hangs on its **facing** side; the open underside is opposite. | A corbel or bracket faces the wall it hangs from. A ring of corbels uses `toward(du, dv)`. Arch shoulders face **outward**, toward the jambs (`d.arch` does this). A barge board's underside faces away from the ridge. |
| Open trapdoor | The panel lies on the side **opposite** its facing. | Use `shutter(on)`, where `on` is the side of the cell where the block it lies against is. |
| Ladder, wall sign, wall banner, wall torch, tripwire hook, wall button | Hangs on the block **opposite** its facing (it faces away from the wall). | A banner on the front wall at v -1 is `facing=west`. |
| Door | The plate sits on the side opposite its facing. | Write both halves (`half=lower`, `half=upper`), with the same hinge and facing. |
| Lantern | `hanging=true` needs a block above; `hanging=false` needs one below. | A lantern on a fence post is standing. |
| Hanging sign, bell | Needs a block above, or `attachment=single_wall` on a wall for a bell. | |
| Logs | `axis=y` upright, `axis=z` a beam along u, `axis=x` a beam along v. | |
| Grindstone, lever, button | `face=floor/wall/ceiling`, plus a facing. | A grindstone on a wall reads as a pulley. |

`look.check` catches every hanging block with nothing behind it. Never silence the check; fix the
facing.

## Walls and frames

| Element | Recipe |
|---|---|
| Stone gradient | A per-cell function by y with jitter: plinth, then low stone, then stone. On a tower: then soot-1, soot-2 and soot-3 toward the crown (`tower_stone`). |
| Two-thick stone front | An arch in both layers. Windows are arched in the outer layer, with bars in the inner. |
| Plinth course | A row of stairs at y 1, a block proud. |
| String course | Upside-down stairs a block proud at the floor line, broken by a chiseled key over the arch. |
| Pilasters and quoins | Corner columns a block proud, alternating polished andesite and stone bricks. |
| Jetty | The upper storey a block out on every side. A dark oak plank band at the jetty line, a cove of upside-down stairs under it, and a hanging lantern under each corner. |
| Joist ends | A button on every other block of the jetty band (`dark_oak_button[face=wall]`). |
| Timber frame | Dark oak posts upright and a block proud, beams along the storey lines, plaster infill (`65%calcite,20%diorite,15%polished_diorite`). On a merchant's front, posts close together (close studding). |
| Posts on brackets | A post a block proud, starting on an upside-down stair corbel. |
| Window | A pane in the wall's own cell; a top slab or upside-down stair sill a block proud; shutters beside it (`shutter`). A lattice is an open trapdoor in the cell. |
| Flower box | A plank course a block out at sill height, with azalea leaves (`persistent=true`) on it. Pots on a sill. |
| Buttress | A stack of stone a block or two out, ending in a stair at its top. Stepped buttresses are a tall one and a short one. |
| Retaining wall | `retain` stone where the dug yard meets the hill, grass on top. |

## Roofs

- **The hall's bellcast** (13 wide plus overhang): `PH = [(0,'slab'), (0,'stair'), (1,'stair'),
  (2,'stair'), (4,'stair'), (6,'stair'), (8,'stair'), (9,'block')]`.
- **The house's**: `PS = [(0,'slab'), (0,'stair'), (1,'stair'), (2,'stair'), (4,'stair'),
  (6,'stair'), (7,'block')]`.
- **A small bridge roof**: `[(0,'stair'), (2,'block')]`.
- **A turret's spire**: `[(0,'stair'), (2,'stair'), (3,'block')]`, then a wall post and a lightning
  rod. Use plain tiles on a spire: moss belongs at eaves.
- **Keys**: `TILE = (stairs(k), slab(k), block)`, with moss tiles where k ≤ 2 (the eaves). The
  palettes:
  - `tiles`: deepslate tile, cobbled deepslate and deepslate brick stairs;
  - `tile-slab`: the same three as slabs;
  - `tile-block`: deepslate tiles, cobbled deepslate and deepslate bricks.
- **Verge**: `('dark_oak_stairs', 'dark_oak_slab', 'dark_oak_planks')`. It gives a thin barge
  board: a stair on the slope, with one upside-down stair under it.
- **Gables**: fill up to `roof(...)[a][0]`, the surface y.
  - A front gable: plaster in a dark oak frame, a king post (stripped log), two lancet panes, and a
    collar rail.
  - A back gable: stone with an oculus (panes in a plus, ringed in polished andesite).
- **Ridge**: a crest of `cobbled_deepslate_wall` along it, and finials of `lightning_rod` at the
  ends.
- **A louvre over a hearth**: fences in a box on the ridge under its own small roof.
- **A dormer**: its own little gable roof, drawn after the main roof.

## Chimneys and crowns

- **A trial chimney** climbs the outside of a gable wall, 2×2, from the ground to the ridge plus
  two. It is never buried in the roof.
- **The crown**:
  - a corbel ring of upside-down stairs facing the shaft (`toward`);
  - a parapet ring above it;
  - merlons (polished blackstone bricks) on alternate parapet cells.
- **Campfires sunk one block into the crown**: the ring hides the campfire's block and the smoke
  rises the same. For a 3×3 crown, put campfires in a plus.
- **Smaller stacks** get a corbel ring with campfires in it, or open trapdoors ringing the
  campfires at the same height.
- **The tower**: an octagonal base of `octo(…, 3)` up to y 8, a set-off ring of stairs at y 9, then
  an `octo(…, 2)` shaft up to y 25. Add a water table of stairs round the foot, stepped buttresses,
  and slits (iron bars with dark stone behind them).

## Curves

- **Arch**: `d.arch(lambda a, y: (a, y, v), a0, a1, spring)`. A 5-wide door springs at 4; 2-wide
  windows use `bottom=2`.
- **Water wheel** (radius about 6, the axle along u):
  - two shrouds, plank rings at u 8 and u 10 for 4.5 ≤ r < 6.2;
  - 8 fence spokes drawn as face-joined steps (`bridge_line`), a stripped-wood hub plus;
  - 16 dark oak buckets at the middle u, at r 5.3.

  A thin ring with paddles reads as a crate.
- **Flume**: a plank trough on log sides, with still water in it, on trestles of posts and a beam.
  A sluice board (`shutter`) sits over the wheel's top.
- **A dome** (a charcoal clamp): the height of each column is `3.2·sqrt(1 - (r/3.7)²)` plus a
  little jitter, filled with an earth mix. Log ends show at its foot. A campfire is sunk into the
  top and another into a side vent.

## Water

- Only `water[level=0]` sources, in level channels closed on every side, including the end walls.
- A race beside the building: a bank below, water, a slab kerb.
- A pond: an ellipse of sources with a bank; lily pads and reeds at its edges.
- Never a waterfall or a spill. Imply the flow with the wheel and the sluice.

## Light

| Where | Recipe |
|---|---|
| Under beams and trusses | An iron chain down from the tie beam, ending in `lantern[hanging=true]`. |
| Arch crown | A hanging lantern just inside the arch. |
| Posts and barrels | `lantern[hanging=false]` on top. |
| Fire | Lava in a closed magma bed (`magma_block` round it, stone everywhere within the fire spacing), or campfires. |
| Dark corners | A hidden `light` block, never under a slab. |

## The trade's micro-blocks (the forge)

| Means | Blocks |
|---|---|
| Ingots, plates | Heavy and light pressure plates, iron trapdoors |
| Tools on racks | Tripwire hooks, lightning rods (pokers, spears), chains |
| Hot coals | Magma blocks; campfires under iron bars; lava only in a closed bed |
| Bellows | Brown wool between spruce boards, a trapdoor lid, a lever beam on a post, a chain nozzle |
| Pulley, hoist | A grindstone on the ceiling or a wall, a chain down to a barrel |
| Raw stock | Raw iron blocks, coal blocks, barrels |
| The trip hammer | A log helve on a post frame, an iron block head over its anvil, cams on the wheel's axle |
| Guild sign | An anvil sitting on a bracket over a hanging sign |
| A farrier's stocks | A frame 2 high with a rail at 3, a trough and a hitching rail |

For a new trade, write its own table in the script's docstring before drawing, from what the work
really needs.

## Furniture idioms

| Furniture | Blocks |
|---|---|
| Table | A fence post with a pressure plate |
| Chair | A stair facing away from the table |
| Desk | A lectern |
| Counter | Faced with upside-down stairs, with a bell on it, pressure-plate trays and wall-sign tags |
| Fireplace | Bricks with a campfire behind iron bars |
| Bed | Against a wall, both halves written; carpet under the furniture |
| Storage | Barrels and chests in corners, with a lantern over the table |

## Palettes that read well (the forge)

```
plinth     30%cobblestone,25%mossy_cobblestone,20%andesite,15%tuff,10%stone
stone      50%stone_bricks,15%stone,15%andesite,10%cracked_stone_bricks,10%tuff_bricks
soot-3     35%deepslate_bricks,25%cracked_deepslate_bricks,20%polished_blackstone_bricks,20%blackstone
plaster    65%calcite,20%diorite,15%polished_diorite
path       40%cobblestone,25%gravel,20%coarse_dirt,15%packed_mud
skirt      40%coarse_dirt,25%podzol,20%gravel,15%packed_mud
bush       60%azalea_leaves[persistent=true],40%flowering_azalea_leaves[persistent=true]
```

For more styles (Medieval, Rustic, Nordic, Steampunk, Fantasy), see the style table in `method.md` section 6.
