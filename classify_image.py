from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import os
from boto.s3.connection import S3Connection
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# Download image from Amazon s3 bucket
AWS_KEY = 'AKIAII34U7AV4AUDSULA'
AWS_SECRET = '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'
aws_connection = S3Connection(AWS_KEY, AWS_SECRET)
bucket = aws_connection.get_bucket('ec601imagebucket')
for file_key in bucket.list():
    print file_key.name

file_key.get_contents_to_filename('test_images.csv')

testset = numpy.loadtxt("test_images.csv", delimiter=",")
X_test = testset[:,0:2304]
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
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
label_predict = loaded_model.predict(X_test)
# image_num = 2;
print(label_predict[3])
# rounded_predict = [round(label_predict) for x in label_predict]
print(round(label_predict[3]))
# score = loaded_model.evaluate(X_test, Y_test, verbose=0)
# print "%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100)
