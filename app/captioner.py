import sys
import numpy as np
from numpy import array
import pandas as pd
#import matplotlib.pyplot as plt
import string
import os
sys.path.append('/home/Laii/.local/lib/python3.7/site-packages/')
sys.path.append('/usr/.local/lib/python3.7/dist-packages')
from PIL import Image
import glob
from pickle import dump, load
from time import time
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import LSTM, Embedding, TimeDistributed, Dense, RepeatVector,\
                         Activation, Flatten, Reshape, concatenate, Dropout, BatchNormalization
from keras.optimizers import Adam, RMSprop
from keras.layers.wrappers import Bidirectional
from keras.layers.merge import add
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras import Input, layers
from keras import optimizers
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

def captioner():
    fileimgtxt = "app/imagetext.txt"
    doc = load_doc(fileimgtxt)
    descriptions = load_descriptions(doc)
    clean_descriptions(descriptions)
    vocabulary = to_vocabulary(descriptions)
    save_descriptions(descriptions, 'app/descriptions.txt')
    filetraintxt = "app/trainImages.txt"
    train = load_set(filetraintxt)
    print('Dataset: %d' %len(train))


def load_doc(filename):
    #open file of image text set
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

def load_descriptions(doc):
    mapping = dict()
    for line in doc.split('\n'):
        #split lines by the white space
        tokens = line.split()
        if len(line) < 2:
            continue
        # take the first token as the image id, the rest as the description
        image_id, image_desc = tokens[0], tokens[1:]
		# extract filename from image id
        image_id = image_id.split('.')[0]
		# convert description tokens back to string
        image_desc = ' '.join(image_desc)
		# create the list if needed
        if image_id not in mapping:
            mapping[image_id] = list()
		# store description
        mapping[image_id].append(image_desc)
    return mapping

def clean_descriptions(descriptions):
    #translation table for removing punct
    table = str.maketrans('','',string.punctuation)
    for key, desc_list in descriptions.items():
        for i in range(len(desc_list)):
            desc = desc_list[i]
            #tokens
            desc = desc.split()
            #lowercase
            desc = [word.lower() for word in desc]
            #remove punct
            desc = [w.translate(table) for w in desc]
            #remove 's' and 'a'
            desc = [word for word in desc if len(word)>1]
            #remove tokens with numbes
            desc = [word for word in desc if word.isalpha()]
            #make string
            desc_list[i] = ' '.join(desc)

#descriptions to vocab
def to_vocabulary(descriptions):
    #build list of all desc strings
    all_desc = set()
    for key in descriptions.keys():
        [all_desc.update(d.split()) for d in descriptions[key]]
    return all_desc

#save descs to file
def save_descriptions(descriptions, filename):
    lines = list()
    for key, desc_list in descriptions.items():
        for desc in desc_list:
            lines.append(key + ' ' + desc)
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()
#load the descriptions
def load_set(filename):
    doc = load_doc(filename)
    dataset = list()
    for line in doc.split('\n'):
        if len(line) < 1:
            continue
        #get image identifier
        identifier = line.split('.')[0]
        dataset.append(identifier)
    return set(dataset)
