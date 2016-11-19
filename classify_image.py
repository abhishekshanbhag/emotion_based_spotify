import numpy
import csv
from keras.datasets import mnist
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')
from boto.s3.connection import S3Connection
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

aws_cred = []

# Download image from Amazon s3 bucket
with open('rootkey_2.csv',"r") as infile:
    lines = csv.reader(infile,delimiter='=')
    for row in lines:
        aws_cred.append(row[1])

aws_connection = S3Connection(aws_cred[0], aws_cred[1])
bucket = aws_connection.get_bucket('ec601imagebucket')
for file_key in bucket.list():
    print file_key.name

file_key.get_contents_to_filename('test_images.csv')

testset = numpy.loadtxt("test_images.csv", delimiter=",")
X_test = testset[:,0:2304]
y_test = testset[:,2304]

X_test = X_test.reshape(X_test.shape[0], 1, 48, 48).astype('float32')
X_test = X_test / 255

y_test = np_utils.to_categorical(y_test)
# Y_test = testset[:,2304]


# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# label_predict = loaded_model.predict(X_test)
# image_num = 2;
# print(label_predict[3])
# rounded_predict = [round(label_predict) for x in label_predict]
# print(round(label_predict[3]))
score = loaded_model.evaluate(X_test, y_test, verbose=0)
print "%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100)
