# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Self-contained functions to write an array to a PNG file. These
# do not require PIL, cv2, scipy.misc, etc.
# Source:
#   stackoverflow.com/questions/902761/saving-a-numpy-array-as-an-image
#
# write_png expects an array of 32-bit values, each of which is a pixel
# in packed RGBA format. It generates the headers and other needed PNG atoms
def write_png(buf, width, height):
  """ buf: must be bytes or a bytearray in Python3.x,
      a regular string in Python2.x.
  """
  import zlib, struct

  # reverse the vertical line order and add null bytes at the start
  width_byte_4 = width * 4
  raw_data = b''.join(b'\x00' + buf[span:span + width_byte_4]
            for span in range((height - 1) * width_byte_4, -1, - width_byte_4))

  def png_pack(png_tag, data):
    chunk_head = png_tag + data
    return (struct.pack("!I", len(data)) +
        chunk_head +
        struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))

  return b''.join([
    b'\x89PNG\r\n\x1a\n',
    png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
    png_pack(b'IDAT', zlib.compress(raw_data, 9)),
    png_pack(b'IEND', b'')])

# Wrapper that takes a normal array (integers, packed ARGB), and filename
def saveAsPNG(array, filename):
  import struct
  if any([len(row) != len(array[0]) for row in array]):
    raise ValueError, "Array should have elements of equal size"

  # First row becomes top row of image.
  flat = []; map(flat.extend, reversed(array))
  # Big-endian, unsigned 32-byte integer.
  buf = b''.join([struct.pack('>I', ((0xffFFff & i32)<<8)|(i32>>24) )
          for i32 in flat])   # Rotate from ARGB to RGBA.

  data = write_png(buf, len(array[0]), len(array))
  f = open(filename, 'wb')
  f.write(data)
  f.close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


seed = 8
import numpy
# fix random seed for reproducibility
numpy.random.seed(seed)

import tensorflow as tf
tf.set_random_seed(seed)

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D

dataset = numpy.loadtxt("fer2013/happy-sad-training.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:2304]
Y = dataset[:,2304]

# Simplarly load the evaluation data
testset = numpy.loadtxt("fer2013/happy-sad-privtest.csv", delimiter=",")
X_test = testset[:,0:2304]
Y_test = testset[:,2304]

# Load the public evaluation data (which we'll pass to predict()
predict_set = numpy.loadtxt("fer2013/happy-sad-pubtest.csv", delimiter=",")
Xp = predict_set[:,0:2304]
# Write the first 10 face images out to files "face-0.png" through "face-9.png"
for i in range(10):
  # print "Xp[i] = ", Xp[i]
  i48 = numpy.reshape(Xp[i], (48, 48,))
  iARGB = (i48.astype(int) * 0x010101) + 0xff000000
  saveAsPNG(iARGB, 'face-'+str(i)+'.png')
  # print "i48 = ", i48

# create model
model = Sequential()
model.add(Dense(12, input_dim=2304, init='normal', activation='relu'))
model.add(Dense(8, init='normal', activation='relu'))
model.add(Dense(1, init='normal', activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, nb_epoch=30, batch_size=100)

# evaluate the model
scores = model.evaluate(X, Y)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# evaluate test set
loss, accuracy = model.evaluate(X_test, Y_test)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))

# Run predictions!
Yp = model.predict(Xp)

for i in range(10):
  print "pubtest face # ", i, " prediction = ", Yp[i]

"""
 20161101.1253:
  I (Robert) got it to work once (after about 10 failures). Output
looks like this:

Using TensorFlow backend.
Epoch 1/10
12045/12045 [==============================] - 1s - loss: 0.6510 - acc: 0.6177
Epoch 2/10
12045/12045 [==============================] - 1s - loss: 0.6146 - acc: 0.6605
Epoch 3/10
12045/12045 [==============================] - 1s - loss: 0.5976 - acc: 0.6853
Epoch 4/10
12045/12045 [==============================] - 1s - loss: 0.5905 - acc: 0.6875
Epoch 5/10
12045/12045 [==============================] - 1s - loss: 0.5826 - acc: 0.6983
Epoch 6/10
12045/12045 [==============================] - 1s - loss: 0.5801 - acc: 0.6994
Epoch 7/10
12045/12045 [==============================] - 1s - loss: 0.5779 - acc: 0.7006
Epoch 8/10
12045/12045 [==============================] - 1s - loss: 0.5752 - acc: 0.7012
Epoch 9/10
12045/12045 [==============================] - 1s - loss: 0.5772 - acc: 0.6982
Epoch 10/10
12045/12045 [==============================] - 1s - loss: 0.5703 - acc: 0.7068
11712/12045 [============================>.] - ETA: 0sacc: 72.52%
1472/1473 [============================>.] - ETA: 0s
Loss: 0.56, Accuracy: 72.57%
('pubtest face # ', 0, ' prediction = ', array([ 0.69337708], dtype=float32))
('pubtest face # ', 1, ' prediction = ', array([ 0.15167654], dtype=float32))
('pubtest face # ', 2, ' prediction = ', array([ 0.09651949], dtype=float32))
('pubtest face # ', 3, ' prediction = ', array([ 0.07291968], dtype=float32))
('pubtest face # ', 4, ' prediction = ', array([ 0.60501647], dtype=float32))
('pubtest face # ', 5, ' prediction = ', array([ 0.43999442], dtype=float32))
('pubtest face # ', 6, ' prediction = ', array([ 0.47970647], dtype=float32))
('pubtest face # ', 7, ' prediction = ', array([ 0.58012635], dtype=float32))
('pubtest face # ', 8, ' prediction = ', array([ 0.58562624], dtype=float32))
('pubtest face # ', 9, ' prediction = ', array([ 0.15237312], dtype=float32))

"""
