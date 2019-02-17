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
