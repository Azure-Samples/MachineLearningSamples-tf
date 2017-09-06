# Classify MNIST dataset using TensorFlow

Run tf_mnist.py in local conda environment.
```
$ pip install tensorflow
$ az ml experiment submit -c local tf_mnist.py
```

Run tf_mnist.py in a local Docker container.
```
$ az ml experiment submit -c docker tf_mnist.py
```

Run tf_mnist.py in a Docker container in a remote machine. Note you need to create/configure myvm.compute.
```
$ az ml experiment submit -c myvm tf_mnist.py
```

Run tf_mnist.py in a Docker container in a remote machine with GPU.
- Create a new compute context, nam it _gpu_ (or any arbitary name)
- Use _az ml computetarget attach_ to target the GPU equipped VM.
- In **conda_dependencies.yml** file, use _tensorflow-gpu_ instead of _tensorflow_.
- In **gpu.compute** file, use _microsoft/mmlspark:gpu_ as the base Docker image.
- In **gpu.compute** file, add a line _nvidiaDocker: true_
- In **gpu.runconfig** file, set _Framework_ to _Python_
- Now run the script.
```
$ az ml experiment submit -c gpu tf_mnist.py
```

For more information on using GPU in Vienna execution, read [this article](https://github.com/Azure/ViennaDocs/blob/master/Documentation/gpu-execution.md).
