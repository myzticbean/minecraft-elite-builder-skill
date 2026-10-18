"""A drawing as a WorldEdit schematic, to paste and look at in game before it becomes a design.

``write(blocks, path, origin)`` writes a Sponge schematic v2 (gzipped NBT) that FAWE loads with
``//schem load``. Blocks are ``look.resolve``'s {(u, y, v): block} in the file frame (x = v,
z = -u, the front faces west); ``origin`` is the drawing cell that lands at the player's feet on
``//paste``. Cells the drawing leaves empty are air, so a plain ``//paste`` clears the box above
the ground (``//paste -a`` keeps what stands there); ``//undo`` puts it all back.

``read(path)`` loads one back as {(x, y, z): block} with the WorldEdit offset, for the check below
and for looking inside schematics we're given.
"""
import gzip
import io
import struct

DATA_VERSION = 4903     # Paper 26.2

# ------------------------------------------------------------ NBT, just the tags a schematic uses

END, BYTE, SHORT, INT, BYTES, STRING, LIST, COMPOUND, INTS = 0, 1, 2, 3, 7, 8, 9, 10, 11


def _w(out, tag, value):
    if tag == BYTE:
        out.write(struct.pack('>b', value))
    elif tag == SHORT:
        out.write(struct.pack('>h', value))
    elif tag == INT:
        out.write(struct.pack('>i', value))
    elif tag == BYTES:
        out.write(struct.pack('>i', len(value)) + bytes(value))
    elif tag == STRING:
        b = value.encode()
        out.write(struct.pack('>H', len(b)) + b)
    elif tag == INTS:
        out.write(struct.pack('>i', len(value)) + struct.pack('>%di' % len(value), *value))
    elif tag == COMPOUND:
        for name, (t, v) in value.items():
            out.write(bytes([t]))
            _w(out, STRING, name)
            _w(out, t, v)
        out.write(bytes([END]))
    else:
        raise ValueError(tag)


def _r(f, tag):
    def take(n):
        return f.read(n)
    if tag == BYTE:
        return struct.unpack('>b', take(1))[0]
    if tag == SHORT:
        return struct.unpack('>h', take(2))[0]
    if tag == INT:
        return struct.unpack('>i', take(4))[0]
    if tag == 4:
        return struct.unpack('>q', take(8))[0]
    if tag == 5:
        return struct.unpack('>f', take(4))[0]
    if tag == 6:
        return struct.unpack('>d', take(8))[0]
    if tag == BYTES:
        return take(struct.unpack('>i', take(4))[0])
    if tag == STRING:
        return take(struct.unpack('>H', take(2))[0]).decode()
    if tag == LIST:
        t, n = take(1)[0], struct.unpack('>i', take(4))[0]
        return [_r(f, t) for _ in range(n)]
    if tag == COMPOUND:
        out = {}
        while (t := take(1)[0]) != END:
            name = _r(f, STRING)            # before the value: `out[k()] = v()` calls v first
            out[name] = _r(f, t)
        return out
    if tag == INTS:
        n = struct.unpack('>i', take(4))[0]
        return list(struct.unpack('>%di' % n, take(4 * n)))
    if tag == 12:
        n = struct.unpack('>i', take(4))[0]
        return list(struct.unpack('>%dq' % n, take(8 * n)))
    raise ValueError(tag)


def _varints(ids):
    out = bytearray()
    for i in ids:
        while i >= 0x80:
            out.append(i & 0x7F | 0x80)
            i >>= 7
        out.append(i)
    return out


def _unvarints(data, n):
    out, i = [], 0
    for _ in range(n):
        v = shift = 0
        while True:
            b = data[i]
            i += 1
            v |= (b & 0x7F) << shift
            shift += 7
            if b < 0x80:
                break
        out.append(v)
    return out


# ------------------------------------------------------------ schematics

def _id(block):
    return block if ':' in block.split('[', 1)[0] else 'minecraft:' + block


def write(blocks, path, origin):
    world = {(v, y, -u): b for (u, y, v), b in blocks.items()}
    ou, oy, ov = origin
    ox, oz = ov, -ou
    xs, ys, zs = zip(*world)
    x0, y0, z0 = min(xs), min(ys), min(zs)
    W, H, L = max(xs) - x0 + 1, max(ys) - y0 + 1, max(zs) - z0 + 1
    palette = {'minecraft:air': 0}
    ids = [0] * (W * H * L)
    for (x, y, z), b in world.items():
        i = palette.setdefault(_id(b), len(palette))
        ids[(x - x0) + (z - z0) * W + (y - y0) * W * L] = i
    off = [x0 - ox, y0 - oy, z0 - oz]
    root = {
        'Version': (INT, 2),
        'DataVersion': (INT, DATA_VERSION),
        'Width': (SHORT, W), 'Height': (SHORT, H), 'Length': (SHORT, L),
        'Offset': (INTS, off),
        'PaletteMax': (INT, len(palette)),
        'Palette': (COMPOUND, {k: (INT, v) for k, v in palette.items()}),
        'BlockData': (BYTES, _varints(ids)),
        'Metadata': (COMPOUND, {'WEOffsetX': (INT, off[0]), 'WEOffsetY': (INT, off[1]),
                                'WEOffsetZ': (INT, off[2])}),
    }
    buf = io.BytesIO()
    buf.write(bytes([COMPOUND]))
    _w(buf, STRING, 'Schematic')
    _w(buf, COMPOUND, root)
    with gzip.open(path, 'wb') as f:
        f.write(buf.getvalue())
    print('wrote', path, '%dx%dx%d' % (W, H, L), len(palette), 'states, offset', off)


def read(path):
    """{(x, y, z): block} relative to the paste origin, air left out; v2 or v3."""
    with gzip.open(path, 'rb') as f:
        f.read(1)
        _r(f, STRING)
        root = _r(f, COMPOUND)
    if 'Schematic' in root:                 # v3 nests everything one deeper
        root = root['Schematic']
        pal, data = root['Blocks']['Palette'], root['Blocks']['Data']
    else:
        pal, data = root['Palette'], root['BlockData']
    W, H, L = root['Width'], root['Height'], root['Length']
    meta = root.get('Metadata', {})
    off = [meta.get('WEOffset' + a, root.get('Offset', [0, 0, 0])[i]) for i, a in enumerate('XYZ')]
    names = {v: k for k, v in pal.items()}
    ids = _unvarints(data, W * H * L)
    out = {}
    for i, n in enumerate(ids):
        b = names[n]
        if b != 'minecraft:air':
            x, z, y = i % W, (i // W) % L, i // (W * L)
            out[(x + off[0], y + off[1], z + off[2])] = b
    return out


if __name__ == '__main__':
    import os
    import tempfile
    blocks = {(0, 0, 0): 'stone', (2, 1, 3): 'oak_stairs[facing=west,half=bottom]', (-1, 0, 5): 'air'}
    p = os.path.join(tempfile.mkdtemp(), 't.schem')
    write(blocks, p, origin=(0, 0, -2))
    back = read(p)
    # file frame: x = v - origin v, z = -u + origin u
    assert back == {(2, 0, 0): 'minecraft:stone',
                    (5, 1, -2): 'minecraft:oak_stairs[facing=west,half=bottom]'}, back
    print('ok')
