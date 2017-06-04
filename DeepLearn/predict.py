import os, cv2, sys
import numpy as np
import mysql.connector
import requests
import re
from keras.models import model_from_json
from keras.models import load_model

from keras import backend as K
K.set_image_dim_ordering('th')

def predict(argv):
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights("model.h5")
    # print "Loaded model from disk"

    PATH = os.getcwd()
    data_path = PATH + '/data'
    data_dir_list = os.listdir(data_path)

    num_channel = 1

    # Testing a new image
    image = argv
    test_image = cv2.imread(image)
    test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    test_image = cv2.resize(test_image,(128,128))
    test_image = np.array(test_image)
    test_image = test_image.astype('float32')
    test_image /= 255
    # print test_image.shape

    if num_channel == 1:
        if K.image_dim_ordering()=='th':
            test_image= np.expand_dims(test_image, axis=0)
            test_image= np.expand_dims(test_image, axis=0)
            # print test_image.shape
        else:
            test_image= np.expand_dims(test_image, axis=3)
            test_image= np.expand_dims(test_image, axis=0)
            # print test_image.shape

    else:
        if K.image_dim_ordering()=='th':
            test_image=np.rollaxis(test_image,2,0)
            test_image= np.expand_dims(test_image, axis=0)
            # print test_image.shape
        else:
            test_image= np.expand_dims(test_image, axis=0)
            print (test_image.shape)

    # Predicting the test image
    probability = loaded_model.predict(test_image)
    class_name = data_dir_list[int(loaded_model.predict_classes(test_image))]
    # print data_dir_list
    # print probability[0].max(axis=0)
    return probability[0].max(axis=0), class_name


if __name__ == '__main__':
    probability, class_name = predict(sys.argv[1])
    cnx = mysql.connector.connect(user="osheenchavhan@icmiamigos", password="GHOSTman@1997", host="icmiamigos.mysql.database.azure.com", port=3306, database="miamigos")
    cursor = cnx.cursor()
    SQLCommand = ("insert into imageres (uid,percentage,result) values (%s,%s,%s)")
    cursor.execute(SQLCommand,(sys.argv[1], probability, class_name)
    cnx.commit()
    #closing cursor
    cursor.close()
    #closing connection
    f= open("result.txt","w")
    f.write(str(probability))
    f.write(class_name)
    print (sys.argv[1], probability, class_name)
