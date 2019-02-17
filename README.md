# edvisor

This is the code for the in-house dialogue manager for Health EdVisor.

## Quick Start:

To start the dialogue, run the following command:

```
python3 main.py --init --outfile <outfile_path>
```

This command would generate the text to be spoken by Ed into the file specified by <outfile_path>.

When an answer is uttered by the patient, save the text of that answer in <infile_path> and run the following command:

```
python3 main.py --infile <infile_path> --outfile <outfile_path>
```

This will generate Ed's response in the file specified by <outfile_path>.

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

