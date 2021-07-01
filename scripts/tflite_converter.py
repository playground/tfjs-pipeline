from tensorflow.python.framework.versions import VERSION
if VERSION >= "2.0.0a0":
    import tensorflow.compat.v1 as tf
else:
    import tensorflow as tf

import os
import argparse

if __name__ == '__main__':
    print('Version: {}'.format(VERSION))
    parser = argparse.ArgumentParser(description="Convert Saved Model to TFLite")
    parser.add_argument('-d', '--saved_model_dir', type=str, required=True, help='Path to saved model')
    parser.add_argument('-s', '--output_path', type=str, required=True, help='Path to output TFLite model')
    args = parser.parse_args()

    # Convert the model
    converter = tf.lite.TFLiteConverter.from_saved_model(args.saved_model_dir) # path to the SavedModel directory
    tflite_model = converter.convert()

    # Save the model.
    tflite_filename = os.path.join(args.output_path, 'model.tflite');
    with open(tflite_filename, 'wb') as f:
        f.write(tflite_model)

    print('Successfully created the TFLite Model: {}'.format(tflite_filename))

