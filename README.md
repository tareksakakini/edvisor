# edvisor

This is the code for the in-house dialogue manager for Health EdVisor. The script, now, will be running always in the background. This is necessary to avoid loading the tensorflow graph every time we want to generate an answer. The way to communicate with this script will be through three files: infile.txt, outfile.txt, and pipeline_status.txt. All three files should be placed in the directory "dialogue_manager". infile.txt will be our way to feed in the answers to Ed. outfile.txt will be our way to read in the replies from Ed. pipeline_status.txt will be our way to tell the script that an answer has been generated ("input generated") for it to act on it, as well as the script way to tell us that a reply has been generated for us ("output generated") to act on.

## Quick Start:

First, download the neural network [model](https://uofi.box.com/s/oiduby74s6ej8sb99mzpja9319okjhwy), unzip it (make sure the directory's name is "model"), and place it as a sibling directory to "dialogue_manager". Then kickstart the script in the background. The script takes in two arguments <medication_name> (options: metformin, insulin_lispro, empagliflozin), and <mode_of_operation> (options: teachback, no_questions, no_evaluation). In teachback, the patient is asked questions, and his/her answer is evaluated. In no_questions, the patient is not required to answer any questions, and the information is just fed in one shot. In no_evaluation, the patient is asked questions, but his/her answer is not evaluated and always replied to by "Thank you for your answer":

```
cd dialogue_manager
python main.py <medication_name> <mode_of_operation>
```

To start the conversation, write "start" into the file "infile.txt", and write "input generated" into the file "pipeline_status.txt". Even if these files existed, overwrite them with these messages. Then, the script will generate its welcoming message in the file "outfile.txt", and it will adjust the content of "pipeline_status.txt" to "output generated" for you to know that Ed's output has been generated/updated.

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

