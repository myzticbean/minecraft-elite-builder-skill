"""A closer look at any build script than its own run gives:

  python review.py <build.py> close <prefix> u0 u1 v0 v1 [corners]
      Isometric views cropped to the box, in true sub-block shapes (look.close). corners like 3,2:
      3 the front left (the hero angle), 2 the front right, 1 the back right, 0 the back left.
  python review.py <build.py> cut <prefix> ymax u0 u1 v0 v1 [corner]
      The same, with everything above ymax taken off: interiors, floors, stairs.
  python review.py <build.py> dump <axis> <at> y0 y1 a0 a1
      One plane's cells as letters, top row first, with a key: axis v holds v at <at> (a wall seen
      from the path, the page's left the player's left, high u); axis u holds u. Settles what an
      isometric view only seems to show (a wall that looks open may be foreshortened).

The build is loaded as a module, so its __main__ (checks, schematic) doesn't run; it must keep its
drawing in ``d``. Blocks are resolved and connected exactly as for the schematic.
"""
import contextlib
import importlib.util
import io
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import look  # noqa: E402


def blocks_of(path):
    spec = importlib.util.spec_from_file_location('build', path)
    build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build)
    with contextlib.redirect_stdout(io.StringIO()):
        return look.connect(look.resolve(build.d))


def dump(blocks, axis, at, y0, y1, a0, a1):
    def cell(a, y):
        return blocks.get((a, y, at) if axis == 'v' else (at, y, a), 'air')
    rows = [(y, [look.base(cell(a, y)) for a in range(a1, a0 - 1, -1)]) for y in range(y1, y0 - 1, -1)]
    names = Counter(b for _, row in rows for b in row if b not in look.AIRS)
    key = {b: (chr(97 + i) if i < 26 else '#') for i, (b, _) in enumerate(names.most_common())}
    for y, row in rows:
        print('%4d  %s' % (y, ''.join(key.get(b, '.') for b in row)))
    print('      %s = %d .. %d, left to right' % ('u' if axis == 'v' else 'v', a1, a0))
    for b, k in key.items():
        print('  %s %s' % (k, b))


if __name__ == '__main__':
    path, view, *args = sys.argv[1:]
    blocks = blocks_of(path)
    if view == 'close':
        corners = tuple(int(c) for c in args[5].split(',')) if len(args) > 5 else (3, 2)
        print(look.close(blocks, args[0], tuple(int(x) for x in args[1:5]), corners=corners, s=28))
    elif view == 'cut':
        ymax, u0, u1, v0, v1 = (int(x) for x in args[1:6])
        k = int(args[6]) if len(args) > 6 else 3
        part = {p: b for p, b in blocks.items() if p[1] <= ymax and u0 <= p[0] <= u1 and v0 <= p[2] <= v1}
        out = '%s-cut%d.png' % (args[0], k)
        look.write_png(out, look.iso(look.fine(look.Volume(part), 4), k, s=6))
        print(out)
    elif view == 'dump':
        dump(blocks, args[0], *(int(x) for x in args[1:6]))
    else:
        sys.exit(__doc__)
