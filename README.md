npm run pre_process --task=build_all --image_dir=/Users/jeff/Downloads/Demo_Augmented --origin=maximmo

npm run pre_process --task=train_model --pipeline_config_path=/Users/jeff/Downloads/Demo/ssd_efficientdet_d0_512x512_coco17_tpu-8.config --model_dir=/Users/jeff/Downloads/Demo/training

npm run pre_process --trained_checkpoint_dir=/User/jeff/Downloads/Demo2/training --pipeline_config_path=/Users/jeff/Downloads/Demo2/ssd_efficientdet_d0_512x512_coco17_tpu-8.config --output_directory=/Users/jeff/Downloads/Demo2/inference_graph --task=export_inference_graph

node webcam.js inference_graph/saved_saved_model/

npm run pre_process --task=build_all --image_dir=/Users/jeff/Downloads/demo-model/poor
npm run pre_process --task=build_all --image_dir=/Users/jeff/Downloads/demo-model/good -Origin=maximo

tensorboard --logdir=/Users/jeff/Downloads/Demoaugmented/training/train 
tensorboard --logdir=/Users/jeff/Downloads/demo-model/poor/training/train