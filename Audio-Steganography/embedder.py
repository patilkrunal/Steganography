import wave as w
import bitarray as b
import headerManager as hm
import os
import sys
import securityManager as sm
# embedding should be with each pixel of image

def embed(fpath, mpath, password_provided):
    song = w.open(fpath, mode='rb')
    songBytes = bytearray(list(song.readframes(song.getnframes())))

    msg = open(mpath, "rb")
    msgBits = b.bitarray(sm.encrypt(msg, password_provided))

    hdr = hm.formHeader(mpath, int(msgBits.length()/8))
    hdrBits = b.bitarray()
    hdrBits.fromstring(hdr)

    bits = b.bitarray(hdrBits)
    bits.extend(msgBits)

    if bits.length() > len(songBytes):
        print("Data File too big to be hidden in given WAV File!!")
        sys.exit(1)

    for i, bit in enumerate(bits):
        songBytes[i] = (songBytes[i] & 254) | bit

    songMod = bytes(songBytes)

    with w.open(os.path.basename(fpath)+"_mod", "wb") as fd:
        fd.setparams(song.getparams())
        fd.writeframes(songMod)

    print("File Hidden Successully!!")
    song.close()
