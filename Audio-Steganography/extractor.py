import wave as w
import bitarray as b
import headerManager
import securityManager as sm


def extract(fpath, password_provided):

    song = w.open(fpath, mode='rb')
    songBytes = bytearray(list(song.readframes(song.getnframes())))

    h = ""
    f = ""
    keepExtracting = True
    i = 0
    while keepExtracting:
        if i < 200:
            h = h+str((songBytes[i] & 1))

        elif i == 200:
            hdrBits = b.bitarray(h)
            hdr = hdrBits.tostring()
            f = f+str((songBytes[i] & 1))

        else:
            fname, fsize = headerManager.getFileNameSize(hdr)
            f = f+str((songBytes[i] & 1))
            if i == 200 + (fsize*8):
                keepExtracting = False
        i = i+1

    msg = b.bitarray(f)
    decrypted = sm.decrypt(msg, password_provided)
    with open(fname, 'wb') as m:
        m.write(decrypted)

    print("File Extracted Successfully!!")
    song.close()
