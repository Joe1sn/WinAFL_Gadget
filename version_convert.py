"""
drcov version 3 isn't supported by lighthouse :(
convert drcov version 3 with module table version 5 to drcov version 2
    with module table version 2 so lighthouse will eat it!
"""

import sys
import re


def eprint(*args, **kwargs):
    kwargs["file"] = sys.stderr
    return print(*args, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        eprint(f"Usage: {sys.argv[0]} <input file> [<output file>]")
        sys.exit(1)
    if len(sys.argv) == 2:
        outfile = sys.argv[1]
    else:
        outfile = sys.argv[2]

    output = b""
    inf = open(sys.argv[1], "rb")

    # drcov version
    ver = inf.readline()
    if not re.match(rb"DRCOV VERSION: 3", ver):
        eprint("Wrong version or bad format")
        sys.exit(2)
    output += b"DRCOV VERSION: 2\n"

    # flavor (don't care)
    output += inf.readline()

    # module table info
    mti = inf.readline()
    mti = re.match(rb"Module Table: version (\d+), count (\d+)", mti)
    if not mti:
        eprint("Bad module table info")
        sys.exit(3)
    ver = int(mti.group(1))
    mcount = int(mti.group(2))
    output += f"Module Table: version 2, count {mcount}\n".encode()

    # column labels
    cols = inf.readline().rstrip()
    cols = re.match(rb"Columns: (.*)", cols)
    if not cols:
        eprint("Bad module table columns")
        sys.exit(4)
    cols = cols.group(1).split(b", ")

    def compat_cols(col):
        return {b"start": b"base"}.get(col, col)

    # we care about id, base, end, and path
    idxs = {
        compat_cols(c): i
        for i, c in enumerate(cols)
        if compat_cols(c) in [b"id", b"base", b"end", b"path"]
    }
    if len(idxs) != 4:
        eprint("id, base, end, and path columns are required")
        sys.exit(5)
    output += b"Columns: id, base, end, entry, checksum, timestamp, path\n"

    # module list
    rjust = len(str(mcount))
    for _ in range(mcount):
        mod = inf.readline().rstrip().split(b", ")
        output += b", ".join(
            [
                mod[idxs[b"id"]].rjust(rjust),
                mod[idxs[b"base"]],
                mod[idxs[b"end"]],
                b"0x0",
                b"0x0",
                b"0x0",
                mod[idxs[b"path"]].strip(),
            ]
        )
        output += b"\n"

    # need to read the rest into memory here in case input
    # and output files are the same
    output += inf.read()
    with open(outfile, "wb") as w:
        # at this point dump the updated module list
        # and then read the rest of the in file
        w.write(output)