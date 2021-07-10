#based on https://github.com/datitran/raccoon_dataset/blob/master/generate_tfrecord.py

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import argparse

import pandas as pd

import tensorflow.compat.v2 as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict


def class_text_to_int(row_label):
    if row_label == 'hard-hat' or row_label == 'hardhat':
        return 1
    elif row_label == 'mask':
        return 2
    elif row_label == 'person':
        return 3
    elif row_label == 'vest':
        return 4
    elif row_label == 'head':
        return 5
    elif row_label == 'lab_coat':
        return 6
    elif row_label == 'badge':
        return 7
    else:
        return 0


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate tfrecord")
    parser.add_argument('-c', '--csv_input', type=str, required=True, help='Path to the CSV input')
    parser.add_argument('-o', '--output_path', type=str, required=True, help='Path to output TFRecord')
    parser.add_argument('-i', '--image_dir', type=str, required=True, help='Path to images')
    args = parser.parse_args()

    writer = tf.io.TFRecordWriter(args.output_path)
    path = os.path.join(args.image_dir)
    print('csv file', args.csv_input)
    examples = pd.read_csv(args.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), args.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))

