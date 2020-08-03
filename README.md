# edvisor

This repo includes the code to control the dialogue of the conversational agent: Edna. The basic functionality is that at first, Edna introduces herself. Then she gives pieces of medication information (frames), followed by questions on each frame. Edna will then wait for the answer of the user. If the answer is accurate, Edna moves on to the next frame, otherwise, Edna repeats and questions the user again.

The script, now, will be running always in the background. This is necessary to avoid loading the tensorflow graph every time we want to generate an answer. The way to communicate with this script will be through three files: infile.txt, outfile.txt, and pipeline_status.txt. All three files should be placed in the directory "dialogue_manager". infile.txt will be our way to feed in the answers to Edna. outfile.txt will be our way to read in the replies from Edna. pipeline_status.txt will be our way to tell the script that an answer has been generated ("input generated") for it to act on it, as well as the script way to tell us that a reply has been generated for us ("output generated") to act on.

## Quick Start:

First, download the neural network [model](https://uofi.box.com/s/oiduby74s6ej8sb99mzpja9319okjhwy), unzip it (make sure the directory's name is "model"), and place it as a sibling directory to "dialogue_manager". Then kickstart the script in the background. The script takes in two arguments <medication_name> (options: metformin, insulin_lispro, empagliflozin), <mode_of_operation> (options: teachback, no_questions, no_evaluation), and <warm_up_mode> (options: warm_up, no_warm_up, acquainted). In teachback, the patient is asked questions, and his/her answer is evaluated. In no_questions, the patient is not required to answer any questions, and the information is just fed in one shot. In no_evaluation, the patient is asked questions, but his/her answer is not evaluated and always replied to by "Thank you for your answer". As for <warm_up_mode>, warm_up is used when we want to warm up the patient the first time they're interacting with Edna. no_warm_up is what we used to do, self introduction of Edna and no interaction with the patient until the first question. acquainted is the mode needed we don't want to introduce Edna and we don't want to ask warm up questions. acquainted should be used for the second medication in the study:

```
cd dialogue_manager
python main.py <medication_name> <mode_of_operation> <warm_up_mode>
```

To start the conversation, write "start" into the file "infile.txt", and write "input generated" into the file "pipeline_status.txt". Even if these files existed, overwrite them with these messages. Then, the script will generate its welcoming message in the file "outfile.txt", and it will adjust the content of "pipeline_status.txt" to "output generated" for you to know that Edna's output has been generated/updated.

P.S. with warm_up mode, you'll need to keep writing "start" into the file "infile.txt" until the end of the warm up stage, which is right after Edna asks the first question. In other words, with warm_up, "start" will be used three times instead of once.

To continue the conversation, repeat the previous step (i.e. update the files "infile.txt" and "pipeline_status.txt"), but now have the patient's answer (or answers for multiple hypotheses) in "infile.txt".

Your script/GUI will have to keep checking "pipeline_status.txt" for the message "output generated" for it to act on it.

## Testing:

For testing purposes, here are the answers to the questions of Ed. Having a lexical overlap above 50% with the reference answer will warrant a positive response.

Q: "What is your medication called?"<br/>
A: "Metformin"

Q: "How does your medication treat your diabetes?"<br/>
A: "By controlling the amount of sugar in my blood."

Q: "How many tablets should you take in one time?"<br/>
A: "One tablet"

Q: "How many times should you take the medicine in one day?"<br/>
A: "Two times"

Q: "You forgot to take your medication and it is almost time for the next dose. How many tablets should you take?"<br/>
A: "Only one tablet"

Q: "What should you do if you feel better after taking your medication for a while?"<br/>
A: "I should ask my doctor if I can stop taking it"
    
Q: "Is it important to eat a healthy diet for your condition?"<br/>
A: "Yes"

Q: "What is an expected side effect?"<br/>
A: "Diarrhea or metallic taste"

Q: "What is a serious side effect?"<br/>
A: "Itching or hives"

