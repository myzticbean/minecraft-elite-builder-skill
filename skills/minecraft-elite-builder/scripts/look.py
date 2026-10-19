"""Looking at a drawing before it goes in game: concrete blocks, renders Claude can read, and checks.

A drawing's cells (``draw.Drawing``) become concrete blocks here: a palette reference
``@key[props]`` takes one block of its mix at that position, in patches about two blocks
across. Then:

- ``render(blocks, path)`` writes PNGs: isometric views from the four corners, the four flat
  elevations, the plan from above. Plain cubes coloured by name, no textures.
- ``check(blocks, start)`` prints the facts a review needs: blocks not joined to the ground, covered
  cells dark enough for a mob, where a player can walk from ``start``, which floors they can't reach.

Needs numpy only; PNGs are written with zlib.
"""
import re
import struct
import zlib
from collections import deque

import numpy as np

from draw import hash01

# ------------------------------------------------------------ concrete blocks

MIX = re.compile(r"(\d+)%(.+)")


def parse_mix(mix):
    """``'75%a,25%b[x=y]'`` or ``'a:3,b:1'`` -> [(block, weight)], commas inside [] kept."""
    out = []
    for part in re.split(r",(?![^\[]*])", mix):
        part = part.strip()
        m = MIX.match(part)
        if m:
            out.append((m.group(2), int(m.group(1))))
        elif re.search(r":\d+$", part):
            b, w = part.rsplit(':', 1)
            out.append((b, int(w)))
        else:
            out.append((part, 1))
    return out


def add_props(block, props):
    """``spruce_stairs`` + ``facing=west`` -> ``spruce_stairs[facing=west]``; the mix's own props stay."""
    if not props:
        return block
    if '[' in block:
        return block[:-1] + ',' + props + ']'
    return block + '[' + props + ']'


def resolve(d):
    """The drawing as {(u, y, v): block id or 'air'}, palette references picked by position."""
    mixes = {k: parse_mix(m) for k, m in d.palettes.items()}
    out = {}
    for (u, y, v), (block, _loose) in d.cells.items():
        if block is None:
            continue
        if block.startswith('@'):
            m = re.match(r"@([\w-]+)(?:\[(.*)])?$", block)
            key, props = m.group(1), m.group(2)
            mix = mixes[key]
            # Patches about two blocks across, with a speckle on top .
            h = hash01(key, u // 2, y // 2, v // 2) if hash01('patch', key, u, y, v) < 0.7 else hash01(key, u, y, v)
            total = sum(w for _, w in mix)
            pick = h * total
            chosen = mix[-1][0]
            for b, w in mix:
                pick -= w
                if pick < 0:
                    chosen = b
                    break
            block = add_props(chosen, props)
        out[(u, y, v)] = block
    return out


def base(block):
    return block.split('[', 1)[0].removeprefix('minecraft:')


# ------------------------------------------------------------ what a block is, roughly

AIRS = {'air', 'cave_air', 'void_air'}
# A player walks through these (no collision, or a door they open).
PASS_WORDS = ('_door', 'ladder', 'vine', 'torch', 'button', 'pressure_plate', 'sign', 'banner',
              'short_grass', 'tall_grass', 'fern', 'petals', 'sunflower', 'wildflowers', 'tulip', 'allium', 'poppy',
              'dandelion', 'orchid', 'daisy', 'cornflower', 'lily_of_the_valley', 'torchflower',
              'rose_bush', 'lilac', 'peony', 'sapling', 'carpet', 'cobweb', 'leaf_litter', 'lever',
              'rail', 'redstone_wire', 'hanging_roots', 'glow_lichen', 'dead_bush', 'bush')
# These don't hold a block up: hanging, thin or soft things.
FLOAT_OK = ('lantern', 'chain', 'vine', 'ladder', 'button', 'sign', 'banner', 'cobweb', 'roots',
            'leaves', 'trapdoor', 'torch')


def passable(block):
    b = base(block)
    if b in AIRS:
        return True
    if b.endswith(('_trapdoor', '_fence_gate')) and 'open=true' in block:
        return True
    return any(w in b for w in PASS_WORDS)


def standable(block):
    """Can a player stand on top of it? (Fences and walls are 1.5 high: no.)"""
    b = base(block)
    if passable(block) or b.endswith(('_fence', '_wall', '_fence_gate')) or b in ('lantern', 'iron_chain'):
        return False
    if b.endswith('_trapdoor') and 'open=true' in block:
        return False
    return True


# ------------------------------------------------------------ colour by name
# Rough colours, most of them the average of the game's own texture (26.2), tinted with the default
# biome colours where the game tints them (water, leaves, grass).

DYES = {"white": (234, 236, 237), "orange": (241, 118, 20), "magenta": (190, 69, 180),
        "light_blue": (58, 175, 217), "yellow": (249, 198, 40), "lime": (112, 185, 26),
        "pink": (238, 141, 172), "gray": (63, 68, 72), "light_gray": (142, 142, 135),
        "cyan": (21, 138, 145), "purple": (122, 42, 173), "blue": (53, 57, 157),
        "brown": (114, 72, 41), "green": (85, 110, 28), "red": (161, 39, 35),
        "black": (21, 21, 26)}
FAMILIES = [("tinted_glass", (60, 50, 70)), ("glass", (150, 200, 210)), ("water", (44, 82, 158)),
            ("lava", (217, 105, 26)), ("snow", (249, 254, 254)), ("quartz", (236, 230, 223)),
            ("calcite", (220, 222, 210)), ("diorite", (200, 200, 196)), ("andesite", (136, 137, 136)),
            ("granite", (150, 106, 89)), ("tuff", (108, 109, 100)), ("sandstone", (216, 203, 156)),
            ("sand", (219, 207, 163)), ("deepslate", (80, 80, 83)), ("blackstone", (48, 44, 56)),
            ("coal", (25, 25, 28)), ("obsidian", (15, 11, 25)), ("copper", (192, 108, 80)),
            ("iron", (220, 220, 220)), ("gold", (246, 208, 62)), ("amethyst", (134, 98, 191)),
            ("froglight", (240, 220, 230)), ("azalea_leaves", (101, 140, 52)), ("leaves", (67, 97, 27)),
            ("stripped_spruce", (150, 112, 70)), ("spruce_log", (70, 52, 33)), ("spruce", (115, 85, 49)),
            ("stripped_dark_oak", (96, 76, 50)), ("dark_oak", (66, 46, 28)), ("stripped_birch", (200, 186, 140)),
            ("birch", (192, 175, 121)), ("cherry", (227, 179, 173)), ("oak", (162, 131, 79)),
            ("bookshelf", (120, 90, 60)), ("barrel", (120, 88, 52)), ("chest", (150, 110, 50)),
            ("moss", (89, 115, 44)), ("grass_block", (84, 109, 51)), ("short_grass", (90, 140, 60)),
            ("fern", (80, 125, 55)), ("coarse_dirt", (118, 85, 60)), ("podzol", (92, 64, 30)),
            ("dirt", (134, 96, 67)), ("gravel", (128, 122, 118)), ("mud", (60, 57, 61)),
            ("cobblestone", (120, 120, 120)), ("mossy", (110, 128, 96)), ("cracked", (128, 128, 126)),
            ("stone", (126, 126, 126)), ("brick", (151, 98, 83)), ("lantern", (250, 200, 90)),
            ("candle", (240, 220, 160)), ("campfire", (230, 120, 40)), ("cauldron", (60, 60, 64)),
            ("brewing", (180, 170, 120)), ("ladder", (160, 120, 70)), ("vine", (60, 110, 40)),
            ("cobweb", (235, 235, 235)), ("chain", (60, 64, 70)), ("torchflower", (230, 150, 60)),
            ("allium", (170, 110, 210)), ("petals", (240, 170, 200))]


def colour(block):
    name = base(block)
    if name in AIRS:
        return None
    if name.startswith('stripped_') and 'spruce' in name:
        return (150, 112, 70)
    for dye in sorted(DYES, key=len, reverse=True):
        if name.startswith(dye + '_'):
            return DYES[dye]
    for frag, c in FAMILIES:
        if frag in name:
            return c
    h = hash01('colour', name)
    return (int(110 + 60 * h), int(110 + 40 * h), int(100 + 30 * h))


# ------------------------------------------------------------ a volume

class Volume:
    """The blocks as a dense grid indexed [y, v, u] (offset to start at 0): x runs along u (+x is
    the front's left), z along v (into the hill), y up."""

    def __init__(self, blocks):
        us = [p[0] for p in blocks]
        ys = [p[1] for p in blocks]
        vs = [p[2] for p in blocks]
        self.u0, self.y0, self.v0 = min(us), min(ys), min(vs)
        self.shape = (max(ys) - self.y0 + 1, max(vs) - self.v0 + 1, max(us) - self.u0 + 1)
        self.palette = ['air']
        index = {'air': 0}
        self.grid = np.zeros(self.shape, dtype=np.int32)
        for (u, y, v), b in blocks.items():
            if b not in index:
                index[b] = len(self.palette)
                self.palette.append(b)
            self.grid[y - self.y0, v - self.v0, u - self.u0] = index[b]

    def cell(self, u, y, v):
        return (y - self.y0, v - self.v0, u - self.u0)

    def at(self, u, y, v):
        i = self.cell(u, y, v)
        if any(k < 0 or k >= s for k, s in zip(i, self.shape)):
            return 'air'
        return self.palette[self.grid[i]]


# ------------------------------------------------------------ PNG without Pillow

def write_png(path, rgb):
    h, w, _ = rgb.shape
    raw = b''.join(b'\x00' + rgb[r].astype(np.uint8).tobytes() for r in range(h))

    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
                + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


BG = np.array((22, 30, 38), dtype=np.uint8)


def _iso_masks(s):
    """Masks of a cube's three visible faces (top, the face toward +x, the face toward +z) in a
    (2s+1) x (2s+1) tile; the cube's corner (x, y+1, z) projects to the tile's top middle."""
    size = 2 * s + 1
    yy, xx = np.mgrid[0:size, 0:size].astype(float) + 0.5
    cx = s

    def inside(poly):
        m = np.zeros((size, size), bool)
        n = len(poly)
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            cond = ((y1 > yy) != (y2 > yy)) & (xx < (x2 - x1) * (yy - y1) / (y2 - y1 + 1e-9) + x1)
            m ^= cond
        return m
    # Projection: screen x = (x - z) * s, screen y = ((x + z) / 2 - y) * s, relative to (x, y+1, z).
    top = [(cx, 0), (cx + s, s / 2), (cx, s), (cx - s, s / 2)]
    east = [(cx, s), (cx + s, s / 2), (cx + s, 1.5 * s), (cx, 2 * s)]     # the +x face
    south = [(cx - s, s / 2), (cx, s), (cx, 2 * s), (cx - s, 1.5 * s)]    # the +z face
    return inside(top), inside(east), inside(south)


def _turn(grid, k):
    """Turn the [y, z, x] grid a quarter k times about y, so each corner in turn faces +x +z."""
    return np.rot90(grid, k, axes=(1, 2))


def iso(vol, corner=0, s=8):
    """An isometric view from above one corner; corner 0..3 turns the house a quarter each."""
    grid = _turn(vol.grid, corner)
    solid_t = np.array([colour(b) is not None for b in vol.palette])
    cols = np.array([colour(b) or (0, 0, 0) for b in vol.palette], float)
    solid = solid_t[grid]
    H, Z, X = solid.shape
    top = solid & ~np.pad(solid[1:], ((0, 1), (0, 0), (0, 0)))
    east = solid & ~np.pad(solid[:, :, 1:], ((0, 0), (0, 0), (0, 1)))
    south = solid & ~np.pad(solid[:, 1:, :], ((0, 0), (0, 1), (0, 0)))
    W = (X + Z) * s + 4 * s
    Hh = int((X + Z) * s / 2 + H * s + 4 * s + 2)
    img = np.empty((Hh, W, 3), np.uint8)
    img[:] = BG
    mt, me, ms = _iso_masks(s)
    ox = Z * s + 2 * s
    oy = H * s + 2 * s
    cells = np.argwhere(top | east | south)
    order = np.lexsort((cells[:, 0], cells[:, 1] + cells[:, 2] + cells[:, 0]))
    for y, z, x in cells[order]:
        c = cols[grid[y, z, x]]
        px = int(ox + (x - z) * s - s)
        py = int(oy + ((x + z) / 2 - (y + 1)) * s)
        tile = img[py:py + 2 * s + 1, px:px + 2 * s + 1]
        for m, on, shade in ((ms, south[y, z, x], 0.62), (me, east[y, z, x], 0.80), (mt, top[y, z, x], 1.05)):
            if on:
                tile[m[:tile.shape[0], :tile.shape[1]]] = np.clip(c * shade, 0, 255)
    return img


def elevation(vol, side, s=10, depth=64):
    """A flat drawing of one side (front, back, left, right) or the plan (top): the first block met.

    front looks from -v (the path) with +u on the left; left looks from +u."""
    g = vol.grid
    solid_t = np.array([colour(b) is not None for b in vol.palette])
    cols = np.array([colour(b) or BG for b in vol.palette], float)
    H, Z, X = g.shape
    if side == 'top':
        rows, ncols = Z, X
    elif side in ('front', 'back'):
        rows, ncols = H, X
    else:
        rows, ncols = H, Z
    out = np.empty((rows, ncols, 3))
    out[:] = BG
    shade = np.ones((rows, ncols))
    for r in range(rows):
        for c in range(ncols):
            for k in range(depth):
                # Each as the viewer sees it, their left hand on the image's left.
                if side == 'top':                                  # the front at the bottom
                    y, z, x = H - 1 - k, Z - 1 - r, X - 1 - c
                elif side == 'front':                              # from the path: +u on the left
                    y, z, x = H - 1 - r, k, X - 1 - c
                elif side == 'back':                               # from the hill: -u on the left
                    y, z, x = H - 1 - r, Z - 1 - k, c
                elif side == 'left':                               # from +u: the back on the left
                    y, z, x = H - 1 - r, Z - 1 - c, X - 1 - k
                else:                                              # from -u: the front on the left
                    y, z, x = H - 1 - r, c, k
                if not (0 <= y < H and 0 <= z < Z and 0 <= x < X):
                    break
                i = g[y, z, x]
                if solid_t[i]:
                    out[r, c] = cols[i]
                    shade[r, c] = max(0.45, 1 - 0.09 * k)     # deeper reads darker: planes show
                    break
    img = (out * shade[:, :, None]).clip(0, 255).astype(np.uint8)
    img = img.repeat(s, 0).repeat(s, 1)
    img[::s, :] = (img[::s, :] * 0.8).astype(np.uint8)        # a faint block grid
    img[:, ::s] = (img[:, ::s] * 0.8).astype(np.uint8)
    return img


def sheet(images, gap=12):
    """Images side by side on one sheet."""
    h = max(i.shape[0] for i in images)
    w = sum(i.shape[1] for i in images) + gap * (len(images) - 1)
    out = np.empty((h, w, 3), np.uint8)
    out[:] = BG
    x = 0
    for i in images:
        out[h - i.shape[0]:, x:x + i.shape[1]] = i
        x += i.shape[1] + gap
    return out


# ------------------------------------------------------------ sub-block shapes

# Which way a facing points in a cell's [y, v, u] sub-grid: (axis, high side?). North is +u, east +v.
_SIDE = {'north': (2, True), 'south': (2, False), 'east': (1, True), 'west': (1, False)}
_SMALL = ('lantern', 'candle', 'flower_pot', 'potted_', '_cluster', '_bud', 'bell', 'brewing_stand',
          'heavy_core', '_head', '_skull', 'sea_pickle', 'turtle_egg', 'torch', 'grindstone')
_PLANTS = ('short_grass', 'fern', 'flower', 'tulip', 'allium', 'bluet', 'orchid', 'daisy', 'poppy',
           'dandelion', 'cornflower', 'lily_of_the_valley', 'torchflower', 'sapling', 'roots',
           'cave_vines', 'dead_bush', 'cobweb', 'sugar_cane', 'sweet_berry_bush', 'wildflowers',
           'sunflower', 'lilac', 'peony', 'rose_bush', 'tall_grass', 'large_fern', 'pitcher')
_FLAT = ('carpet', 'pressure_plate', 'lily_pad', 'snow', 'petals', 'leaf_litter', 'rail',
         'redstone_wire', 'glow_lichen')


def _half(m, n, direction, sl=slice(None)):
    """Mark the half of the cell toward ``direction`` (within the y slice ``sl``)."""
    axis, high = _SIDE[direction]
    cut = slice(n // 2, n) if high else slice(0, n // 2)
    idx = [sl, slice(None), slice(None)]
    idx[axis] = cut
    m[tuple(idx)] = True


def _plate(m, n, direction, ys=slice(None), thick=1):
    """A plate ``thick`` sub-cells deep on the cell's ``direction`` face."""
    axis, high = _SIDE[direction]
    idx = [ys, slice(None), slice(None)]
    idx[axis] = slice(n - thick, n) if high else slice(0, thick)
    m[tuple(idx)] = True


def _arm(m, n, direction, ys, w):
    """A bar from the cell's middle out to its ``direction`` face, ``w`` wide, in the y slice."""
    axis, high = _SIDE[direction]
    idx = [ys, w, w]
    idx[axis] = slice(n // 2 - 1, n) if high else slice(0, n // 2 + 1)
    m[tuple(idx)] = True


def shape(block, n=4):
    """The block's rough shape as a boolean [y, v, u] grid of n sub-cells a side, or None for a full
    cube: stairs, slabs, panes, fences, walls, trapdoors, doors and the small things, so a render
    shows a roof's profile and a window's depth, not a pile of cubes."""
    name, props = split(base(block) + (block[block.index('['):] if '[' in block else ''))
    m = np.zeros((n, n, n), bool)
    lo, hi, mid = slice(0, n // 2), slice(n // 2, n), slice(n // 2 - 1, n // 2 + 1)
    if name in AIRS or name == 'light':
        return m
    if name.endswith('_slab'):
        t = props.get('type', 'bottom')
        if t == 'double':
            return None
        m[lo if t == 'bottom' else hi] = True
        return m
    if name.endswith('_stairs'):
        top = props.get('half') == 'top'
        m[hi if top else lo] = True
        f, s = props.get('facing', 'north'), props.get('shape', 'straight')
        ys = lo if top else hi
        side = CCW[f] if s.endswith('left') else OPP[CCW[f]]
        if s.startswith('outer'):
            q = np.zeros_like(m)
            _half(q, n, f, ys)
            r = np.zeros_like(m)
            _half(r, n, side, ys)
            m |= q & r
        else:
            _half(m, n, f, ys)
            if s.startswith('inner'):
                _half(m, n, side, ys)
        return m
    fam = _family(name)
    if fam:
        post = slice(n // 2 - 1, n // 2 + 1) if fam != 'pane' else mid
        m[:, post, post] = True
        for dname in DIRS:
            c = props.get(dname, 'false')
            if c in ('false', 'none'):
                continue
            if fam == 'pane':
                _arm(m, n, dname, slice(None), mid)
            elif fam == 'wall':
                _arm(m, n, dname, slice(None) if c == 'tall' else slice(0, n - 1), mid)
            else:
                _arm(m, n, dname, slice(1, n), slice(n // 2 - 1, n // 2))
        return m
    if name.endswith('_fence_gate'):
        f = props.get('facing', 'north')
        axis = _SIDE[f][0]
        idx = [slice(1, n), slice(None), slice(None)]
        idx[axis] = mid
        m[tuple(idx)] = True
        return m
    if name.endswith('_trapdoor'):
        if props.get('open') == 'true':
            _plate(m, n, OPP[props.get('facing', 'north')])
        else:
            m[(0 if props.get('half', 'bottom') == 'bottom' else n - 1)] = True
        return m
    if name.endswith('_door') or name == 'ladder' or name.endswith(('_wall_sign', '_wall_banner')) \
            or name in ('tripwire_hook',) or (name.endswith('_button') and props.get('face') == 'wall'):
        f = props.get('facing', 'north')
        if name.endswith('_button') or name == 'tripwire_hook':
            axis, high = _SIDE[OPP[f]]
            idx = [mid, mid, mid]
            idx[axis] = slice(n - 1, n) if high else slice(0, 1)
            m[tuple(idx)] = True
        else:
            ys = slice(1, n - 1) if name.endswith('_wall_sign') else slice(None)
            _plate(m, n, OPP[f], ys)
        return m
    if name in ('chain', 'iron_chain') or name.endswith(('_chain', 'lightning_rod', 'end_rod')):
        a = props.get('axis') or {'up': 'y', 'down': 'y', 'north': 'z', 'south': 'z',
                                   'east': 'x', 'west': 'x'}.get(props.get('facing', 'up'), 'y')
        c = slice(n // 2, n // 2 + 1)
        m[(slice(None), c, c) if a == 'y' else (c, slice(None), c) if a == 'x' else (c, c, slice(None))] = True
        return m
    if name in ('campfire', 'soul_campfire') or name.endswith('_bed') or name in ('daylight_detector', 'stonecutter'):
        m[0:max(1, n // 2)] = True
        return m
    if any(w in name for w in _FLAT):
        m[0] = True
        return m
    if name.endswith('_hanging_sign'):
        m[1:n, mid, :] = True
        return m
    if any(w in name for w in _SMALL):
        ys = slice(1, n - 1) if props.get('hanging') == 'true' else slice(0, n // 2)
        m[ys, mid, mid] = True
        return m
    if any(w in name for w in _PLANTS) or name == 'vine':
        m[0:n - 1, mid, mid] = True
        return m
    return None


def fine(vol, n=4):
    """The volume cut to n sub-cells a block, each block in its rough shape (``shape``)."""
    masks = [shape(b, n) for b in vol.palette]
    whole = np.array([m is None for m in masks])
    g = (vol.grid * whole[vol.grid]).repeat(n, 0).repeat(n, 1).repeat(n, 2)
    for i, m in enumerate(masks):
        if m is None or not m.any():
            continue
        for y, v, u in np.argwhere(vol.grid == i):
            g[y * n:(y + 1) * n, v * n:(v + 1) * n, u * n:(u + 1) * n][m] = i
    out = Volume.__new__(Volume)
    out.__dict__.update(vol.__dict__)
    out.grid = g
    return out


def close(blocks, prefix, box, corners=(3, 2), n=4, s=24):
    """Close isometric views of the drawing cropped to box (u0, u1, v0, v1), in true sub-block
    shapes: prefix-close<corner>.png, corner 3 the front left, 2 the front right."""
    u0, u1, v0, v1 = box
    vol = fine(Volume({p: b for p, b in blocks.items() if u0 <= p[0] <= u1 and v0 <= p[2] <= v1}), n)
    paths = []
    for k in corners:
        p = '%s-close%d.png' % (prefix, k)
        write_png(p, iso(vol, k, s=max(2, s // n)))
        paths.append(p)
    return paths


def render(vol, prefix, n=4):
    """prefix-hero.png (big, from the front left, the angle of a reference shot), prefix-iso.png
    (the other three corners: front right, back right, back left), prefix-sides.png (front, left,
    back, right), prefix-top.png. The isometric views are in sub-block shapes (``fine``)."""
    paths = []
    sub = fine(vol, n) if n > 1 else vol
    for name, img in (('hero', iso(sub, 3, s=max(2, 16 // n))),
                      ('iso', sheet([iso(sub, k, s=max(2, 10 // n)) for k in (2, 1, 0)])),
                      ('sides', sheet([elevation(vol, s) for s in ('front', 'left', 'back', 'right')])),
                      ('top', elevation(vol, 'top'))):
        p = '%s-%s.png' % (prefix, name)
        write_png(p, img)
        paths.append(p)
    return paths


# ------------------------------------------------------------ checks

N6 = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def floating(blocks, ground_y=0):
    """Blocks not joined, face to face, to the ground (y <= ground_y), hanging things aside."""
    solid = {p for p, b in blocks.items() if base(b) not in AIRS}
    seen = {p for p in solid if p[1] <= ground_y}
    todo = deque(seen)
    while todo:
        u, y, v = todo.popleft()
        for du, dy, dv in N6:
            q = (u + du, y + dy, v + dv)
            if q in solid and q not in seen:
                seen.add(q)
                todo.append(q)
    return sorted(p for p in solid - seen if not any(w in base(blocks[p]) for w in FLOAT_OK))


def walk(blocks, start, ground_y=-1):
    """Every cell a player's feet can reach from start: 2-high clearance, a standable block
    below (or the ground under the drawing), up 1 by a jump, down any drop to 3, ladders climb."""
    def b(p):
        if p[1] <= ground_y:
            return 'stone'
        return blocks.get(p, 'air')

    def ok(p):
        return passable(b(p)) and passable(b((p[0], p[1] + 1, p[2])))

    def floor(p):
        below = b((p[0], p[1] - 1, p[2]))
        return standable(below) or 'ladder' in base(b(p))

    lo = [min(p[i] for p in blocks) - 1 for i in range(3)]   # a block past the drawing, no further:
    hi = [max(p[i] for p in blocks) + 1 for i in range(3)]   # the ground beyond it is endless
    seen = {start}
    todo = deque([start])
    while todo:
        u, y, v = todo.popleft()
        if not all(lo[i] <= (u, y, v)[i] <= hi[i] for i in range(3)):
            continue
        steps = []
        for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for dy in (1, 0, -1, -2, -3):
                steps.append((u + du, y + dy, v + dv, dy))
        if 'ladder' in base(b((u, y, v))) or 'ladder' in base(b((u, y + 1, v))):
            steps += [(u, y + 1, v, 1), (u, y - 1, v, -1)]
        for nu, ny, nv, dy in steps:
            q = (nu, ny, nv)
            if q in seen or not ok(q) or not floor(q):
                continue
            if dy == 1 and not passable(b((u, y + 2, v))):
                continue                                   # no headroom to jump
            if dy < 0 and not all(passable(b((nu, y - k, nv))) for k in range(0, -dy)):
                continue
            seen.add(q)
            todo.append(q)
    return seen


# ------------------------------------------------------------ states a paste doesn't work out

# A schematic is pasted as written: no neighbour updates. So panes, bars, fences and walls carry
# their connections, and stairs their corner shapes, or they stand as bare posts and straight runs.
# Directions in the drawing's frame: north is +u, east is +v (draw.py).
DIRS = {'north': (1, 0), 'south': (-1, 0), 'east': (0, 1), 'west': (0, -1)}
OPP = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
CCW = {'north': 'west', 'east': 'north', 'south': 'east', 'west': 'south'}
NOT_FULL = ('_slab', '_stairs', '_fence', '_fence_gate', '_wall', '_pane', '_bars', '_trapdoor', 'lantern',
            '_chain', 'campfire', 'cauldron', 'brewing_stand', '_bed', 'chest', 'lectern', 'anvil',
            'grindstone', 'bell', 'hopper', '_head', '_skull', 'scaffolding', 'snow', 'dirt_path',
            'farmland', '_rod', 'dripstone', 'composter', 'enchanting_table', 'stonecutter', 'candle',
            'cake', 'cactus', 'bamboo', '_cluster', '_bud', 'flower_pot', 'conduit', 'daylight_detector')


def split(block):
    name, _, rest = block.partition('[')
    return name, dict(kv.split('=') for kv in rest.rstrip(']').split(',') if kv)


def join(name, props):
    return name + ('[' + ','.join('%s=%s' % kv for kv in props.items()) + ']' if props else '')


def full(block):
    """A block whose sides are whole: panes, fences and walls join it, ladders hang on it."""
    b = base(block)
    return not passable(block) and not b.startswith('potted_') and not b.endswith(NOT_FULL)


def _family(b):
    if b.endswith('_pane') or b == 'iron_bars':
        return 'pane'
    if b.endswith('_fence'):
        return 'nether' if b.startswith('nether') else 'fence'
    if b.endswith('_wall') and 'sign' not in b and 'banner' not in b and 'torch' not in b:
        return 'wall'
    return None


def connect(blocks):
    """The blocks with panes, bars, fences and walls joined to their neighbours and stairs turned
    at corners, as the game would set them on placing. Prints panes that join nothing (a pane
    standing alone in a room is a window in the wrong cell)."""
    out = dict(blocks)
    alone = []
    for (u, y, v), block in blocks.items():
        b = base(block)
        fam = _family(b)
        name, props = split(block)
        if fam:
            sides = {}
            for side, (du, dv) in DIRS.items():
                nb = blocks.get((u + du, y, v + dv), 'air')
                nf = _family(base(nb))
                joins = (full(nb) or nf == fam or base(nb).endswith('_fence_gate')
                         or (fam == 'wall' and nf == 'pane') or (fam == 'pane' and nf == 'wall'))
                sides[side] = joins
            if fam == 'wall':
                straight = sides in ({'north': True, 'south': True, 'east': False, 'west': False},
                                     {'north': False, 'south': False, 'east': True, 'west': True})
                props.update({s: 'low' if j else 'none' for s, j in sides.items()})
                props['up'] = 'false' if straight else 'true'
            else:
                props.update({s: 'true' if j else 'false' for s, j in sides.items()})
            if fam == 'pane' and not any(sides.values()):
                alone.append((u, y, v))
            out[(u, y, v)] = join(name, props)
        elif b.endswith('_stairs'):
            props['shape'] = _stair_shape(blocks, (u, y, v), props)
            out[(u, y, v)] = join(name, props)
    if alone:
        print('panes joining nothing: %d' % len(alone), alone[:12])
    return out


def _stairs_at(blocks, p):
    b = blocks.get(p, 'air')
    return split(b)[1] if base(b).endswith('_stairs') else None


def _stair_shape(blocks, p, props):
    """Vanilla's StairBlock.getStairsShape, in the drawing's frame."""
    f, half = props.get('facing', 'north'), props.get('half', 'bottom')
    u, y, v = p

    def at(direction):
        du, dv = DIRS[direction]
        return _stairs_at(blocks, (u + du, y, v + dv))

    def can_take(direction):
        o = at(direction)
        return o is None or o.get('facing') != f or o.get('half', 'bottom') != half
    behind = at(f)
    if behind and behind.get('half', 'bottom') == half:
        bf = behind.get('facing')
        if bf in DIRS and bf not in (f, OPP[f]) and can_take(OPP[bf]):
            return 'outer_left' if bf == CCW[f] else 'outer_right'
    front = at(OPP[f])
    if front and front.get('half', 'bottom') == half:
        ff = front.get('facing')
        if ff in DIRS and ff not in (f, OPP[f]) and can_take(ff):
            return 'inner_left' if ff == CCW[f] else 'inner_right'
    return 'straight'


def unattached(blocks):
    """Things that hang on a block with nothing there: an open trapdoor's panel, a ladder, a
    button, a wall sign, banner or torch, a hanging or standing lantern, a vine's side."""
    bad = []
    for (u, y, v), block in blocks.items():
        b = base(block)
        _, pr = split(block)
        need = []                            # (du, dy, dv, must be full)
        f = pr.get('facing')
        if b.endswith('_trapdoor') and pr.get('open') == 'true':
            need.append((*_d3(OPP[f]), False))
        elif b == 'ladder' or b.endswith(('_wall_sign', '_wall_banner', 'wall_torch', '_wall_hanging_sign')):
            need.append((*_d3(OPP[f]), b == 'ladder'))
        elif b.endswith('_button'):
            face = pr.get('face', 'wall')
            need.append((0, -1, 0, False) if face == 'floor' else (0, 1, 0, False) if face == 'ceiling'
                        else (*_d3(OPP[f]), False))
        elif b in ('lantern', 'soul_lantern'):
            need.append((0, 1, 0, False) if pr.get('hanging') == 'true' else (0, -1, 0, False))
        elif b.endswith('_hanging_sign'):
            need.append((0, 1, 0, False))
        elif b == 'vine':
            need += [(*_d3(s), False) for s in DIRS if pr.get(s) == 'true']
        for du, dy, dv, must_full in need:
            nb = blocks.get((u + du, y + dy, v + dv), 'air')
            if base(nb) in AIRS or (must_full and not full(nb)):
                bad.append(((u, y, v), b))
                break
    return bad


WOODS = ('oak', 'spruce', 'birch', 'jungle', 'acacia', 'mangrove', 'cherry', 'bamboo')


def flammable(block):
    b = base(block)
    return (not b.startswith('potted_') and any(w in b for w in WOODS)
            or b.endswith(('_wool', '_carpet', '_leaves')) or b in ('bookshelf', 'hay_block', 'scaffolding',
                                                                    'coal_block', 'vine', 'lectern'))


def fire_risk(blocks):
    """Flammable blocks within 2 sideways and 5 above any lava (the fire-spacing rule)."""
    out = set()
    for (u, y, v), b in blocks.items():
        if base(b) != 'lava':
            continue
        for du in range(-2, 3):
            for dv in range(-2, 3):
                for dy in range(0, 6):
                    q = (u + du, y + dy, v + dv)
                    if flammable(blocks.get(q, 'air')):
                        out.add((q, base(blocks[q])))
    return sorted(out)


def _d3(direction):
    du, dv = DIRS[direction]
    return du, 0, dv


# Block light by name, the game's levels; a light block carries its own (level=, 15 by default).
GLOW = {'lantern': 15, 'sea_lantern': 15, 'jack_o_lantern': 15, 'campfire': 15, 'glowstone': 15,
        'shroomlight': 15, 'lava': 15, 'torch': 14, 'wall_torch': 14, 'soul_lantern': 10,
        'soul_campfire': 10, 'soul_torch': 10, 'soul_wall_torch': 10, 'magma_block': 3}
FACES = (((1, 0, 0), 'north', 'south'), ((-1, 0, 0), 'south', 'north'), ((0, 0, 1), 'east', 'west'),
         ((0, 0, -1), 'west', 'east'), ((0, 1, 0), 'up', 'down'), ((0, -1, 0), 'down', 'up'))


def glow(block):
    b = base(block)
    if 'lit=false' in block:
        return 0
    if b == 'light':
        return int(split(block)[1].get('level', 15))
    return GLOW.get(b, 0)


def clear(block):
    """Does block light pass into it? Every block that isn't full does, and glass, ice, leaves and
    water."""
    b = base(block)
    return (not full(block) or b in ('light', 'ice', 'water', 'lava') or b.endswith('leaves')
            or (b.endswith('glass') and b != 'tinted_glass'))


def shut(block, face):
    """Does the block cover its whole face toward ``face``? Light never crosses a whole face: a slab
    floor or ceiling stops it, and so do a stair's underside (or top) and its back."""
    b = base(block)
    _, pr = split(block)
    if b.endswith('_slab'):
        return face == {'bottom': 'down', 'top': 'up'}.get(pr.get('type', 'bottom'))
    if b.endswith('_stairs'):
        return face in ('up' if pr.get('half') == 'top' else 'down', pr.get('facing', 'north'))
    return False


def dark(blocks):
    """Feet cells where a mob could spawn: a full block below (not glass, leaves or water), air at
    the feet, room for a head, block light 0, and something other than leaves overhead (out in the
    open the sky lights it by day). Block light floods from every lamp and fire (``glow``), one less
    a block, into every block it passes (``clear``), never across a whole face (``shut``)."""
    # ponytail: leaves and water dim no more than air, snow, path and farmland let light through, and
    # two half faces never close a face together; the game is a little darker there.
    light = {p: glow(b) for p, b in blocks.items() if glow(b)}
    todo = deque(light)
    while todo:
        p = todo.popleft()
        lv = light[p] - 1
        here = blocks.get(p, 'air')
        for (du, dy, dv), out, into in FACES:
            q = (p[0] + du, p[1] + dy, p[2] + dv)
            there = blocks.get(q, 'air')
            if lv <= light.get(q, 0) or not clear(there) or shut(here, out) or shut(there, into):
                continue
            light[q] = lv
            todo.append(q)
    top = {}
    for (u, y, v), b in blocks.items():
        if base(b) not in AIRS and not base(b).endswith('leaves'):
            top[(u, v)] = max(top.get((u, v), y), y)
    return sorted((u, y + 1, v) for (u, y, v), b in blocks.items()
                  if not clear(b) and base(blocks.get((u, y + 1, v), 'air')) in AIRS
                  and passable(blocks.get((u, y + 2, v), 'air'))
                  and not light.get((u, y + 1, v)) and top.get((u, v), y) > y + 1)


def check(blocks, start, floors=()):
    """Print the facts: floating blocks, things hung on nothing, flammables by lava, covered cells left
    dark, and for each named floor (name, y, cells) how much of it a player reaches from start.
    Returns True when all of them are clean and every floor is reached."""
    good = True
    f = floating(blocks)
    print('floating blocks: %d' % len(f), f[:12] if f else '')
    good &= not f
    h = unattached(blocks)
    print('hung on nothing: %d' % len(h), h[:12] if h else '')
    good &= not h
    r = fire_risk(blocks)
    print('flammable by lava: %d' % len(r), r[:12] if r else '')
    good &= not r
    k = dark(blocks)
    print('dark covered cells: %d' % len(k), k[:12] if k else '')
    good &= not k
    reach = walk(blocks, start)
    for name, cells in floors:
        cells = [c for c in cells if passable(blocks.get(c, 'air'))]
        got = sum(1 for c in cells if c in reach)
        print('%-24s reached %3d of %3d standing cells' % (name, got, len(cells)))
        good &= got > 0
    return good


if __name__ == '__main__':
    # A shut stone room with 5 by 5 cells of floor: dark, then lit by a lantern, then dark again with
    # the lantern up on a slab ceiling.
    room = {(u, y, v): 'stone' for u in range(-3, 4) for v in range(-3, 4) for y in range(5)
            if y in (0, 4) or 3 in (abs(u), abs(v))}
    assert len(dark(room)) == 25
    assert dark({**room, (0, 1, 0): 'lantern'}) == []
    slab = {p: 'oak_slab' if p[1] == 4 else b for p, b in room.items()}
    assert len(dark({**slab, (0, 5, 0): 'lantern'})) == 25
    print('dark: ok')
