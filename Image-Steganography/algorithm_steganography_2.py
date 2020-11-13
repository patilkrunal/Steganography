#steganography
# Lets hide our  data by embedding it into an image.
# ensure to install  opencv-python

import cv2
import os

HEADER_FILENAME_LENGTH= 30
HEADER_FILESIZE_LENGTH= 20
HEADER_LENGTH = HEADER_FILENAME_LENGTH +  HEADER_FILESIZE_LENGTH


getbits = lambda n : [n>>5,(n&0x1C)>>2,n&0x3] 

getbyte =lambda bits : (((bits[0]<<3)|bits[1])<<2)|bits[2]

def get_file_size(filename):
	try:
		return os.stat(filename).st_size
	except:
		return 0


	#fileName: 'd:/images/work.jpg
def generate_header(filename):

	file_size=get_file_size(filename)
	if file_size==0:
		return None
	name=filename.split('/')[-1]
	#splitted: [d:, images, work.jpg]
	name_extension=name.split('.')
	extension_name=name_extension[1]
	extension_size=len(extension_name)+1

	name_len=HEADER_FILENAME_LENGTH - extension_size

	name=name_extension[0][:name_len]+ '.' + extension_name

	name=name.ljust(HEADER_FILENAME_LENGTH,'*')
	qty=str(file_size).ljust(HEADER_FILESIZE_LENGTH,'*')

	return name+qty

def embed(result_img,src_img,file_to_embed):
	image=cv2.imread(src_img,cv2.IMREAD_COLOR)
	if image is None:
		print(src_img,"not found")
		return False

	file_size=get_file_size(file_to_embed)
	if file_size==0:
		print(file_to_embed,"not found")
		return False

	#capacity check

	h,w,band=image.shape  #band (BGR)
	capacity=h*w
	if capacity<file_size+HEADER_LENGTH:
		print('embedding is not possible Insufficient Image Capacity')
		return False

        #get header
	header=generate_header(file_to_embed)
	# print("header= ",header)
	cnt=0
	i=0
	data=0
	keep_going=True
	fh=open(file_to_embed,'rb')
	b=0
	while i<h and keep_going:
		j=0
		while j<w:
			if cnt<HEADER_LENGTH:
				data=ord(header[cnt])
				# print(header[cnt])

				#cnt+=1
			else:
				data=fh.read(1)
				    # as the file is opened in binary mode
					# so we get byte objects on read
					# the byte object dont support bitwise operations
					# hence they are to be converted to int
				if data:
					data=int.from_bytes(data,byteorder='big')
				else:
					keep_going=False
					break

			bits=getbits(data)

			image[i,j,2]=(image[i,j,2]& (~0x7))|bits[0]
			image[i,j,1]=(image[i,j,1]& (~0x7))|bits[1]
			image[i,j,0]=(image[i,j,0]& (~0x3))|bits[2]
			
			# if b<10:
			# 	print(image[i,j,2]," ",image[i,j,1]," ",image[i,j,0])
			# 	b+=1

			cnt+=1
			j+=1

		i+=1

	fh.close()

	#save back the image
	cv2.imwrite(result_img, image)
	print('Embedding Done')



def extract(src_img, result_folder):
	#load the image as a numpy.ndarray
	image=cv2.imread(src_img,cv2.IMREAD_COLOR)
	if image is None:
		print(src_img,"not found")
		return False
	header=''
	fh=None
	i=0
	cnt=0
	keep_going=True
	h,w,band=image.shape
	b=0
	while i<h and keep_going:
		j=0
		while j<w:
			bit1=image[i,j,2]& 0x7
			bit2=image[i,j,1]& 0x7
			bit3=image[i,j,0]& 0x3

			data=getbyte([bit1,bit2,bit3])
			
			# if b<50:
			# 	print(image[i,j,2]," ",image[i,j,1]," ",image[i,j,0])
			# 	b+=1

			if cnt<HEADER_LENGTH:
				header=header+chr(data)
				# print(chr(data))
			else :
				
				if cnt==HEADER_LENGTH:
					# print(header)
					filename=result_folder+ '/' + header[:HEADER_FILENAME_LENGTH].strip('*')
					# print(filename)
					filesize=int(header[HEADER_FILENAME_LENGTH:].strip('*')) + cnt
					# print(filesize,cnt)
					fh=open(filename,'wb')

				if cnt<filesize:
					data=int.to_bytes(int(data),1,byteorder='big')
					fh.write(data)

				else:
					fh.close()
					keep_going=False
					break

			cnt+=1
			j+=1
		i+=1


	print("extraction done")



def main():

	while True:
		
		print('1. Embed ')
		print('2. Extract')
		print('3. Exit')
		ch = input()
		if ch=='1':
		    result_img=input('enter the path with the resultant image_name eg:-"/home/nikhil/Downloads/result.png" or "d:/images/result.png" ')
		    file_to_embed=input('enter the path for file to embed')
		    src_img=input('enter the path of image in which the file needs to be embedded')

		    result=embed(result_img,src_img,file_to_embed)
		    if result == False:
		        print('EMBEDDED FAILED ')
		    
		elif ch=='2':
		    signedImg = input('Enter  Stego Image ')
		    result_folder=input('Enter the folder name where you want the extracted file eg:- "/home/nikhil/Pictures" or "f:/images"')
		    x=extract(signedImg,result_folder)
		    if x==False:
		        print("extraction failed")

		elif ch == '3':
		    break

		else:
		    print('Wrong Choice')

main()
