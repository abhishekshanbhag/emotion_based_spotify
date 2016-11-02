The original data is from Kaggle:

  www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge

The data is described as follows:

  fer2013.tar  .gz (91.97 mb)

  The data consists of 48x48 pixel grayscale images of faces. The
  faces have been automatically registered so that the face is more or
  less centered and occupies about the same amount of space in each
  image. The task is to categorize each face based on the emotion
  shown in the facial expression in to one of seven categories
  (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral).

  train.csv contains two columns, "emotion" and "pixels". The
  "emotion" column contains a numeric code ranging from 0 to 6,
  inclusive, for the emotion that is present in the image. The
  "pixels" column contains a string surrounded in quotes for each
  image. The contents of this string a space-separated pixel values in
  row major order. test.csv contains only the "pixels" column and your
  task is to predict the emotion column.

  The training set consists of 28,709 examples. The public test set
  used for the leaderboard consists of 3,589 examples. The final test
  set, which was used to determine the winner of the competition,
  consists of another 3,589 examples.

  This dataset was prepared by Pierre-Luc Carrier and Aaron Courville,
  as part of an ongoing research project. They have graciously
  provided the workshop organizers with a preliminary version of their
  dataset to use for this contest.


Steps to create data files used by Andrew's code (which is in
../emotify_NN_training_v1.py) :

  cat fer2013.csv.gz | gunzip > fer2013.csv
  python gen1

This will generate the files:

  happy-sad-privtest.csv
  happy-sad-pubtest.csv
  happy-sad-training.csv

(No modules like numpy, etc. need to be installed; it's just reading
the CSV format data and parsing it directly)
