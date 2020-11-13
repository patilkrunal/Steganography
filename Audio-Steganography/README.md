# SteganoSound-Py

Audio Steganography is the art of covertly embedding secret messages into digital audio. This Program lets you hide any kind of data file within a WAV Audio File. It also uses password based encryption so that anyone without the key cannot extract the data. Fernet Encrytion  has been used to encrypt the data. Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key.

## USAGE

### INSTALL REQUIRED PACKAGES (FOR FIRST TIME USE ONLY)
```
$ pip3 install -r requirements.txt
```
### TO HIDE DATA IN WAV FILE:
```
$ python3 main.py -h <WavFile> <DataFile> <Password>
```
### RECOVER HIDDEN DATA FROM WAV FILE IF PRESENT:
```
$ python3 main.py -r <WavFile> <Password>
```
### SHOW USAGE:
```
$ python3 main.py --help 
```

Report any Issues and 
Feel Free to Contribute!! 
