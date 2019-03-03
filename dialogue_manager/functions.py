# -*- coding: utf-8 -*-
from classes import *
from nltk.tokenize import word_tokenize
import json
from input_helpers import InputHelper

# Constants
welcome_message = "Hello and welcome to Health EdVisor. My name is Ed and I will be walking you through your medication " \
                  "today. I will be giving you a lot of important information, so I want to make sure you understand. " \
                  "I’ll be asking some questions as we go, just to make sure I am doing a good job of explaining how to " \
                  "take your medication."
wrong_answer_message = "You might have misheard me. Let me repeat it for you."
right_answer_message = "Great! Let's move on."
exit_message = "Seems like you're tired. Let's take this up another time."
skip_message = "Okay, let's skip this question."
done_message = "That brings us to the end of our session. Thank you for your participation!"

vocab_filepath = "../model/checkpoints/vocab"
batch_size = 64

def lexical_overlap(patient_answers, reference_answers, threshold = 0.5):
    for patient_answer in patient_answers:
        for reference_answer in reference_answers:
            nwords = 0.0
            reference_answer = reference_answer.split()
            for word in patient_answer.split():
                if word in reference_answer:
                    nwords += 1
            if nwords/len(reference_answer) >= threshold:
                return True
    return False

def siamese_network(patient_answers, reference_answers, sess, nodes):
    with open("nn_input.txt", "w") as outfile:
        for patient_answer in patient_answers:
            for reference_answer in reference_answers:
                outfile.write("0" + "\t" + patient_answer + "\t" + reference_answer + "\n")

    [input_x1, input_x2, input_y, dropout_keep_prob, predictions, accuracy, sim] = nodes

    inpH = InputHelper()
    x1_test, x2_test, y_test = inpH.getTestDataSet("nn_input.txt", vocab_filepath, 30)

    batches = inpH.batch_iter(list(zip(x1_test, x2_test, y_test)), 2 * batch_size, 1, shuffle=False)

    for db in batches:
        x1_dev_b, x2_dev_b, y_dev_b = zip(*db)

        batch_predictions, batch_acc, batch_sim = sess.run([predictions, accuracy, sim],
                                                           {input_x1: x1_dev_b, input_x2: x2_dev_b, input_y: y_dev_b,
                                                            dropout_keep_prob: 1.0})
        if sum(batch_sim)>0:
            return True
    return False


def evaluate_answer(reference_answers, evaluation_method, sess, nodes, lowercase = True, tokenize = True):
    patient_answers = [x.strip() for x in open("infile.txt").read().strip().split("\n")]
    if lowercase:
        patient_answers = [x.lower() for x in patient_answers]
        reference_answers = [x.lower() for x in reference_answers]
    if tokenize:
        patient_answers = [" ".join(word_tokenize(x)) for x in patient_answers]
        reference_answers = [" ".join(word_tokenize(x)) for x in reference_answers]
    if evaluation_method == "strict":
        if len(set(patient_answers) & set(reference_answers)) > 0:
            return True
    elif evaluation_method == "lexical_overlap":
        if lexical_overlap(patient_answers, reference_answers):
            return True
    elif evaluation_method == "siamese_network":
        if siamese_network(patient_answers, reference_answers, sess, nodes):
            return True
    return False


def generate_reply(state, frames, evaluation_method, look_ahead, sess, nodes):
    if open("infile.txt").read().strip() == "start":
        with open("outfile.txt", "w") as outfile:
            outfile.write("Ed: " + welcome_message + "\n")
            for i in range(look_ahead[0]):
                outfile.write("Ed: " + frames[i].statement + "\n")
            outfile.write("Ed: " + frames[0].question + "\n")
            state = {"frame_index": 0, "nattempts": 0, "questions_remaining": look_ahead[0]-1}
            json.dump(state, open("state.json", "w"))
    else:
        with open("outfile.txt", "w") as outfile:
            if evaluate_answer(frames[state["frame_index"]].answer, evaluation_method, sess, nodes):
                outfile.write("Ed: " + right_answer_message + "\n")
                state["frame_index"] += 1
                state["nattempts"] = 0
                if state["frame_index"] == len(frames):
                    outfile.write("Ed: " + done_message)
                    return
                if state["questions_remaining"] > 0:
                    state["questions_remaining"] -= 1
                    json.dump(state, open("state.json", "w"))
                    outfile.write("Ed: " + frames[state["frame_index"]].question)
                else:
                    state["questions_remaining"] = look_ahead[state["frame_index"]] - 1
                    json.dump(state, open("state.json", "w"))
                    for i in range(look_ahead[state["frame_index"]]):
                        outfile.write("Ed: " + frames[state["frame_index"] + i].statement + "\n")
                    outfile.write("Ed: " + frames[state["frame_index"]].question + "\n")
            else:
                state["nattempts"] += 1
                #if state["nattempts"] == 3:
                #    outfile.write("Ed: " + exit_message)
                #    exit()
                if state["nattempts"] == 3:
                    outfile.write("Ed: " + skip_message + "\n")
                    state["frame_index"] += 1
                    state["nattempts"] = 0
                    if state["frame_index"] == len(frames):
                        outfile.write("Ed: " + done_message)
                        exit()
                    if state["questions_remaining"] > 0:
                        state["questions_remaining"] -= 1
                        json.dump(state, open("state.json", "w"))
                        outfile.write("Ed: " + frames[state["frame_index"]].question)
                    else:
                        state["questions_remaining"] = look_ahead[state["frame_index"]] - 1
                        json.dump(state, open("state.json", "w"))
                        for i in range(look_ahead[state["frame_index"]]):
                            outfile.write("Ed: " + frames[state["frame_index"] + i].statement + "\n")
                        outfile.write("Ed: " + frames[state["frame_index"]].question + "\n")
                else:
                    json.dump(state, open("state.json", "w"))
                    outfile.write("Ed: " + wrong_answer_message + "\n")
                    outfile.write("Ed: " + frames[state["frame_index"]].statement + "\n")
                    outfile.write("Ed: " + frames[state["frame_index"]].question + "\n")
