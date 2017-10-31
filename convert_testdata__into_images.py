from __future__ import print_function

import tensorflow as tf
import numpy
from skimage.io import imsave
from skimage.color import gray2rgb

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)
testdata = mnist.test.images

for im in range(len(testdata)):
    img = numpy.array([numpy.uint8(x*255) for x in testdata[im]])
    sq = img.reshape((28,28))
    rgb = gray2rgb(sq)
    imsave('/tmp/test/'+ str(im) +'.png', rgb)		   

