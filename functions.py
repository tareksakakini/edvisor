from classes import *
from nltk.tokenize import word_tokenize
import json

# Constants
welcome_message = "Hello and welcome to Health EdVisor. My name is Ed and I will be walking you through your medication today."
wrong_answer_message = "Seems like you have misunderstood this part. Let me repeat it for you."
right_answer_message = "That is correct! Let's move on."
exit_message = "Seems like you're tired. Let's take this up another time."

def lexical_overlap(patient_answer, reference_answer, threshold = 0.5):
    nwords = 0
    reference_answer = reference_answer.split()
    for word in patient_answer.split():
        if word in reference_answer:
            nwords += 1
    return nwords/len(reference_answer) > threshold

def evaluate_answer(patient_answer, reference_answer, evaluation_method, lowercase = True, tokenize = True):
    if lowercase:
        patient_answer = patient_answer.lower()
        reference_answer = reference_answer.lower()
    if tokenize:
        patient_answer = " ".join(word_tokenize(patient_answer))
        reference_answer = " ".join(word_tokenize(reference_answer))
    if evaluation_method == "strict":
        return patient_answer == reference_answer
    elif evaluation_method == "lexical_overlap":
        return lexical_overlap(patient_answer, reference_answer)

def generate_reply(answer, state, frames, evaluation_method, initial_state, look_ahead, outfile_path):
    if initial_state:
        with open(outfile_path, "w") as outfile:
            outfile.write("Ed: " + welcome_message + "\n")
            for i in range(look_ahead[0]):
                outfile.write("Ed: " + frames[i].statement + "\n")
            outfile.write("Ed: " + frames[0].question + "\n")
            state = {"frame_index": 0, "nattempts": 0, "questions_remaining": look_ahead[0]-1}
            json.dump(state, open("state.json", "w"))
    else:
        with open(outfile_path, "w") as outfile:
            if evaluate_answer(answer, frames[state["frame_index"]].answer, evaluation_method):
                outfile.write("Ed: " + right_answer_message + "\n")
                state["frame_index"] = state["frame_index"] + 1
                state["nattempts"] = 0
                if state["questions_remaining"] > 0:
                    state["questions_remaining"] = state["questions_remaining"] - 1
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
                if state["nattempts"] == 3:
                    outfile.write("Ed: " + exit_message)
                    exit()
                json.dump(state, open("state.json", "w"))
                outfile.write("Ed: " + wrong_answer_message + "\n")
                outfile.write("Ed: " + frames[state["frame_index"]].statement + "\n")
                outfile.write("Ed: " + frames[state["frame_index"]].question + "\n")
