# Tensorflow pipeline 

This project aims to streamline the process of training of Tensorflow V2 deep neural network model from A to Z.  This project assumes you have already set up your system setup with the Python >= V3.5

pre_process.js is script that provides the sub-processes that help you through the entire process from having a labeled data set to generating the inference graph with a saved model that can be used in your nodejs application.

* Start with your image dataset
* Resize images (depending on your use case, smaller images size speeds up training time)
* Use tool like labelImag, Maximo Visual Inspection & etc. to label and create bounnding boxes for each class type for each image
* Break the dataset into a training set and a testing set (9:1 ratio)
* Covert csv files from xml files of the data set for generating TFRecord
* Generate TRecord
* Train model
* Generate inference graph from trained model 

labelImg /Users/jeff/git_repo/sandbox/wu/playbox/ml/TensorFlow/workspace/training_demo/images
python resize_images.py -d /Downloads/LFE/samples -s 800 600   

npm run pre_process --task=build_all --image_dir=/Users/jeff/Downloads/Demo_Augmented --origin=maximmo

npm run pre_process --task=train_model --pipeline_config_path=/Users/jeff/Downloads/Demo/ssd_efficientdet_d0_512x512_coco17_tpu-8.config --model_dir=/Users/jeff/Downloads/Demo/training

npm run pre_process --trained_checkpoint_dir=/User/jeff/Downloads/Demo2/training --pipeline_config_path=/Users/jeff/Downloads/Demo2/ssd_efficientdet_d0_512x512_coco17_tpu-8.config --output_directory=/Users/jeff/Downloads/Demo2/inference_graph --task=export_inference_graph

node webcam.js inference_graph/saved_saved_model/

npm run pre_process --task=build_all --image_dir=/Users/jeff/Downloads/demo-model/poor
npm run pre_process --task=build_all --image_dir=/Users/jeff/Downloads/demo-model/good -Origin=maximo

npm run pre_process --trained_checkpoint_dir=/Users/jeff/Downloads/demo-model/poor/training --pipeline_config_path=/Users/jeff/Downloads/demo-model/poor/ssd_efficientdet_d0_512x512_coco17_tpu-8.config --output_directory=/Users/jeff/Downloads/demo-model/poor/inference_graph --task=export_inference_graph

npm run pre_process --task=tflite_converter --saved_model_dir=/Users/jeff/Downloads/demo-model/poor/inference_graph/saved_model/ --output_path=/Users/jeff/Downloads/

tensorboard --logdir=/Users/jeff/Downloads/Demoaugmented/training/train 
tensorboard --logdir=/Users/jeff/Downloads/demo-model/poor/training/train

https://www.digikey.com/en/maker/projects/how-to-perform-object-detection-with-tensorflow-lite-on-raspberry-pi/b929e1519c7c43d5b2c6f89984883588
https://blog.roboflow.com/run-tensorflow-js-on-nvidia-jetson/

https://hub.docker.com/r/onerhao/ubuntu-dev

sudo apt install v4l-utils
v4l2-ctl --list-devices