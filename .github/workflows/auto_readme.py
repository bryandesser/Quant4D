# generate README.rst for GitHub
file_list = ["index.rst", "installation.rst", "acknowledgement.rst"]

with open(file = "../../README.rst", mode = "w") as outfile:
    for filename in file_list:
        with open(file = filename, mode = "r") as infile:
            outfile.write(infile.read().split("Contents\n^^^^^^^^")[0])
        outfile.write("\n\n")
