from classes import *
from functions import *
import json, argparse

medication = medication()

parser = argparse.ArgumentParser()
parser.add_argument("--init", action="store_true")
parser.add_argument("--infile", type=str)
parser.add_argument("--outfile", type=str)
args = parser.parse_args()



frames = [medication.name, medication.purpose, medication.dose, medication.frequency, medication.missed_dose,
          medication.duration, medication.warnings, medication.mild_side_effects, medication.dangerous_side_effects]

look_ahead = [2,0,2,0,1,1,1,1,1]

if args.init:
    answer = ""
    state = {"frame_index": 0, "nattempts": 0, "questions_remaining": 0}
else:
    answer = open(args.infile).read().strip()
    state = json.load(open("state.json"))


generate_reply(answer, state, frames, "lexical_overlap", args.init, look_ahead, args.outfile)