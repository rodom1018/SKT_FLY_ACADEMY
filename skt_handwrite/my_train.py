import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

#칼라 -> 검정/하양 전환
def get_char(image):

    a = ( image[:,:,0] == 255)
    b = (image[:, :, 1] ==255)
    c = (image[:,:,2] == 255)

    image[b] = [255,255,255]
    white = a&b&c

    image[a] = [255,255,255]
    image[c] = [255,255,255]
    image[white] = [0,0,0]

    return image

def my_train(now_image, i):
    now_image = get_char(now_image)
    image_gray = cv2.cvtColor(now_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image_gray, 230, 255, 0)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    now_image = cv2.bitwise_not(thresh)
    now_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    for contour in contours:

        x, y, width, height = cv2.boundingRect(contour)
        new_image = now_image[y:y + height, x:x + width]
        new_image = cv2.resize(new_image, (20, 20))
        # plt.imshow(new_image)
        # plt.show()
        gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
        #print(i)
        #plt.imshow(gray)
        #plt.show()
        train.append(gray)
        train_labels.append(i)


###########################################
###############main########################
###########################################
now_image = cv2.imread("./samples/1/1.png")
now_image = get_char(now_image)
#plt.imshow(now_image)
#plt.show()

train = []
train_labels = []

for i in range(13):
    path = './samples/'+str(i)+'/'
    for j in range(20):
        img = cv2.imread(path+str(j)+'.png')
        my_train(img, i)

#print(train)
x = np.array(train)
train = x[:,:].reshape(-1,400).astype(np.float32)
train_labels = np.array(train_labels)[:, np.newaxis]

np.savez("trained.npz", train=train, train_labels=train_labels)


