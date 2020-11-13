import os

# HEADER_LENGHT=25
# SEPARATOR='~'


def formHeader(mpath, msize):
    ms = str(msize)
    while len(ms) < 8:
        ms = "#"+ms

    mpath = os.path.basename(mpath)
    if len(mpath) > 16:
        pos = len(mpath)-16
        mpath = mpath[pos:]
    else:
        while len(mpath) < 16:
            mpath = "#"+mpath

    return mpath+"~"+ms


def getFileNameSize(hdr):
    name = hdr[0:16]
    name = name.replace("#", " ")
    name = name.strip()

    size = hdr[17:]
    size = size.replace("#", " ")
    size = size.strip()

    return name, int(size)
