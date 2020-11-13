import cv2  #computer vision library

#digital  sign means having some message hidden behind a photo which could be extracted to proof the ownership and piracy protection

#identifier = lambda  multiple_parameters : one line logic only
getbits =lambda n : [n>>5,(n&0x1C)>>2,n&0x3 ]

getbyte =lambda bits : (((bits[0]<<3)| bits[1])<<2)|bits[2]


normalized_signature= lambda sign,size=30: sign.ljust(size,'#')

original_signature=lambda sign: sign.strip('#') # strip function strips from either end but not from middle

def embedding_points(qty=30):
    points=[]
    for i in range(qty):
        points.append((7,i))

    return points

def embed(trg_img,src_img,sign):
    normalized_sign=normalized_signature(sign)
    #print(normalized_sign)
    image=cv2.imread(src_img,cv2.IMREAD_COLOR)
    if image is None:
        print('error in loading image')
        return False

    h,w,band=image.shape  # returns 3-D array as img is read in IMG COLOR format (height * width * list of band of size 3)
    #print(image.shape)
    
    #capacity check
    capacity=h*w
    if capacity<len(normalized_sign):
        print('embedding is not possible Insufficient Image Capacity')
        return False

    #start embedding
    cnt=0
    embed_at=embedding_points((len(normalized_sign)))
    for x,y in embed_at:
       #print(x,y,end=' ')
       bits=getbits(ord(normalized_sign[cnt]))
       #print(ord(normalized_sign[cnt]),bits[0],bits[1],bits[2])
       image[x,y,2]=(image[x,y,2] & (~0x7))|bits[0]
       image[x,y,1]=(image[x,y,1] & (~0x7))|bits[1]
       image[x,y,0]=(image[x,y,0] & (~0x3))|bits[2]
       #print(image[x,y,2])

       cnt+=1

    cv2.imwrite(trg_img,image)  # it is used to wirte an image on disk  ,here image is the nd array

    return True

def extract(src_img):
    image=cv2.imread(src_img,cv2.IMREAD_COLOR)
    if image is None:
       print("uable to load src img")
       return False 	 
    points=embedding_points(30)
    cnt=0
    
    sign=''
    for x,y in points:
       #print(x,y,end=' ')
       bit1= image[x,y,2] & 0x7
       bit2= image[x,y,1] & 0x7
       bit3= image[x,y,0] & 0x3
       cnt+=1
       #print(bit1,bit2,bit3) 
       #print(image[x,y,2])
       data=getbyte([bit1,bit2,bit3])
       #print(data,end=' ')
       sign = sign + chr(data)
    return original_signature(sign)
	

def main():
    while True:

        print('1. Embed ')
        print('2. Extract')
        print('3. Exit')
        ch = input()
        if ch=='1':
            sign=input('enter your signature (not more than 30 characters) ')
            trg_img=input('enter the path for result image (.png) ')
            src_img=input('enter the path of the src image')

            result=embed(trg_img,src_img,sign)
            if result == True:
                print('EMBEDDED DONE ')
            else:
                print('FAILED')
        elif ch=='2':
            print('Enter Signed Image')
            signedImg = input()
            signature = extract(signedImg)
            print("The signature found = ",signature)

        elif ch == '3':
            break

        else:
            print('Wrong Choice')
    #use the .png extension for avoiding lossy compression 

main()
