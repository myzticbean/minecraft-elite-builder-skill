"""Drawing a building in its own frame, the way Blockbench draws a model: an authoring tool.

A drawing is in the building's own frame: u runs across the front (+u is the left hand of someone
on the path looking at it), v runs back into the hill, y 0 is the ground's own layer. A block is a
vanilla id with props (``oak_stairs[facing=west]``) or a palette reference (``@roof[facing=west]``).
Facings are written in the file's frame, where the front faces west: west is out of the front, east
is into the hill, north is +u, south is -u. ``look.resolve`` turns a drawing into blocks and
``schem.write`` into a schematic.
"""
import hashlib
import math


OPP = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}


def shutter(on, wood='spruce', half='bottom'):
    """An open trapdoor laid flat on the block at its ``on`` side (north, south, east or west). Its
    panel lies opposite its facing, so the facing points away from the block it lies on."""
    return '%s_trapdoor[facing=%s,half=%s,open=true]' % (wood, OPP[on], half)


def hash01(*k):
    """A stable number in [0, 1) for a position and a salt."""
    h = hashlib.blake2b(repr(k).encode(), digest_size=8).digest()
    return int.from_bytes(h, 'big') / 2 ** 64


def toward(du, dv):
    """The facing from a ring cell (du, dv) toward the ring's centre."""
    if abs(du) >= abs(dv):
        return 'south' if du > 0 else 'north'
    return 'west' if dv > 0 else 'east'


def octo(du, dv, r):
    """Inside a square of radius r with its corners cut: a tower's octagonal plan."""
    return max(abs(du), abs(dv)) <= r and not abs(du) == abs(dv) == r


class Drawing:
    def __init__(self, title):
        self.title = title
        self.cells = {}      # (u, y, v) -> (block, loose)
        self.palettes = {}

    # ------------------------------------------------------------ blocks

    def set(self, u, y, v, block, loose=False):
        self.cells[(u, y, v)] = (block, loose)

    def get(self, u, y, v):
        c = self.cells.get((u, y, v))
        return c[0] if c else None

    def clear(self, u, y, v):
        self.cells.pop((u, y, v), None)

    def box(self, u0, y0, v0, u1, y1, v1, block, hollow=False):
        """Every cell of the box; ``hollow`` keeps only its sides (no top or bottom left open)."""
        for u in range(min(u0, u1), max(u0, u1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for v in range(min(v0, v1), max(v0, v1) + 1):
                    side = u in (u0, u1) or v in (v0, v1) or y in (y0, y1)
                    if not hollow or side:
                        self.set(u, y, v, block(u, y, v) if callable(block) else block)

    fill = box

    def line(self, a, b, block):
        """Cells along a straight line from a to b, (u, y, v) each."""
        n = max(abs(b[i] - a[i]) for i in range(3)) or 1
        for k in range(n + 1):
            p = tuple(round(a[i] + (b[i] - a[i]) * k / n) for i in range(3))
            self.set(*p, block(*p) if callable(block) else block)

    def gable(self, u0, u1, v0, v1, y, key, overhang=1, slab=None, under=None):
        """A gable roof with its ridge along v over u0..u1, eaves at y, stairs from ``key`` (a
        palette reference or id), a slab along an odd ridge; overhang past every side. ``under``
        puts a full block under every stair above the eave, so the roof is two thick."""
        mid2 = u0 + u1
        for u in range(u0 - overhang, u1 + overhang + 1):
            d = min(u - (u0 - overhang), (u1 + overhang) - u)
            for v in range(v0 - overhang, v1 + overhang + 1):
                if 2 * u == mid2:
                    self.set(u, y + d, v, (slab or key) + '[type=bottom]')
                else:
                    face = 'north' if 2 * u < mid2 else 'south'   # rising toward the ridge
                    self.set(u, y + d, v, key + '[facing=' + face + ',half=bottom]')
                if under and d >= 1:
                    self.set(u, y + d - 1, v, under)

    def _course(self, cell, k, profile, y, keys, under, facing, force_under=False, thin=False):
        """One column of a profiled roof: the surface block at its height, roof blocks under it down
        to the outer neighbour's height, so a steep step shows a face of roof, never a hole. ``thin``
        (a gable's barge board) puts only an upside-down stair under a stair, so the board's
        underside runs with the slope instead of filling down in steps."""
        stairs, slab, block = (key(k) if callable(key) else key for key in keys)
        dy, kind = profile[k]
        top = y + dy
        if kind == 'stair' and facing:
            surface = '%s[facing=%s,half=bottom]' % (stairs, facing)
        elif kind in ('slab', 'top'):
            surface = '%s[type=%s]' % (slab, 'bottom' if kind == 'slab' else 'top')
        else:
            surface = block
        self.set(*cell(top), surface)
        low = top
        if k > 0:
            low = min(y + profile[k - 1][0], top - 1)
            u_key = under(k) if callable(under) else under
            if thin and facing:
                low, u_key = top - 1, '%s[facing=%s,half=top]' % (stairs, OPP[facing])
            for yy in range(low, top):
                if force_under or self.get(*cell(yy)) is None:
                    self.set(*cell(yy), u_key)
        return top, low

    def roof(self, a0, a1, b0, b1, y, profile, keys, under, along='v', verge=None):
        """A gable roof with a profile: across a0..a1 (the overhang included), along b0..b1 (the
        ridge's run, overhang included), eaves at y. ``along`` is the ridge's axis: 'v' (the gable
        ends face the path) or 'u'. ``profile`` is [(dy, kind)] from the eave inward, kind 'slab',
        'top', 'stair' or 'block'; a bellcast is shallow at the eave (slab, stair) and steep at the
        ridge (rises of two, stair over block). An odd span's middle column takes the entry after the
        last one it reaches. ``keys`` is (stairs, slab, block) palette references or ids, each one
        maybe a function of the column's k for a gradient; ``verge`` the same for the two gable
        rows (thin barge boards). Returns {a: (surface y, lowest roof y)}: fill a gable up to the
        surface y, under the board."""
        mid2 = a0 + a1
        out = {}
        for a in range(a0, a1 + 1):
            k = min(a - a0, a1 - a, len(profile) - 1)
            if 2 * a == mid2:
                facing = None
            elif along == 'v':
                facing = 'north' if 2 * a < mid2 else 'south'
            else:
                facing = 'east' if 2 * a < mid2 else 'west'
            for b in range(b0, b1 + 1):
                def cell(yy, a=a, b=b):
                    return (a, yy, b) if along == 'v' else (b, yy, a)
                edge = bool(verge) and b in (b0, b1)
                out[a] = self._course(cell, k, profile, y, verge if edge else keys,
                                      verge[2] if edge else under, facing, thin=edge)
        return out

    def spire(self, cu, cv, r, y, profile, keys, under):
        """A square pyramid roof round (cu, cv), r out to its eave, eaves at y, with a profile as in
        ``roof`` (entry k for the ring r - k in; the last entry is the tip)."""
        for du in range(-r, r + 1):
            for dv in range(-r, r + 1):
                k = r - max(abs(du), abs(dv))
                if du == dv == 0:
                    facing = None
                elif abs(du) >= abs(dv):
                    facing = 'north' if du < 0 else 'south'
                else:
                    facing = 'east' if dv < 0 else 'west'

                def cell(yy, u=cu + du, v=cv + dv):
                    return (u, yy, v)
                self._course(cell, k, profile, y, keys, under, facing, force_under=True)

    def arch(self, cell, a0, a1, spring, bottom=1, ends=('south', 'north'), stairs='stone_brick_stairs',
             slab='stone_brick_slab', ring='polished_andesite', key='chiseled_stone_bricks'):
        """A round-headed opening a0..a1 in a wall, cell(a, y) -> (u, y, v): straight jambs from
        ``bottom`` to ``spring``, then a half circle on the opening's width, with an upside-down stair
        (its low end facing ends[0], its high end ends[1]: outward) or a top slab where the curve falls
        half-way through a block, a voussoir over every column, a key at the crown, imposts at the
        spring."""
        c, r = (a0 + a1) / 2, (a1 - a0 + 1) / 2
        for a in range(a0, a1 + 1):
            h = math.sqrt(r * r - (a - c) ** 2)
            top = spring + int(h)
            for y in range(bottom, top + 1):
                self.set(*cell(a, y), 'air')
            y = top + 1
            if h - int(h) >= 0.35:
                self.set(*cell(a, y), '%s[type=top]' % slab if a == c else
                         '%s[facing=%s,half=top]' % (stairs, ends[0] if a < c else ends[1]))
                y += 1
            self.set(*cell(a, y), key if a == c else ring)
        for a in (a0 - 1, a1 + 1):
            self.set(*cell(a, spring), ring)

    def palette(self, key, mix):
        self.palettes[key] = mix
