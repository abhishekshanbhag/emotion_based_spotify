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
