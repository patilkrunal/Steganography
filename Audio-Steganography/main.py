#!/usr/bin/python3

import embedder as em
import extractor as ex
import sys


def usage():
    print("\nUsage options:\n\n",
          "TO HIDE DATA IN WAV FILE:\n"
          " -h <WavFile> <DataFile> <Password>\n\n",
          "TO RECOVER HIDDEN DATA FROM WAV FILE IF PRESENT:\n",
          " -r <WavFile> <Password>\n\n",
          " --help  Display help\n")


if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) > 5:
        print("Invalid Number of Arguments!!")
        usage()
        sys.exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            usage()
    elif len(sys.argv) == 5:
        if sys.argv[1] == '-h':
            em.embed(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Invalid Arguments!!")
            usage()
            sys.exit(1)
    elif len(sys.argv) == 4:
        if sys.argv[1] == '-r':
            ex.extract(sys.argv[2], sys.argv[3])
        else:
            print("Invalid Arguments!!")
            usage()
            sys.exit(1)
    else:
        print("Invalid Arguments!!")
        usage()
        sys.exit(1)
