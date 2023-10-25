import cv2
import  matplotlib.pyplot as plt

img=cv2.imread('mount.jpg',cv2.IMREAD_COLOR)
resize_img=cv2.resize(img,(1920,1080))
print(resize_img.shape,resize_img.size)
print(img.shape,img.size)
print(plt.get_backend())
resize_img[:,:,0]=resize_img[:,:,0]/1.1
plt.imshow(resize_img)
plt.show()