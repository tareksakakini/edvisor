with open("infile.txt", "w") as infile:
    #infile.write("0\tone tablet a day\tone tablet")
    infile.write("star")

with open("pipeline_status.txt", "w") as status_file:
    status_file.write("input updated")