'''
This script performs emotion classification on the photo taken by the user.  The
script performs the following steps:

    1. Download photo from Amazon S3 storage bucket
    2. Covert colored photo to grayscale
    3. Loads trained convolutional neural network
    4. Performs emotion prediction

'''

# Load required functions and classes
import numpy
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys
K.set_image_dim_ordering('th')

if(len(sys.argv) != 2):
	sys.exit(1)

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# Download image from Amazon s3 bucket
with open('rootkey_2.csv',"r") as infile:
    text = infile.readlines()
    infile.close()

AWS_KEY = text[0].strip()
AWS_SECRET = text[1].strip()

AWS_KEY = AWS_KEY[15:]
AWS_SECRET = AWS_SECRET[13:]

predict_file_key = Key()
aws_connection = S3Connection(AWS_KEY, AWS_SECRET)
bucket = aws_connection.get_bucket('ec601imagebucket')
for file_key in bucket.list():
    if(file_key.name.encode('utf-8') == sys.argv[1]):
        predict_file_key = file_key
        break
if(predict_file_key.name == None):
    print('No such file found')
    sys.exit(1)

predict_file_key.get_contents_to_filename('test_image.jpg')
bucket.delete_key(predict_file_key)

# Covert photo to grayscale
def rgb2gray(rgb):
    return numpy.dot(rgb[...,:3],[0.299,0.587,0.114])

def detect(img, cascade):
    rects = []
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        rects = list([])
    else:
        rects[:,2:] += rects[:,:2]
    return rects

cascade_fn = "face_detection_files/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_fn)


#img = mpimg.imread('test_image.jpg')
img = cv2.imread('test_image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

rects = detect(gray, cascade)
if(len(rects)):
    i = 0
    biggest_sz = 0
    biggest_index = 0
    for x1, y1, x2, y2 in rects:
        temp_face = gray[y1:y2, x1:x2]
        sz1 = (y2-y1)*(x2-x1)
        if sz1 > biggest_sz:
            biggest_sz = sz1
            biggest_index = i
        i = i+1
    x1, y1, x2, y2 = rects[biggest_index]
    roi = gray[y1:y2, x1:x2]
else:
    roi = gray
    print('face not detected. Please click from another angle of lighting.')
roi = cv2.equalizeHist(roi)
roi = cv2.resize(roi, (48, 48))

# X_test = rgb2gray(img)
#X_test = X_test.reshape(1,1,48, 48).astype('float32')
X_test = roi.reshape(1,1,48, 48).astype('float32')
X_test = X_test / 255
# plt.imshow(gray_out,cmap = plt.get_cmap('gray'))
# plt.show()'''


# y_test = np_utils.to_categorical(y_test)
# Y_test = testset[:,2304]

# Load trained convolutional neural network model (both structure and weights)
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
# print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
label_predict = loaded_model.predict(X_test)
print(label_predict)
label_predict = numpy.argmax(label_predict)
# image_num = 2;
print(label_predict)
# rounded_predict = [round(label_predict) for x in label_predict]
# print(round(label_predict[3]))
# score = loaded_model.evaluate(X_test, y_test, verbose=0)
# print "%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100)
