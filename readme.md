# Operationalizing TensorFlow-Based Digits Classifier Trained on MNIST Dataset 

This sample uses [TensorFlow](https://www.tensorflow.org/) and the [MNIST dataset](http://yann.lecun.com/exdb/mnist/) to train a neural network for classifying handwritten digits, and operationalizes the trained model into a RESTful web service. 

## Train the model locally

To use TensorFlow, one must install it. Open the command-line window by clicking on **File** --> **Open Command Prompt*. Then in local Python environment installed by Azure ML Workbench, type in the following command.
```
# Install tensorflow using pip, you only needed to do this once.
$ pip install tensorflow
```

Then run the training code `train.py`.
```
# submit the experiment to local execution environment.
$ az ml experiment submit -c local train.py
```

Pay attention to the code in `train.py`: The MNIST dataset is downloaded into `/tmp/data/`, and the trained model is saved into `/tmp/model/`. We name the trained model as `my_ConvNet_MNIST_model`, and under `/tmp/model/` you will find four model files `my_ConvNet_MNIST_model.data`, `my_ConvNet_MNIST_model.index`, `my_ConvNet_MNIST_model.meta`, and `checkpoint`.

If you decide to run `train.py` in a Docker container, you must also save the trained model files properly for operationalization.

For the convenience of the following steps, copy all four model files into the project home directory as the current working directory.

## Prepare for operationalization

To allow the web service to accept common image formats such as .jpg or .png as inputs, one must install [scikit-Image](http://scikit-image.org/). In the command-line window type in the following command.
```
# Install scikit-image libraries using pip, you only needed to do this once.
$ pip install scikit-image
```

Then one must compose the scoring code in the required webservice driver format, as shown in `webservice_driver.py`: In the `init()` function, the model files are loaded into a tensorflow session, and in the `run()` function, the byte stream received from the RESTful API submission is decoded into an image array and subsequently transformed into the appropriate format that the neural network accepts for scoring. The `run()` function returns the predicted digit, one between '0' and '9'.

To make sure the webservice driver works properly, one should run a few test cases. For this purpose, one must first convert the original MNIST data into a common image format so that images in this format be sent as inputs into the web service. In `convert_test_data_into_images.py`, all test data is converted into images in .png format and saved into '/tmp/test/'. A few samples from this step are available in the `./sampletestimages/` directory for visualization.  

We use these samples to run tests by executing `test.py`: In this file, an image `0.png` is read and encoded into the payload of the RESTful call, and subsequently submitted to the web servive driver. To run this test, simply type
```
# Run test using a sample image.
$ python test.py
```

IMPORTANT NOTE: The web service driver in this example only accepts image in the same size of 28\*28 as the original MNIST data. If one wishes to score an image in a different size, he/she must resize the image into 28\*28 before encoding the pixel values into the payload, or re-code the web service driver to handle image resizing.

## Deploy the scoring service

Now that the webservice driver works properly, one may proceed to deploy the scoring webservice according to the [instructions](https://docs.microsoft.com/en-us/azure/machine-learning/preview/deployment-setup-configuration). Pay attention to `conda_dependencies.yml` where both tensorflow and scikit-image must be declared. Also pay attention to the fact that all model files must be included in the deployment, and to this end one may run the following in the command line interface
```
# Deploy the trained model.
$ az ml service create realtime -m my_ConvNet_MNIST_model.meta -d my_ConvNet_MNIST_model.data -d my_ConvNet_MNIST_model.index -d checkpoint -f webservice_driver.py -n [your service name] -r python -c ./aml_config/conda_dependencies.yml
```

Wait until the deployment is complete, and collect two pieces of important information about your deployed webservice: Scoring URL and API key. To get the scoring URL, type
```
# Describe the usage of the deployed service
$ az ml service usage realtime --i [The Service ID shown after the completion of the deployment]
```
and to get the API Key, type
```
# Display the API key of the deployed service
$ az ml service keys realtime --i [The Service ID shown after the completion of the deployment]
```

Store the scoring URL and API key securely, and in the example they are saved in `webserviceparams.py`.

## Consume the web service

Congratulations! You are now all set to consume the web service you deployed. A python example to do so is shown in `webservice_invoke.py`. Simply run the following to give it a try.
```
# Consume the web service through python
$ python webservice_invoke.py
```