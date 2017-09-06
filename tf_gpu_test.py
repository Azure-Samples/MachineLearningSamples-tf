# To run the below script on GPU in a Docker container on a Linux VM, do the following:
# In conda_dependencies.yml file, using tensorflow-gpu (vs. tensorflow)
# In your GPU VM .compute file, set teh baseDockerImage to nvidia/cuda:8.0-cudnn6-devel-ubuntu16.04
# In your GPU VM .compute file, add a line: nvidiaDocker: true
# And, in your GPU VM .runconfig file, make sure the Framework is set to "Python" (vs. "PySpark")

import tensorflow as tf

with tf.device('/gpu:0'):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape = [2, 3], name = 'a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape = [3, 2], name = 'b')
    c = tf.matmul(a, b)
	
sess = tf.Session(config = tf.ConfigProto(log_device_placement = True))
print("RESULTS using GPU:")
print(sess.run(c))
