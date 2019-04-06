# -*- coding: utf-8 -*-
from classes import *
from nltk.tokenize import word_tokenize
import json
from input_helpers import InputHelper
from nltk.stem.porter import *
import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

# Constants
welcome_message = "Hello and welcome to Health EdVisor. My name is Ed and I will be walking you through your medication " \
                  "today. I will be giving you a lot of important information, so I want to make sure you understand. " \
                  "I’ll be asking some questions as we go, just to make sure I am doing a good job of explaining how to " \
                  "take your medication."
wrong_answer_message = "You might have misheard me. Let me repeat it for you."
right_answer_message = "Great! That is correct."
next_statement_message = "Here is some more information."
next_question_message = "Let's move on to the next question."
exit_message = "Seems like you're tired. Let's take this up another time."
skip_message = "Okay, let's skip this question."
done_message = "That brings us to the end of our session. Thank you for your participation!"
no_evaluation_message = "Thank you for your answer!"

vocab_filepath = "../model/checkpoints/vocab"
batch_size = 64

stemmer = PorterStemmer()
stopwords_english = stopwords.words('english')

def get_synonyms(word):
    synonyms = [word]
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return list(set(synonyms))

def expand_word_list(word_list):
    return {word: get_synonyms(word) for word in word_list}

def explain_evaluation(patient_answer, reference_answer, original_patient_answer, original_reference_answer, matches):
    with open("explanation.txt", "w") as outfile:
        outfile.write("Original Patient Answer: " + original_patient_answer + "\n")
        outfile.write("Original Reference Answer: " + original_reference_answer + "\n")
        outfile.write("Processed Patient Answer: " + " ".join(patient_answer) + "\n")
        outfile.write("Processed Reference Answer: " + " ".join(reference_answer) + "\n")
        outfile.write("Match Level: " + str(len(matches)) + "(" + str(100*float(len(matches))/len(reference_answer)) + "%)\n")
        outfile.write("Matching Words:\n")
        for match in matches:
            outfile.write(match[0] + "--" + match[1] + ": " + ", ".join(match[2]) + "\n")
    return


def lexical_overlap_with_synonymy(patient_answers, reference_answers, original_patient_answers, original_reference_answers, threshold = 0.5):

    best_match = 0.0
    best_matches = []
    best_patient_ind = -1
    best_reference_ind = -1

    for i, patient_answer in enumerate(patient_answers):
        patient_answer = patient_answer.split()
        patient_answer_syns = expand_word_list(patient_answer)
        for j, reference_answer in enumerate(reference_answers):
            matches = []
            reference_answer = reference_answer.split()
            reference_answer_syns = expand_word_list(reference_answer)
            for word_reference in reference_answer:
                for word_patient in patient_answer:
                    intersection = set(patient_answer_syns[word_patient]) & set(reference_answer_syns[word_reference])
                    if len(intersection) > 0:
                        matches.append((word_patient, word_reference, intersection))
                        break
            if float(len(matches))/len(reference_answer) >= threshold:
                explain_evaluation(patient_answer, reference_answer, original_patient_answers[i], original_reference_answers[j], matches)
                return True
            if float(len(matches)) / len(reference_answer) >= best_match:
                best_match = float(len(matches)) / len(reference_answer)
                best_matches = matches
                best_patient_ind = i
                best_reference_ind = j
    explain_evaluation(patient_answers[best_patient_ind].split(), reference_answers[best_reference_ind].split(), original_patient_answers[best_patient_ind], original_reference_answers[best_reference_ind], best_matches)
    return False

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


def evaluate_answer(reference_answers, evaluation_method, sess, nodes, lowercase = True, tokenize = True, stem = False, remove_stop_words = True):
    patient_answers = [x.strip() for x in open("infile.txt").read().strip().split("\n")]
    original_patient_answers = [x for x in patient_answers]
    patient_answers = [x.translate(None, string.punctuation) for x in patient_answers]
    original_reference_answers = [str(x) for x in reference_answers]
    reference_answers = [str(x).translate(None, string.punctuation) for x in reference_answers]

    if lowercase:
        patient_answers = [x.lower() for x in patient_answers]
        reference_answers = [x.lower() for x in reference_answers]
    if tokenize:
        patient_answers = [" ".join(word_tokenize(x)) for x in patient_answers]
        reference_answers = [" ".join(word_tokenize(x)) for x in reference_answers]
    if remove_stop_words:
        patient_answers = [" ".join([y for y in x.split() if y not in stopwords_english]) for x in patient_answers]
        reference_answers = [" ".join([y for y in x.split() if y not in stopwords_english]) for x in reference_answers]
    if stem:
        patient_answers = [" ".join([stemmer.stem(y).decode("utf-8") for y in x.split()]) for x in patient_answers]
        reference_answers = [" ".join([stemmer.stem(y).decode("utf-8") for y in x.split()]) for x in reference_answers]
    if evaluation_method == "strict":
        if len(set(patient_answers) & set(reference_answers)) > 0:
            return True
    elif evaluation_method == "lexical_overlap":
        if lexical_overlap(patient_answers, reference_answers):
            return True
    elif evaluation_method == "lexical_overlap_w_synonymy":
        if lexical_overlap_with_synonymy(patient_answers, reference_answers, original_patient_answers, original_reference_answers):
            return True
    elif evaluation_method == "siamese_network":
        if siamese_network(patient_answers, reference_answers, sess, nodes):
            return True
    return False


def generate_reply(state, frames, evaluation_method, look_ahead, sess, nodes, mode):
    if mode == "teachback":
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
                        outfile.write("Ed: " + next_question_message + "\n")
                        outfile.write("Ed: " + frames[state["frame_index"]].question)
                    else:
                        outfile.write("Ed: " + next_statement_message + "\n")
                        state["questions_remaining"] = look_ahead[state["frame_index"]] - 1
                        json.dump(state, open("state.json", "w"))
                        for i in range(look_ahead[state["frame_index"]]):
                            outfile.write("Ed: " + frames[state["frame_index"] + i].statement + "\n")
                        outfile.write("Ed: " + frames[state["frame_index"]].question + "\n")
                else:
                    state["nattempts"] += 1
                    if state["nattempts"] == 2:
                        outfile.write("Ed: " + skip_message + "\n")
                        state["frame_index"] += 1
                        state["nattempts"] = 0
                        if state["frame_index"] == len(frames):
                            outfile.write("Ed: " + done_message)
                            return
                        if state["questions_remaining"] > 0:
                            state["questions_remaining"] -= 1
                            json.dump(state, open("state.json", "w"))
                            outfile.write("Ed: " + next_question_message + "\n")
                            outfile.write("Ed: " + frames[state["frame_index"]].question)
                        else:
                            state["questions_remaining"] = look_ahead[state["frame_index"]] - 1
                            json.dump(state, open("state.json", "w"))
                            outfile.write("Ed: " + next_statement_message + "\n")
                            for i in range(look_ahead[state["frame_index"]]):
                                outfile.write("Ed: " + frames[state["frame_index"] + i].statement + "\n")
                            outfile.write("Ed: " + frames[state["frame_index"]].question + "\n")
                    else:
                        json.dump(state, open("state.json", "w"))
                        outfile.write("Ed: " + wrong_answer_message + "\n")
                        outfile.write("Ed: " + frames[state["frame_index"]].statement + "\n")
                        outfile.write("Ed: " + frames[state["frame_index"]].question + "\n")

    elif mode == "no_questions":
        if open("infile.txt").read().strip() == "start":
            with open("outfile.txt", "w") as outfile:
                outfile.write("Ed: " + welcome_message + "\n")
                for i in range(len(frames)):
                    outfile.write("Ed: " + frames[i].statement + "\n")
                outfile.write("Ed: " + done_message)

    elif mode == "no_evaluation":
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
                outfile.write("Ed: " + no_evaluation_message + "\n")
                state["frame_index"] += 1
                state["nattempts"] = 0
                if state["frame_index"] == len(frames):
                    outfile.write("Ed: " + done_message)
                    return
                if state["questions_remaining"] > 0:
                    state["questions_remaining"] -= 1
                    json.dump(state, open("state.json", "w"))
                    outfile.write("Ed: " + next_question_message + "\n")
                    outfile.write("Ed: " + frames[state["frame_index"]].question)
                else:
                    outfile.write("Ed: " + next_statement_message + "\n")
                    state["questions_remaining"] = look_ahead[state["frame_index"]] - 1
                    json.dump(state, open("state.json", "w"))
                    for i in range(look_ahead[state["frame_index"]]):
                        outfile.write("Ed: " + frames[state["frame_index"] + i].statement + "\n")
                    outfile.write("Ed: " + frames[state["frame_index"]].question + "\n")

