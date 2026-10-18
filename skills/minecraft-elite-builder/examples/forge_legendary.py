"""The forge at its legendary tier (the user asked for one, 2026-10-18): the trial forge's trade
grown over three generations into a hammer mill, built by the method in references/method.md.
The worked example of the minecraft-elite-builder skill.

Inspiration: the water-powered hammer mills of medieval Europe (a wheel turning a camshaft that
lifts a trip hammer), the jettied merchants' houses of Tudor England, and the great smithies of
fantasy RPGs (Skyrim's Skyforge on its rock, The Witcher 3's Hattori workshop in Novigrad): a smithy
that is a landmark of its town. None copied: the layout below is its own.

The story, which sets every material:
- The grandfather's smithy: a squat stone tower whose chimney still serves the great hearth, too
  strong to pull down. Rough stone, sooted darker toward the crown.
- The father's forge hall built against it: a stone hall with a timber gable, a water wheel on
  its left driving a trip hammer inside, fed by a flume on trestles from a spring up the hill.
- The master's own house to the right: a stone shop under a jettied, close-studded upper storey,
  a corner turret, a dormer, joined to the hall's gallery by a bridge over the gate to the old
  tower's door.

Breakdown (the four heads):

Footprint and orientation. Everything faces the path and is dug into the hill at the back. From
the path, left to right: the race, the wheel and the flume on the far left; the hall in the middle
(13 wide, 16 deep, its steep gable to the path); the tower behind it on the right; the bridge and
the gate; the house (12 wide, 10 deep, its ridge across the front). The forecourt is cobbled; a
pond at the race's foot. Floors are flush with the ground.

Walls. Stone on a gradient: moss and cobble at the plinth, stone bricks above, soot (deepslate,
then blackstone) up the tower. The hall's front two thick: a round-headed arch five wide, arched
windows with bars in the inner layer, a plinth course, corner pilasters, a string course, a dark oak
jetty band with joist ends; the gable plaster in a dark oak frame with a king post, two lancets and
a hoist. The house: a stone ground storey with quoins, a bay window and an arched door under a
jetty with a cove, the upper storey plaster close-studded in dark oak, flower box, shutters, posts
a block proud on brackets.

Roof. Bellcast slate (deepslate tile, mossier at the eaves) on profiles: shallow at the eave, two
up for one toward the ridge; dark oak barge boards; a crest of walls on the ridges. The hall's ridge
along the path with a louvre and two finials; the house's across it with a dormer and a corner
turret's spire; the bridge's tucked between. Chimneys: the tower's crown (a corbel, a parapet,
merlons, a fire pit), the hall's back stack, the house's stack on its gable, each with campfires
sunk into a corbel ring.

Props. The hall: the great hearth (lava in a magma bed, a stepped hood into the tower), bellows on
a lever, anvil, quench trough, grindstone, coal and ore bins; the trip hammer on its frame, lifted
by cams on the wheel's axle; a finishing hearth; trusses on corbels with lanterns on chains; the
master's gallery with a ladder. The house: a showroom with a counter and a bell, polearms, a
fireplace, stairs up; the master's room (bed, table, lectern) open to the rafters. The yard: the
anvil sign over the path, a farrier's stocks and trough, a wagon of ore, a charcoal clamp smoking
with its woodshed, a slag heap, a pond with reeds and lilies, lanterns about every five
blocks. No entities. Nothing flammable near the lava (look.fire_risk).

Frame (draw.py): u across the front, +u the left hand of someone on the path; v back into the hill;
y 0 the ground's own layer, so a player on it stands at y 1. Facings are the file's: west is out of
the front, east into the hill, north is +u, south is -u.

Run: python examples/forge_legendary.py [render prefix]
Writes forge_legendary.schem next to this file; the paste origin is GATE.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'scripts'))
from draw import Drawing, hash01, octo, shutter, toward  # noqa: E402

d = Drawing("The forge, legendary: a hammer mill of three generations, Claude's design.")
d.palette('plinth', '30%cobblestone,25%mossy_cobblestone,20%andesite,15%tuff,10%stone')
d.palette('stone-lo', '35%stone_bricks,20%mossy_stone_bricks,15%cobblestone,15%andesite,15%cracked_stone_bricks')
d.palette('stone', '50%stone_bricks,15%stone,15%andesite,10%cracked_stone_bricks,10%tuff_bricks')
d.palette('soot-1', '40%stone_bricks,30%tuff_bricks,30%cobbled_deepslate')
d.palette('soot-2', '45%cobbled_deepslate,40%deepslate_bricks,15%tuff_bricks')
d.palette('soot-3', '35%deepslate_bricks,25%cracked_deepslate_bricks,20%polished_blackstone_bricks,20%blackstone')
d.palette('hearth', '45%deepslate_bricks,30%polished_deepslate,25%cobbled_deepslate')
d.palette('plaster', '65%calcite,20%diorite,15%polished_diorite')
d.palette('tiles', '55%deepslate_tile_stairs,25%cobbled_deepslate_stairs,20%deepslate_brick_stairs')
d.palette('tiles-low', '40%deepslate_tile_stairs,30%cobbled_deepslate_stairs,15%deepslate_brick_stairs,'
                       '15%mossy_cobblestone_stairs')
d.palette('tile-slab', '55%deepslate_tile_slab,25%cobbled_deepslate_slab,20%deepslate_brick_slab')
d.palette('tile-slab-low', '40%deepslate_tile_slab,30%cobbled_deepslate_slab,15%deepslate_brick_slab,'
                           '15%mossy_cobblestone_slab')
d.palette('tile-block', '50%deepslate_tiles,30%cobbled_deepslate,20%deepslate_bricks')
d.palette('floor', '35%packed_mud,25%coarse_dirt,20%cobblestone,20%tuff')
d.palette('flag', '45%stone_bricks,25%polished_andesite,20%cracked_stone_bricks,10%andesite')
d.palette('cobble', '45%cobblestone,20%mossy_cobblestone,15%gravel,10%andesite,10%stone')
d.palette('path', '40%cobblestone,25%gravel,20%coarse_dirt,15%packed_mud')
d.palette('skirt', '40%coarse_dirt,25%podzol,20%gravel,15%packed_mud')
d.palette('slag', '30%gravel,25%tuff,20%blackstone,15%cobbled_deepslate,10%coal_ore')
d.palette('logs', '60%spruce_log[axis=x],25%oak_log[axis=x],15%dark_oak_log[axis=x]')
d.palette('hill-rock', '35%stone,25%andesite,20%tuff,20%cobblestone')
d.palette('retain', '35%cobblestone,25%mossy_cobblestone,20%stone_bricks,20%mossy_stone_bricks')
d.palette('bank', '50%stone_bricks,30%mossy_stone_bricks,20%cobblestone')
d.palette('earth', '75%dirt,25%coarse_dirt')
d.palette('clamp', '35%coarse_dirt,30%packed_mud,20%podzol,15%mud')
d.palette('bush', '60%azalea_leaves[persistent=true],40%flowering_azalea_leaves[persistent=true]')

DO = 'dark_oak_log[axis=y]'
DOZ = 'dark_oak_log[axis=z]'                  # a beam along u
DOX = 'dark_oak_log[axis=x]'                  # a beam along v
SDO = 'stripped_dark_oak_log[axis=y]'
LIT = 'campfire[lit=true,signal_fire=false,facing=west]'
HANG = 'lantern[hanging=true]'
STAND = 'lantern[hanging=false]'
GATE = (0, 1, -22)                            # the paste origin: a player's feet on the path
TILE = (lambda k: '@tiles-low' if k <= 2 else '@tiles',
        lambda k: '@tile-slab-low' if k <= 2 else '@tile-slab', '@tile-block')
PLAIN = ('@tiles', '@tile-slab', '@tile-block')
VERGE = ('dark_oak_stairs', 'dark_oak_slab', 'dark_oak_planks')


def stone(u, y, v):
    """Wall stone on its gradient: rough and mossy at the foot, stone bricks above."""
    t = y + (hash01('stone', u, y, v) - 0.5) * 1.6
    return '@plinth' if t < 1.5 else '@stone-lo' if t < 3.5 else '@stone'


# ------------------------------------------------------------ the hall: stone walls

HU, HV = 6, 15                                 # the hall's walls: u -6..6, v 0..15
for u in range(-HU, HU + 1):
    for v in range(0, HV + 1):
        front, side, back = v in (0, 1), u in (-HU, HU), v == HV
        if not (front or side or back):
            continue
        for y in range(0, (8 if front else 9) + 1):
            if u == HU and 2 <= v < HV and y >= 5:
                continue                       # the left side's timber storey, below
            d.set(u, y, v, stone(u, y, v))

# The front: a great arch, an arched window either side with bars in the inner layer, corner
# pilasters, a plinth course, a string course, the jetty band with its joist ends.
for v in (0, 1):
    d.arch(lambda a, y, v=v: (a, y, v), -2, 2, 4)
    for a in range(-2, 3):
        d.set(a, 0, v, '@flag')
for u0 in (-5, 4):
    d.arch(lambda a, y: (a, y, 0), u0, u0 + 1, 4, bottom=2)
    for u in (u0, u0 + 1):
        for y in (2, 3, 4):
            d.set(u, y, 1, 'iron_bars')
for u in (-HU, HU):
    for y in range(0, 8):
        d.set(u, y, -1, 'polished_andesite' if y % 2 else 'stone_bricks')
for u in (-5, -4, -3, 3, 4, 5):
    d.set(u, 1, -1, 'stone_brick_stairs[facing=east,half=bottom]')
for u in range(-HU, HU + 1):
    d.set(u, 8, -1, 'stone_brick_stairs[facing=east,half=top]')
    for v in (-1, 0, 1):
        d.set(u, 9, v, 'dark_oak_planks')
    if u % 2 == 0 and abs(u) != 2:
        d.set(u, 9, -2, 'dark_oak_button[face=wall,facing=west,powered=false]')
for u in (-3, 3):
    d.set(u, 7, -1, 'black_wall_banner[facing=west]')
for u in (-5, 5):
    d.set(u, 7, -1, HANG)
d.set(0, 6, 0, HANG)                           # a lantern in the arch's crown
d.set(0, 8, -1, 'chiseled_stone_bricks')        # the key, breaking the string course

# The left side, toward the wheel: a timber storey on the stone, posts a block proud on corbels;
# a buttress at the front corner takes the wheel's thrust.
for v in range(2, HV):
    d.set(HU, 5, v, DOX)
    d.set(HU, 9, v, DOX)
    for y in (6, 7, 8):
        d.set(HU, y, v, DO if v in (3, 7, 11) else '@plaster')
for v in (4, 5, 9, 10):
    for y in (7, 8):
        d.set(HU, y, v, 'glass_pane')
    d.set(HU + 1, 6, v, 'dark_oak_slab[type=top]')
for v in (3, 11):
    d.set(HU + 1, 4, v, 'stone_brick_stairs[facing=south,half=top]')
    for y in range(5, 10):
        d.set(HU + 1, y, v, DO)
for v in (0, 1):
    for y in range(1, 7):
        d.set(HU + 1, y, v, stone(HU + 1, y, v))
    d.set(HU + 1, 7, v, 'stone_brick_stairs[facing=south,half=bottom]')

# The right side: all stone (the hearth's side); a door from the court under the gallery, another
# from the bridge onto it.
for y, half in ((1, 'lower'), (2, 'upper')):
    d.set(-HU, y, 5, 'dark_oak_door[facing=north,half=%s,hinge=left,open=false,powered=false]' % half)
for y, half in ((6, 'lower'), (7, 'upper')):
    d.set(-HU, y, 2, 'dark_oak_door[facing=north,half=%s,hinge=right,open=false,powered=false]' % half)

# ------------------------------------------------------------ the hall: roof and gables

PH = [(0, 'slab'), (0, 'stair'), (1, 'stair'), (2, 'stair'), (4, 'stair'), (6, 'stair'), (8, 'stair'), (9, 'block')]
hall = d.roof(-7, 7, -2, HV + 1, 10, PH, TILE, '@tile-block', along='v', verge=VERGE)

# The front gable, a block out over the jetty: plaster in a dark oak frame, a king post between two
# lancets, a collar rail, posts a block proud on brackets either side; the hoist out of the apex.
for u in range(-5, 6):
    for y in range(10, hall[u][0]):
        if u == 0:
            b = SDO
        elif abs(u) == 1 and 11 <= y <= 13:
            b = 'glass_pane'
        elif abs(u) == 1 and y == 14:
            b = 'stripped_dark_oak_log[axis=z]'
        else:
            b = '@plaster'
        d.set(u, y, -1, b)
for u in (-1, 1):
    d.set(u, 10, -2, 'dark_oak_slab[type=top]')
for u in (-2, 2):
    d.set(u, 9, -2, 'dark_oak_stairs[facing=east,half=top]')
    for y in range(10, 14):
        d.set(u, y, -2, DO)
for v in range(-5, 0):
    d.set(0, 17, v, DOX)
d.set(0, 16, -2, 'dark_oak_stairs[facing=east,half=top]')
d.set(0, 16, -5, 'grindstone[face=ceiling,facing=west]')
for y in range(11, 16):
    d.set(0, y, -5, 'iron_chain[axis=y]')
d.set(0, 10, -5, 'barrel[facing=up,open=false]')

# The back gable: stone, a round window.
for u in range(-5, 6):
    for y in range(10, hall[u][0]):
        d.set(u, y, HV, stone(u, y, HV))
for u, y in ((0, 12), (0, 13), (0, 14), (-1, 13), (1, 13)):
    d.set(u, y, HV, 'glass_pane')
for u, y in ((0, 11), (0, 15), (-2, 13), (2, 13), (-1, 12), (1, 12), (-1, 14), (1, 14)):
    d.set(u, y, HV, 'polished_andesite')

# The crest, the finials, and a louvre on the ridge over the hearths.
for v in list(range(-1, 5)) + list(range(10, HV + 1)):
    d.set(0, 20, v, 'cobbled_deepslate_wall')
for v in (-2, HV + 1):
    d.set(0, 20, v, 'lightning_rod[facing=up,powered=false]')
for v in (6, 7, 8):
    for u in (-1, 1):
        d.set(u, 19, v, 'dark_oak_fence')
        d.set(u, 20, v, 'dark_oak_fence')
for v in (6, 8):
    d.set(0, 20, v, 'dark_oak_fence')
d.roof(-2, 2, 5, 9, 21, [(0, 'slab'), (0, 'stair'), (1, 'block')], PLAIN, '@tile-block', along='v', verge=VERGE)

# ------------------------------------------------------------ the hall inside

for u in range(-5, 6):
    for v in range(2, HV):
        d.set(u, 0, v, '@flag' if abs(u) <= 1 and v <= 9 else '@floor')

# Trusses: tie beams on stone corbels, king posts, struts to the rafters, a lantern on a chain.
for v in (3, 7, 11):
    for u in (-5, 5):
        d.set(u, 8, v, 'stone_brick_stairs[facing=%s,half=top]' % ('north' if u > 0 else 'south'))
    for u in range(-5, 6):
        d.set(u, 9, v, DOZ)
    for y in range(10, 18):
        d.set(0, y, v, SDO)
    for s in (-1, 1):
        d.set(s, 11, v, 'stripped_dark_oak_wood')
        d.set(2 * s, 12, v, 'stripped_dark_oak_wood')
    d.set(0, 8, v, 'iron_chain[axis=y]')
    d.set(0, 7, v, 'iron_chain[axis=y]')
    d.set(0, 6, v, HANG)

# The great hearth against the tower: lava in a magma bed, stone cheeks, a bar lip, a hood stepping
# back into the old chimney. All stone within the fire spacing.
for u in range(-5, -1):
    for v in range(8, 13):
        d.set(u, 0, v, '@hearth')
for u in range(-5, -2):
    for v in range(9, 12):
        d.set(u, 1, v, '@hearth')
d.set(-4, 1, 10, 'lava[level=0]')
for p in ((-5, 1, 10), (-3, 1, 10), (-4, 1, 9), (-4, 1, 11)):
    d.set(*p, 'magma_block')
for v in (8, 12):
    for u in range(-5, -1):
        for y in (1, 2, 3):
            d.set(u, y, v, '@soot-1')
for v in (9, 10, 11):
    d.set(-2, 1, v, 'iron_bars')
for y, half, ring in ((4, 'top', range(-5, -1)), (5, 'bottom', range(-5, -1)), (6, 'bottom', range(-5, -2))):
    lo, hi = (8, 12) if y < 6 else (9, 11)
    edge_u = ring[-1]
    for u in ring:
        for v in range(lo, hi + 1):
            if u == edge_u or v in (lo, hi):
                face = 'east' if v == lo else 'west' if v == hi else 'south'
                d.set(u, y, v, 'deepslate_brick_stairs[facing=%s,half=%s]' % (face, half))
            else:
                d.set(u, y, v, '@soot-2')
for u in (-5, -4):
    for v in (9, 10, 11):
        d.set(u, 7, v, '@soot-2')
for v in (9, 10, 11):
    d.set(-5, 8, v, '@soot-3')
d.set(-1, 1, 10, 'anvil[facing=north]')
d.set(-1, 1, 12, 'water_cauldron[level=3]')
d.set(1, 1, 9, 'grindstone[face=floor,facing=north]')

# The bellows on a lever: leather between boards, a chain nozzle through the cheek into the bed.
for u in (-5, -4):
    for v in (13, 14):
        d.set(u, 1, v, 'spruce_planks')
        d.set(u, 2, v, 'brown_wool')
        d.set(u, 3, v, 'spruce_trapdoor[facing=east,half=bottom,open=false]')
d.set(-4, 2, 12, 'iron_chain[axis=x]')
for y in range(1, 5):
    d.set(-2, y, 14, DO)
for u in range(-5, -1):
    d.set(u, 5, 14, DOZ)
d.set(-4, 4, 14, 'iron_chain[axis=y]')
# Coal and ore by the back wall.
for p, b in (((-1, 1, 14), 'coal_block'), ((0, 1, 14), 'coal_block'), ((0, 2, 14), 'coal_block'),
             ((-1, 1, 13), 'barrel[facing=up,open=true]'), ((1, 1, 14), 'raw_iron_block'),
             ((1, 1, 13), 'raw_iron_block'), ((1, 2, 14), 'barrel[facing=up,open=false]')):
    d.set(*p, b)

# The trip hammer: a log helve on a post frame, an iron head over its anvil, lifted at its tail by
# cams on the wheel's axle, which comes through the left wall.
for v in range(2, 7):
    d.set(3, 5, v, 'stripped_dark_oak_log[axis=x]')
for u in (2, 4):
    for y in range(1, 6):
        d.set(u, y, 4, DO)
for u in (2, 3, 4):
    d.set(u, 6, 4, DOZ)
d.set(3, 4, 2, 'iron_block')
d.set(3, 1, 2, 'polished_deepslate')
d.set(3, 2, 2, 'anvil[facing=north]')
for u in range(3, 12):
    d.set(u, 6, 7, DOZ)
for p in ((3, 5, 7), (3, 7, 7), (3, 6, 8)):
    d.set(*p, 'stripped_dark_oak_wood')
# The quench trough, the bench and its tool rack.
for u in (3, 4, 5):
    for v in (8, 9, 10, 11):
        d.set(u, 0, v, 'stone_bricks')
        d.set(u, 1, v, 'water[level=0]' if u >= 4 and v in (9, 10) else 'polished_andesite')
d.set(5, 1, 5, 'smithing_table')
d.set(5, 1, 6, 'crafting_table')
d.set(5, 2, 5, 'heavy_weighted_pressure_plate[power=0]')
for v in (5, 6):
    d.set(5, 3, v, 'tripwire_hook[facing=south,attached=false,powered=false]')

# The finishing hearth in the back left corner: coals on a stone bed under a hood, its own stack.
for u in (3, 4, 5):
    for v in (12, 13, 14):
        d.set(u, 0, v, '@hearth')
        d.set(u, 1, v, '@hearth')
for u in (4, 5):
    for v in (13, 14):
        d.set(u, 2, v, 'magma_block')
d.set(3, 2, 12, '@soot-1')
d.set(3, 3, 12, '@soot-1')
for y, half in ((4, 'top'), (5, 'bottom')):
    for u in (3, 4, 5):
        for v in (12, 13, 14):
            if u == 3 or v == 12:
                d.set(u, y, v, 'deepslate_brick_stairs[facing=%s,half=%s]' % ('east' if v == 12 else 'north', half))
            else:
                d.set(u, y, v, '@soot-1')
for u in (4, 5):
    for v in (13, 14):
        for y in range(6, 18):
            d.set(u, y, v, '@soot-1' if y < 12 else '@soot-2')
        d.set(u, 18, v, LIT)
for u in range(3, 7):
    for v in range(12, 16):
        if u in (3, 6) or v in (12, 15):
            face = 'east' if v == 12 else 'west' if v == 15 else 'north' if u == 3 else 'south'
            d.set(u, 18, v, 'deepslate_brick_stairs[facing=%s,half=top]' % face)
            if u in (3, 6) and v in (12, 15):
                d.set(u, 19, v, 'cobbled_deepslate_wall')

# The master's gallery over the racks, a ladder up to it, a rail along its edge.
for u in (-5, -4, -3):
    for v in range(2, 8):
        d.set(u, 5, v, 'spruce_planks')
for v in range(2, 8):
    d.set(-2, 5, v, DOX)
    d.set(-2, 6, v, 'dark_oak_fence')
for u in (-4, -3):
    d.set(u, 6, 8, 'iron_bars')
for v in (2, 7):
    for y in range(1, 5):
        d.set(-2, y, v, DO)
d.clear(-5, 5, 7)
for y in range(1, 7):
    d.set(-5, y, 7, 'ladder[facing=north]')
for p, b in (((-5, 1, 2), 'barrel[facing=up,open=false]'), ((-5, 2, 2), 'barrel[facing=up,open=true]'),
             ((-5, 1, 3), 'chest[facing=north,type=single,waterlogged=false]'),
             ((-5, 1, 4), 'lightning_rod[facing=up,powered=false]'),
             ((-5, 1, 6), 'lightning_rod[facing=up,powered=false]'),
             ((-4, 4, 4), HANG),
             ((-5, 6, 3), 'barrel[facing=up,open=false]'), ((-5, 7, 3), STAND),
             ((-5, 6, 4), 'lectern[facing=north,has_book=false,powered=false]'),
             ((-5, 6, 5), 'chest[facing=north,type=single,waterlogged=false]'),
             ((-3, 6, 4), 'spruce_stairs[facing=north,half=bottom]')):
    d.set(*p, b)
for v in (2, 3, 4):
    d.set(-5, 3, v, 'tripwire_hook[facing=north,attached=false,powered=false]')

# ------------------------------------------------------------ the house: a stone ground storey

XU0, XU1, XV0, XV1 = -21, -10, -2, 7           # the ground storey's walls
for u in range(XU0, XU1 + 1):
    for v in range(XV0, XV1 + 1):
        if u in (XU0, XU1) or v in (XV0, XV0 + 1, XV1):
            for y in range(0, 5):
                d.set(u, y, v, stone(u, y, v))
        else:
            d.set(u, 0, v, '@flag')
for y in range(0, 5):                          # quoins, long and short by turns
    for u, inward in ((XU0, 1), (XU1, -1)):
        d.set(u, y, XV0, 'polished_andesite')
        d.set(*((u + inward, y, XV0) if y % 2 else (u, y, XV0 + 2)), 'polished_andesite')

# The arched double door, in the inner layer.
for u, hinge in ((-13, 'right'), (-12, 'left')):
    for y, half in ((1, 'lower'), (2, 'upper')):
        d.set(u, y, XV0 + 1, 'dark_oak_door[facing=east,half=%s,hinge=%s,open=false,powered=false]' % (half, hinge))
        d.set(u, y, XV0, 'air')
    d.set(u, 0, XV0, '@flag')
    d.set(u, 0, XV0 + 1, '@flag')
    d.set(u, 4, XV0, 'chiseled_stone_bricks')
d.set(-13, 3, XV0, 'stone_brick_stairs[facing=south,half=top]')
d.set(-12, 3, XV0, 'stone_brick_stairs[facing=north,half=top]')

# The bay window under the jetty, its seat in the wall; a bench by the door; a plinth course.
for u in range(-19, -15):
    d.set(u, 1, XV0 - 1, 'stone_bricks')
for u in (-19, -16):
    for y in (2, 3):
        d.set(u, y, XV0 - 1, DO)
for u in (-18, -17):
    for y in (2, 3):
        d.set(u, y, XV0 - 1, 'glass_pane')
        d.set(u, y, XV0, 'air')
        d.set(u, y, XV0 + 1, 'air')
for u in (-15, -14):
    d.set(u, 1, XV0 - 1, 'spruce_stairs[facing=east,half=bottom]')
for u in (-21, -20, -11, -10):
    d.set(u, 1, XV0 - 1, 'stone_brick_stairs[facing=east,half=bottom]')
for v in (5, 6):                               # the right side's window, the back door
    for y in (2, 3):
        d.set(XU0, y, v, 'iron_bars')
for y, half in ((1, 'lower'), (2, 'upper')):
    d.set(-16, y, XV1, 'dark_oak_door[facing=east,half=%s,hinge=left,open=false,powered=false]' % half)

# ------------------------------------------------------------ the house: the jettied upper storey

JU0, JV0 = -22, -3                              # the upper storey's planes: u -22..-10, v -3..7
for u in range(JU0, XU1 + 1):
    for v in range(JV0, XV1 + 1):
        d.set(u, 5, v, 'dark_oak_planks' if u == JU0 or v == JV0 else 'spruce_planks')
for u in range(JU0, XU1 + 1):                   # the cove under the jetty, joist ends on the band
    d.set(u, 4, JV0, 'spruce_stairs[facing=east,half=top]')
    if u % 2:
        d.set(u, 5, JV0 - 1, 'dark_oak_button[face=wall,facing=west,powered=false]')
for v in range(JV0, XV1 + 1):
    d.set(JU0, 4, v, 'spruce_stairs[facing=north,half=top]')
    if v % 2:
        d.set(JU0 - 1, 5, v, 'dark_oak_button[face=wall,facing=south,powered=false]')
for u in (-20, -14):
    d.set(u, 3, JV0, HANG)

FRONT = {-22: DO, -18: DO, -14: DO, -10: DO}    # the front: studs, three windows, symmetric on u -16
for u in range(JU0, XU1 + 1):
    for y in range(6, 10):
        if u in FRONT:
            b = FRONT[u]
        elif y in (7, 8) and u in (-20, -19, -17, -16, -15, -13, -12):
            b = 'glass_pane'
        else:
            b = '@plaster'
        d.set(u, y, JV0, b)
    d.set(u, 10, JV0, DOZ)
for u in (-18, -14, -10):                       # posts a block proud on brackets, under the eave
    d.set(u, 5, JV0 - 1, 'dark_oak_stairs[facing=east,half=top]')
    for y in range(6, 10):
        d.set(u, y, JV0 - 1, DO)
    d.set(u, 10, JV0 - 1, 'dark_oak_stairs[facing=east,half=top]')
for u in (-20, -19, -13, -12, -17, -16, -15):
    d.set(u, 6, JV0 - 1, 'dark_oak_slab[type=top]')
for u in (-17, -16, -15):                       # the flower box under the middle window
    d.set(u, 6, JV0 - 1, '@bush')
    d.set(u, 6, JV0 - 2, shutter('east'))
for u in (-21, -11):
    for y in (7, 8):
        d.set(u, y, JV0 - 1, shutter('east'))

SIDE = {-3: DO, 1: DO, 4: DO, 7: DO}            # the right side, over the chimney
for v in range(JV0, XV1 + 1):
    for y in range(6, 10):
        b = SIDE.get(v) or ('glass_pane' if y in (7, 8) and v in (-1, 0, 5, 6) else '@plaster')
        d.set(JU0, y, v, b)
    d.set(JU0, 10, v, DOX)
for v in range(XV0, XV1 + 1):                   # the left side, toward the bridge
    for y in range(6, 10):
        b = DO if v in (0, 3) else 'glass_pane' if y in (7, 8) and v in (5, 6) else '@plaster'
        d.set(XU1, y, v, b)
    d.set(XU1, 10, v, DOX)
for y, half in ((6, 'lower'), (7, 'upper')):
    d.set(XU1, y, 1, 'dark_oak_door[facing=north,half=%s,hinge=left,open=false,powered=false]' % half)
for u in range(JU0, XU1 + 1):                   # the back
    for y in range(6, 10):
        b = DO if u in (-22, -16) else 'glass_pane' if y in (7, 8) and u in (-19, -18, -14, -13) else '@plaster'
        d.set(u, y, XV1, b)
    d.set(u, 10, XV1, DOZ)
for u in (-18, -14):                            # tie beams across the master's room
    for v in range(JV0 + 1, XV1):
        d.set(u, 10, v, DOX)
    d.set(u, 9, 2, HANG)

# ------------------------------------------------------------ the house: roof, dormer, turret

PS = [(0, 'slab'), (0, 'stair'), (1, 'stair'), (2, 'stair'), (4, 'stair'), (6, 'stair'), (7, 'block')]
house = d.roof(JV0 - 1, XV1 + 1, JU0 - 1, XU1 + 1, 11, PS, TILE, '@tile-block', along='u', verge=VERGE)
for u in (JU0, XU1):                            # the gables: plaster, a king post
    for v in range(JV0 + 1, XV1):
        for y in range(11, house[v][0]):
            d.set(u, y, v, SDO if v == 2 else '@plaster')
for u in range(JU0, XU1 + 1):
    d.set(u, 19, 2, 'cobbled_deepslate_wall')
d.set(XU1 + 1, 19, 2, 'lightning_rod[facing=up,powered=false]')

# The dormer over the middle window: the front wall carried up through the eave, its own gable.
for u in range(-18, -13):
    d.clear(u, 11, JV0 - 1)
dormer = d.roof(-19, -13, JV0 - 1, 0, 13, [(0, 'slab'), (0, 'stair'), (1, 'stair'), (2, 'block')],
                TILE, '@tile-block', along='v', verge=VERGE)
for u in range(-18, -13):
    for y in range(11, dormer[u][0]):
        d.set(u, y, JV0, DO if u in (-18, -14) else 'glass_pane' if y in (11, 12) else '@plaster')
for u in (-17, -16, -15):
    for v in (-2, -1):
        for y in (11, 12):
            d.clear(u, y, v)
d.set(-16, 16, JV0 - 1, 'lightning_rod[facing=up,powered=false]')

# The corner turret: a corbel of stairs, a timber body with windows, a spire.
TU_, TV_ = -23, -4
for du in (-1, 0, 1):
    for dv in (-1, 0, 1):
        u, v = TU_ + du, TV_ + dv
        d.set(u, 5, v, 'dark_oak_planks')
        d.set(u, 4, v, 'dark_oak_stairs[facing=%s,half=top]' % toward(du, dv) if du or dv else 'dark_oak_planks')
        if du or dv:
            for y in range(6, 14):
                if du and dv:
                    b = DO
                elif 8 <= y <= 10 and (dv == -1 or du == -1):
                    b = 'glass_pane'
                else:
                    b = '@plaster'
                d.set(u, y, v, b)
        else:
            for y in range(6, 14):
                d.set(u, y, v, 'air')
            d.set(u, 6, v, STAND)
d.set(TU_, 3, TV_, 'dark_oak_fence')
d.set(TU_, 2, TV_, HANG)
d.spire(TU_, TV_, 2, 14, [(0, 'stair'), (2, 'stair'), (3, 'block')], PLAIN, '@tile-block')
d.set(TU_, 18, TV_, 'cobbled_deepslate_wall')
d.set(TU_, 19, TV_, 'lightning_rod[facing=up,powered=false]')

# The chimney on the right gable: a breast with its fireplace, a stack, a corbelled crown.
for u in (-24, -23, -22):
    for v in (1, 2, 3, 4):
        for y in range(0, 5):
            d.set(u, y, v, stone(u, y, v))
for u in (-24, -23):
    d.set(u, 5, 1, 'stone_brick_stairs[facing=east,half=bottom]')
    d.set(u, 5, 4, 'stone_brick_stairs[facing=west,half=bottom]')
    for v in (2, 3):
        for y in range(5, 20):
            d.set(u, y, v, '@stone' if y < 15 else '@soot-1')
        d.set(u, 20, v, LIT)
for u in range(-25, -21):
    for v in range(1, 5):
        if u in (-25, -22) or v in (1, 4):
            face = 'east' if v == 1 else 'west' if v == 4 else 'north' if u == -25 else 'south'
            d.set(u, 20, v, 'stone_brick_stairs[facing=%s,half=top]' % face)
            if u in (-25, -22) and v in (1, 4):
                d.set(u, 21, v, 'stone_brick_wall')
for v in (2, 3):
    for y in (1, 2):
        d.set(XU0, y, v, 'air')
        d.set(XU0 - 1, y, v, LIT if y == 1 else 'air')
    d.set(XU0, 3, v, 'stripped_dark_oak_log[axis=x]')
    d.set(XU0 + 1, 0, v, '@hearth')

# ------------------------------------------------------------ the house inside

for p, b in (((-15, 2, 3), 'bell[attachment=floor,facing=west,powered=false]'),
             ((-13, 2, 3), 'heavy_weighted_pressure_plate[power=0]'), ((-12, 2, 3), STAND),
             ((-11, 1, 4), 'barrel[facing=up,open=false]'),
             ((-11, 1, 5), 'chest[facing=west,type=single,waterlogged=false]'),
             ((-19, 1, 0), 'chipped_anvil[facing=north]'),
             ((-20, 1, 0), 'lightning_rod[facing=up,powered=false]'),
             ((-20, 1, 1), 'lightning_rod[facing=up,powered=false]'),
             ((-15, 4, 1), HANG), ((-18, 4, 4), HANG), ((-12, 4, 1), HANG)):
    d.set(*p, b)
for u in range(-16, -11):                        # the counter, faced with upside-down stairs
    d.set(u, 1, 3, 'dark_oak_stairs[facing=east,half=top]')
for v in (0, 1):
    d.set(-20, 3, v, 'tripwire_hook[facing=north,attached=false,powered=false]')
for u in range(-20, -14):                        # goods on a shelf along the back
    d.set(u, 1, 6, 'barrel[facing=west,open=false]')
    d.set(u, 2, 6, 'spruce_slab[type=top]')
for u, b in ((-20, STAND), (-19, 'iron_chain[axis=y]'), (-18, 'soul_lantern[hanging=false]'),
             (-17, 'bell[attachment=floor,facing=west,powered=false]'), (-16, STAND)):
    d.set(u, 3, 6, b)
for i, u in enumerate(range(-11, -15, -1)):      # the stairs up, rising toward -u
    for y in range(1, i + 1):
        d.set(u, y, 6, 'spruce_planks')
    d.set(u, i + 1, 6, 'spruce_stairs[facing=south,half=bottom]')
    d.clear(u, 5, 6)
    d.set(u, 6, 5, 'spruce_fence')
for p, b in (((-20, 6, 5), 'red_bed[part=foot,facing=east,occupied=false]'),
             ((-20, 6, 6), 'red_bed[part=head,facing=east,occupied=false]'),
             ((-21, 6, 6), 'chest[facing=west,type=single,waterlogged=false]'),
             ((-21, 6, 4), 'bookshelf'), ((-21, 7, 4), 'bookshelf'),
             ((-17, 6, 1), 'dark_oak_fence'), ((-17, 7, 1), 'dark_oak_pressure_plate[powered=false]'),
             ((-17, 6, 0), 'spruce_stairs[facing=west,half=bottom]'),
             ((-17, 6, 2), 'spruce_stairs[facing=east,half=bottom]'),
             ((-12, 6, -2), 'lectern[facing=west,has_book=false,powered=false]'),
             ((-12, 7, 5), STAND), ((-13, 6, 5), 'barrel[facing=up,open=false]')):
    d.set(*p, b)
for u in (-18, -17, -16):
    for v in (3, 4):
        d.set(u, 6, v, 'red_carpet')

# ------------------------------------------------------------ the bridge over the gate

for u in (-9, -8, -7):
    for v in (0, 1, 2, 3):
        d.set(u, 5, v, DOZ if v in (0, 3) else 'dark_oak_planks')
        for y in range(1, 5):
            d.set(u, y, v, 'air')
        d.set(u, 0, v, '@cobble')
for v in (0, 3):
    d.set(-9, 4, v, 'dark_oak_stairs[facing=south,half=top]')
    d.set(-7, 4, v, 'dark_oak_stairs[facing=north,half=top]')
    for y in range(6, 10):
        d.set(-9, y, v, DO)
        d.set(-7, y, v, DO)
        d.set(-8, y, v, 'glass_pane' if y in (7, 8) else '@plaster')
d.roof(-9, -7, -1, 4, 10, [(0, 'stair'), (2, 'block')], PLAIN, '@tile-block', along='v', verge=VERGE)
d.set(-8, 9, 1, HANG)
d.set(-8, 4, 1, HANG)

# ------------------------------------------------------------ the grandfather's tower

TU, TV = -9, 10


def tower_stone(u, y, v):
    """The tower's stone: rough at the foot, sooted darker toward the crown, the bands blurred."""
    t = y + (hash01('tower', u, y, v) - 0.5) * 3
    return '@plinth' if t < 2.5 else '@stone' if t < 12 else '@soot-1' if t < 17 else '@soot-2' if t < 21 else '@soot-3'


for du in range(-3, 4):
    for dv in range(-3, 4):
        u, v = TU + du, TV + dv
        if octo(du, dv, 3):
            for y in range(0, 9):
                d.set(u, y, v, tower_stone(u, y, v))
        if octo(du, dv, 2):
            for y in range(9, 26):
                d.set(u, y, v, tower_stone(u, y, v))
        elif octo(du, dv, 3):
            d.set(u, 9, v, 'stone_brick_stairs[facing=%s,half=bottom]' % toward(du, dv))
            d.set(u, 24, v, 'deepslate_brick_stairs[facing=%s,half=top]' % toward(du, dv))
            d.set(u, 25, v, '@soot-3')
            if (du + dv) % 2 == 0:
                d.set(u, 26, v, 'polished_blackstone_bricks')
for du in (-1, 0, 1):                            # the fire pit in the crown, campfires sunk in it
    for dv in (-1, 0, 1):
        if du == 0 or dv == 0:
            d.set(TU + du, 25, TV + dv, LIT)
# A water table round the foot where the ground is free; buttresses on the two open faces.
for du in range(-4, 5):
    for dv in range(-4, 5):
        u, v = TU + du, TV + dv
        near = any(octo(du + a, dv + b, 3) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if not octo(du, dv, 3) and near and d.get(u, 1, v) is None and u <= XU1 + 4 and (du, dv) != (0, -4):
            if not (-9 <= u <= -7 and 4 <= v <= 6) or v == 6:
                d.set(u, 1, v, 'stone_brick_stairs[facing=%s,half=bottom]' % toward(du, dv))
for (u, v), face in (((TU - 4, TV), 'north'), ((TU, TV + 4), 'west')):
    for y in range(0, 7):
        d.set(u, y, v, tower_stone(u, y, v))
    d.set(u, 7, v, 'stone_brick_stairs[facing=%s,half=bottom]' % face)
for (u, v), face in (((TU - 5, TV), 'north'), ((TU, TV + 5), 'west')):
    for y in range(0, 3):
        d.set(u, y, v, tower_stone(u, y, v))
    d.set(u, 3, v, 'stone_brick_stairs[facing=%s,half=bottom]' % face)
# The old smithy's room at the foot, its iron door to the court; slits up the tower.
for du in (-1, 0, 1):
    for dv in (-1, 0, 1):
        for y in (1, 2, 3):
            d.set(TU + du, y, TV + dv, 'air')
for y, half in ((1, 'lower'), (2, 'upper')):
    d.set(TU, y, TV - 3, 'iron_door[facing=west,half=%s,hinge=left,open=false,powered=false]' % half)
    d.set(TU, y, TV - 2, 'air')
d.set(TU, 3, TV - 3, 'chiseled_stone_bricks')
for u in (TU - 1, TU + 1):
    for y in (1, 2, 3):
        d.set(u, y, TV - 3, 'polished_andesite')
for p, b in (((TU, 1, TV), 'damaged_anvil[facing=north]'), ((TU - 1, 1, TV + 1), 'chest[facing=west,type=single,waterlogged=false]'),
             ((TU + 1, 3, TV + 1), 'cobweb'), ((TU - 1, 3, TV - 1), 'cobweb'), ((TU, 3, TV), HANG)):
    d.set(*p, b)
for (u, y, v), behind in (((TU, 5, TV - 3), (TU, 5, TV - 2)), ((TU, 6, TV - 3), (TU, 6, TV - 2)),
                          ((TU, 17, TV - 2), (TU, 17, TV - 1)), ((TU, 18, TV - 2), (TU, 18, TV - 1)),
                          ((TU - 2, 19, TV), (TU - 1, 19, TV)), ((TU - 2, 20, TV), (TU - 1, 20, TV)),
                          ((TU, 15, TV + 2), (TU, 15, TV + 1)), ((TU, 16, TV + 2), (TU, 16, TV + 1))):
    d.set(u, y, v, 'iron_bars')
    d.set(*behind, 'polished_blackstone')

# Moss where the old walls stay damp: the shaded face and the court's corner. (Not vines: vines grow
# on random ticks and would creep over the tower between resets.)
for (u, v), top in (((TU - 3, TV - 2), 7), ((TU - 3, TV - 1), 5), ((TU - 3, TV + 1), 6), ((TU - 3, TV + 2), 8),
                    ((TU + 2, TV - 3), 7)):
    for y in range(1, top + 1):
        if hash01('moss', u, y, v) < 0.75 - 0.06 * y:
            d.set(u, y, v, 'mossy_stone_bricks' if hash01('mossy', u, y, v) < 0.5 else 'mossy_cobblestone')

# The court behind the gate.
for u in (-9, -8, -7):
    for v in (4, 5, 6):
        d.set(u, 0, v, '@cobble')
d.set(-7, 1, 4, 'barrel[facing=up,open=false]')
d.set(-7, 2, 4, STAND)
d.set(-7, 1, 6, '@bush')

# ------------------------------------------------------------ water: the race, the wheel, the flume

for v in range(-7, 14):                          # the race beside the hall, to the pond
    for u in (8, 9, 10):
        d.set(u, -1, v, '@bank')
        d.set(u, 0, v, 'water[level=0]')
    if v >= -6:
        for u in (7, 11):
            d.set(u, -1, v, '@bank')
            d.set(u, 0, v, '@bank')
            d.set(u, 1, v, 'stone_brick_slab[type=bottom]')
for u in range(7, 12):
    for y in (-1, 0, 1):
        d.set(u, y, 14, '@bank')

WV, WY = 7, 6                                    # the wheel's hub; the axle runs along u through it


def bridge_line(t0, angle, steps):
    """A spoke from the hub outward as face-joined cells (dv, dy): no diagonal steps."""
    out, (pv, py) = [], (0, 0)
    for t in range(1, steps + 1):
        cv, cy = round(t * math.cos(angle)), round(t * math.sin(angle))
        if cv != pv and cy != py:
            out.append((cv, py))
        out.append((cv, cy))
        pv, py = cv, cy
    return out


for u in (8, 10):
    for dv in range(-7, 8):
        for dy in range(-7, 8):
            if 4.5 <= math.hypot(dv, dy) < 6.2:
                d.set(u, WY + dy, WV + dv, 'spruce_planks')
    for k in range(8):
        for dv, dy in bridge_line(0, k * math.pi / 4, 4):
            if math.hypot(dv, dy) < 4.5:
                d.set(u, WY + dy, WV + dv, 'spruce_fence')
    for dv, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        d.set(u, WY + dy, WV + dv, 'stripped_spruce_wood')
for k in range(16):
    a = k * math.pi / 8
    d.set(9, WY + round(5.3 * math.sin(a)), WV + round(5.3 * math.cos(a)), 'dark_oak_planks')
d.set(11, 1, WV, '@bank')
for y in range(2, 6):
    d.set(11, y, WV, DO)
d.set(11, 7, WV, STAND)

# The flume: a plank trough on trestles from the spring, a sluice board over the wheel's top.
for v in range(8, 28):
    for u in (8, 9, 10):
        d.set(u, 13, v, 'spruce_planks')
    d.set(8, 14, v, 'stripped_spruce_log[axis=x]')
    d.set(10, 14, v, 'stripped_spruce_log[axis=x]')
    d.set(9, 14, v, 'water[level=0]')
d.set(9, 14, 7, shutter('east'))
# The spring: a pool among rocks at the hill's top.
for u in range(7, 12):
    for v in range(27, 31):
        if 8 <= u <= 10 and 28 <= v <= 29:
            d.set(u, 13, v, 'mossy_cobblestone')
            d.set(u, 14, v, 'water[level=0]')
        elif not (8 <= u <= 10 and v == 27):
            for y in range(13, 15 + (hash01('spring', u, v) < 0.5)):
                d.set(u, y, v, 'mossy_cobblestone' if hash01('rock', u, y, v) < 0.5 else 'stone')

# The pond at the race's foot.
POND = {(u, v) for u in range(4, 19) for v in range(-17, -5)
        if ((u - 11) / 5.5) ** 2 + ((v + 11) / 4.5) ** 2 < 1 + (hash01('pond', u, v) - 0.5) * 0.3}
for u, v in POND:
    d.set(u, -1, v, 'mud' if hash01('bed', u, v) < 0.6 else 'gravel')
    d.set(u, 0, v, 'water[level=0]')
    if hash01('lily', u, v) < 0.1:
        d.set(u, 1, v, 'lily_pad')
for u in range(3, 20):
    for v in range(-18, -4):
        if (u, v) in POND or d.get(u, 0, v) is not None:
            continue
        if any((u + a, v + b) in POND for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            k = hash01('shore', u, v)
            d.set(u, 0, v, 'coarse_dirt' if k < 0.4 else 'gravel' if k < 0.6 else 'mossy_cobblestone' if k < 0.7 else 'grass_block[snowy=false]')
            if k < 0.25:
                d.set(u, 1, v, 'sugar_cane[age=0]')
                d.set(u, 2, v, 'sugar_cane[age=0]')

# ------------------------------------------------------------ the yard

# The guild sign over the path: an anvil on a dark oak arm above a hanging sign, a lantern on the post.
for y in range(1, 6):
    d.set(3, y, -11, DO)
for u in (1, 2):
    d.set(u, 5, -11, DOZ)
d.set(1, 6, -11, 'anvil[facing=north]')
d.set(1, 4, -11, 'dark_oak_hanging_sign[attached=false,rotation=4,waterlogged=false]')
d.set(3, 6, -11, STAND)
d.set(4, 1, -11, 'stone_brick_stairs[facing=south,half=bottom]')
for u, v in ((-3, -17), (3, -4), (-4, -6)):      # lantern posts
    d.set(u, 1, v, 'cobblestone_wall')
    d.set(u, 2, v, 'dark_oak_fence')
    d.set(u, 3, v, STAND)

# The farrier's stocks before the house, a trough and a hitching rail, hay.
for u in (-20, -17):
    for v in (-8, -6):
        for y in (1, 2):
            d.set(u, y, v, DO)
for u in range(-20, -16):
    d.set(u, 3, -8, DOZ)
    d.set(u, 3, -6, DOZ)
d.set(-20, 3, -7, DOX)
d.set(-17, 3, -7, DOX)
for u in (-19, -18):
    d.set(u, 2, -8, 'iron_chain[axis=y]')
d.set(-21, 2, -6, STAND)
d.set(-21, 1, -6, 'dark_oak_fence')
d.set(-22, 1, -9, 'hay_block[axis=y]')
d.set(-22, 1, -8, 'hay_block[axis=x]')
d.set(-22, 2, -9, 'hay_block[axis=y]')
for u in range(-14, -10):
    for v in (-8, -7, -6):
        d.set(u, 0, v, 'stone_bricks')
        d.set(u, 1, v, 'water[level=0]' if v == -7 and -13 <= u <= -12 else 'stone_bricks')
for u in (-14, -13, -12, -11):
    d.set(u, 1, -10, 'dark_oak_fence')
d.set(-14, 2, -10, 'dark_oak_fence')
d.set(-11, 2, -10, 'dark_oak_fence')
d.set(-17, 1, -11, 'anvil[facing=east]')
d.set(-16, 1, -11, 'water_cauldron[level=3]')

# The ore wagon by the path, a wheel off.
for u in (-7, -6, -5):
    for v in (-15, -14, -13, -12):
        d.set(u, 1, v, 'spruce_slab[type=top]')
for v in (-15, -12):
    d.set(-8, 1, v, shutter('north'))
d.set(-4, 1, -12, shutter('south'))
d.set(-3, 1, -14, 'spruce_trapdoor[facing=north,half=bottom,open=false]')   # the wheel off, lying by it
for u in (-7, -5):
    d.set(u, 1, -16, 'dark_oak_fence')
for p, b in (((-6, 2, -14), 'raw_iron_block'), ((-7, 2, -13), 'raw_iron_block'), ((-5, 2, -13), 'coal_block'),
             ((-6, 2, -12), 'barrel[facing=up,open=true]'), ((-6, 3, -14), 'raw_iron_block')):
    d.set(*p, b)

# The charcoal clamp: an earth dome over stacked wood, smoking from its top and a side vent.
CU, CV = 16, 3
for du in range(-4, 5):
    for dv in range(-4, 5):
        r = math.hypot(du, dv)
        if r > 3.6:
            continue
        h = round(3.2 * math.sqrt(max(0.0, 1 - (r / 3.7) ** 2)) + (hash01('clamp', du, dv) - 0.5) * 0.6)
        for y in range(1, h + 1):
            d.set(CU + du, y, CV + dv, '@clamp')
        if h >= 1 and r > 2.8 and hash01('billet', du, dv) < 0.35:
            d.set(CU + du, 1, CV + dv, '@logs')
d.set(CU, 3, CV, LIT)
d.set(CU - 2, 2, CV + 1, LIT)

# The woodshed beside the clamp it feeds: cordwood end-on under a pent roof on posts.
for u in (17, 21):
    for y in (1, 2, 3):
        d.set(u, y, 9, DO)
    for y in (1, 2, 3, 4):
        d.set(u, y, 13, DO)
for u in range(17, 22):
    for v in range(8, 14):
        d.set(u, 4 if v < 11 else 5, v, 'spruce_slab[type=%s]' % ('bottom' if v in (8, 11) else 'top'))
        if 18 <= u <= 20 and v >= 10:
            for y in (1, 2, 3):
                d.set(u, y, v, '@logs')
d.set(19, 1, 8, 'stripped_oak_log[axis=y]')       # the chopping block

# ------------------------------------------------------------ the ground: the hill, the yard, the path


def hill(u, v):
    """The hill: rising from behind the buildings, a knoll where the spring is, falling away at the ends."""
    h = min(9.0, 0.75 * (v - 10)) + 6 * math.exp(-((u - 10) ** 2 + (v - 28) ** 2) / 50)
    return h - 0.9 * max(0, -19 - u, u - 14) - 1.5 * max(0, v - 31)


def dug(u, v):
    """Where the hill is dug away to the yard: the hall and the wheel's pit."""
    return (-7 <= u <= 7 and v <= HV) or (7 <= u <= 12 and v <= 14)


def height(u, v):
    if dug(u, v):
        return 0
    h = round(hill(u, v) + (hash01('hill', u, v) - 0.5) * 0.8)
    return min(h, 12) if 7 <= u <= 11 and v <= 30 else h


SITE_U, SITE_V = range(-28, 23), range(-25, 37)
H = {(u, v): height(u, v) for u in SITE_U for v in SITE_V}
for (u, v), hh in H.items():
    if hh <= 0:
        continue
    nbs = [(u + a, v + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
    steep = max(hh - H.get(q, hh) for q in nbs)
    retain = any(dug(*q) for q in nbs) and hh >= 2
    for y in range(0, hh + 1):
        if d.get(u, y, v) is not None:
            continue
        if retain:
            b = '@retain' if y < hh else 'grass_block[snowy=false]'
        elif steep >= 3 or hash01('outcrop', u // 2, v // 2) < 0.04:
            b = '@hill-rock'
        else:
            b = '@earth' if y < hh else 'grass_block[snowy=false]'
        d.set(u, y, v, b)
    k = hash01('green', u, v)
    if d.get(u, hh + 1, v) is None and d.get(u, hh, v) == 'grass_block[snowy=false]':
        if k < 0.2:
            d.set(u, hh + 1, v, 'fern' if k < 0.07 else 'short_grass')
        elif k < 0.25:
            d.set(u, hh + 1, v, '@bush')
        elif k < 0.28:
            d.set(u, hh + 1, v, 'cornflower' if k < 0.265 else 'oxeye_daisy')

for v in (15, 19, 23):
    for u in (8, 10):
        for y in range(max(0, H[(u, v)]) + 1, 12):
            d.set(u, y, v, DO)
    for u in range(7, 12):
        d.set(u, 12, v, DOZ)

# The slag heap behind the house, on the slope.
for u in range(-20, -13):
    for v in range(9, 16):
        r = math.hypot((u + 16.5) / 1.3, v - 12)
        h = round(2.8 - 0.9 * r + hash01('slag', u, v) - 0.5)
        base = max(0, H.get((u, v), 0))
        for y in range(base + 1, base + h + 1):
            d.set(u, y, v, '@slag')


def oak(u0, v0):
    y0 = max(0, H.get((u0, v0), 0)) + 1
    for y in range(y0, y0 + 5):
        d.set(u0, y, v0, 'oak_log[axis=y]')
    for du in range(-3, 4):
        for dv in range(-3, 4):
            for dy in range(-1, 3):
                r = math.sqrt(du * du + dv * dv + (1.5 * dy) ** 2)
                p = (u0 + du, y0 + 4 + dy, v0 + dv)
                if r < 3.3 - 0.9 * hash01('leaf', *p) and d.get(*p) is None:
                    d.set(*p, 'oak_leaves[persistent=true]')


def spruce(u0, v0, tall=9):
    y0 = max(0, H.get((u0, v0), 0)) + 1
    for y in range(y0, y0 + tall):
        d.set(u0, y, v0, 'spruce_log[axis=y]')
    for i in range(2, tall + 1):
        r = 0.6 + 2.4 * (1 - i / tall) + (0.6 if i % 2 else 0)
        for du in range(-3, 4):
            for dv in range(-3, 4):
                p = (u0 + du, y0 + i, v0 + dv)
                if math.hypot(du, dv) <= r and d.get(*p) is None:
                    d.set(*p, 'spruce_leaves[persistent=true]')


oak(18, -12)
spruce(-17, 21)
spruce(-23, 18, 7)
spruce(19, 24, 8)

# The yard's ground: cobbles before the hall, a worn path in from the gate, beaten earth before the
# house and round the clamp, grass beyond.
PATH = {(u, v) for v in range(-25, -9) for u in range(-2, 3) if abs(u) <= 1 or hash01('path', u, v) > 0.55}
for u in SITE_U:
    for v in SITE_V:
        if d.get(u, 0, v) is not None:
            continue
        k = hash01('yard', u, v)
        if (u, v) in PATH:
            d.set(u, 0, v, '@path')
        elif -9 <= u <= 6 and -10 <= v <= -1 and (k < 0.9 or -6 <= u <= 5):
            d.set(u, 0, v, '@cobble')
        elif (-24 <= u <= -10 and -12 <= v <= -4 or 12 <= u <= 20 and -2 <= v <= 8) and k < 0.75:
            d.set(u, 0, v, '@skirt')
        else:
            d.set(u, 0, v, 'grass_block[snowy=false]')
            g = hash01('grass', u, v)
            if d.get(u, 1, v) is None and g < 0.16:
                d.set(u, 1, v, 'short_grass' if g < 0.11 else 'fern' if g < 0.13 else 'dandelion' if g < 0.145 else 'poppy')
for p in ((HU + 1, 1, 2), (-HU - 1, 1, 7), (XU0 - 1, 1, 6), (-10, 1, -3), (XU0 - 2, 1, -2), (-HU, 1, -2)):
    if d.get(*p) is None:
        d.set(*p, '@bush')
for p, b in (((-21, 1, -3), 'red_tulip'), ((-9, 1, -3), 'allium'), ((HU, 1, -2), 'cornflower')):
    if d.get(*p) is None:
        d.set(*p, b)


if __name__ == '__main__':
    import look
    import schem
    blocks = look.connect(look.resolve(d))
    floors = [('hall', [(u, 1, v) for u in range(-5, 6) for v in range(2, HV)]),
              ('gallery', [(u, 6, v) for u in range(-5, -2) for v in range(2, 8)]),
              ('bridge', [(u, 6, v) for u in range(-9, -6) for v in (1, 2)]),
              ('house', [(u, 1, v) for u in range(XU0 + 1, XU1) for v in range(0, XV1)]),
              ('master room', [(u, 6, v) for u in range(XU0, XU1) for v in range(JV0 + 1, XV1)]),
              ('tower room', [(u, 1, v) for u in (TU - 1, TU, TU + 1) for v in (TV - 1, TV, TV + 1)])]
    good = look.check(blocks, GATE, floors)
    if len(sys.argv) > 1:
        print(look.render(look.Volume(blocks), sys.argv[1]))
        print(look.close(blocks, sys.argv[1] + '-hall', (-10, 14, -10, 18)))
        print(look.close(blocks, sys.argv[1] + '-house', (-27, -5, -12, 12)))
    schem.write(blocks, os.path.join(HERE, 'forge_legendary.schem'), GATE)
    print('good' if good else 'NOT GOOD')
