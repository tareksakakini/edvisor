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
import sys

medication_name = sys.argv[1]
mode = sys.argv[2]

medication_database = json.load(open("medication_database.json"))

medication = medication(medication_database[medication_name])

#frames = [medication.name, medication.purpose, medication.dose, medication.frequency, medication.missed_dose,
#          medication.duration, medication.warnings, medication.mild_side_effects, medication.dangerous_side_effects]

#look_ahead = [2,0,2,0,1,1,1,1,1]

frames = [medication.name, medication.purpose, medication.dose, medication.frequency]

look_ahead = [2,0,2,0]

state = {"frame_index": 0, "nattempts": 0, "questions_remaining": 0}
json.dump(state, open("state.json", "w"))

checkpoint_file = "../model/checkpoints/model-10000"

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

        nodes = [input_x1, input_x2, input_y, dropout_keep_prob, predictions, accuracy, sim]

        while True:
            if "pipeline_status.txt" in os.listdir("."):
                if open("pipeline_status.txt").read().strip() == "input updated":
                    state = json.load(open("state.json"))
                    generate_reply(state, frames, "lexical_overlap_w_synonymy", look_ahead, sess, nodes, mode)
                    with open("pipeline_status.txt", "w") as outfile_status:
                        outfile_status.write("output updated")