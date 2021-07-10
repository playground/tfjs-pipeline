from tensorflow.python.framework.versions import VERSION
if VERSION >= "2.0.0a0":
    import tensorflow as tf
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

    ## TFLite Conversion
    # Before conversion, fix the model input size
    model = tf.saved_model.load(args.saved_model_dir)
    model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs[0].set_shape([1, 300, 300, 3])
    tf.saved_model.save(model, "saved_model_updated", signatures=model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY])

    # Convert the model
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir='saved_model_updated', signature_keys=['serving_default'])
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
    tflite_model = converter.convert()
    
    # converter = tf.lite.TFLiteConverter.from_saved_model(args.saved_model_dir) # path to the SavedModel directory
    # converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # converter.experimental_new_converter = True
    # converter.target_spec.supported_ops = [
    #     tf.lite.OpsSet.TFLITE_BUILTINS,
    #     tf.lite.OpsSet.SELECT_TF_OPS,
    # ]   
    # tflite_model = converter.convert()

    # Save the model.
    tflite_filename = os.path.join(args.output_path, 'model.tflite');
    with open(tflite_filename, 'wb') as f:
        f.write(tflite_model)

    print('Successfully created the TFLite Model: {}'.format(tflite_filename))

