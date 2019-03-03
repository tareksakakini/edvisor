#! /usr/bin/env python

from classes import *
from functions import *
import json
import tensorflow as tf
import numpy as np
import os
import time
import datetime
from tensorflow.contrib import learn


medication = medication()

frames = [medication.name, medication.purpose, medication.dose, medication.frequency, medication.missed_dose,
          medication.duration, medication.warnings, medication.mild_side_effects, medication.dangerous_side_effects]

look_ahead = [2,0,2,0,1,1,1,1,1]

state = {"frame_index": 0, "nattempts": 0, "questions_remaining": 0}

checkpoint_file = "../model/checkpoints/model-10000"
vocab_filepath = "../model/checkpoints/vocab"
batch_size = 64

print checkpoint_file
graph = tf.Graph()
with graph.as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=True,
      log_device_placement=False)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # Load the saved meta graph and restore variables
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        sess.run(tf.initialize_all_variables())
        saver.restore(sess, checkpoint_file)

        # Get the placeholders from the graph by name
        input_x1 = graph.get_operation_by_name("input_x1").outputs[0]
        input_x2 = graph.get_operation_by_name("input_x2").outputs[0]
        input_y = graph.get_operation_by_name("input_y").outputs[0]

        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
        # Tensors we want to evaluate
        predictions = graph.get_operation_by_name("output/distance").outputs[0]

        accuracy = graph.get_operation_by_name("accuracy/accuracy").outputs[0]

        sim = graph.get_operation_by_name("accuracy/temp_sim").outputs[0]

        while True:
            input1 = raw_input("first sentence: ")
            input2 = raw_input("second sentence: ")
            with open("nn_demo_input.txt", "w") as outfile:
                outfile.write("0" + "\t" + input1 + "\t" + input2 + "\n")

            inpH = InputHelper()
            x1_test, x2_test, y_test = inpH.getTestDataSet("nn_demo_input.txt", vocab_filepath, 30)

            batches = inpH.batch_iter(list(zip(x1_test, x2_test, y_test)), 2 * batch_size, 1, shuffle=False)

            for db in batches:
                x1_dev_b, x2_dev_b, y_dev_b = zip(*db)

                batch_predictions, batch_acc, batch_sim = sess.run([predictions, accuracy, sim],
                                                                   {input_x1: x1_dev_b, input_x2: x2_dev_b,
                                                                    input_y: y_dev_b,
                                                                    dropout_keep_prob: 1.0})
                print(batch_sim)
                if sum(batch_sim) > 0:
                    print("correct")
                else:
                    print("wrong")