# generate README.rst for GitHub
file_list = ["./docs/source/index.rst", "./docs/source/installation.rst", "./docs/source/acknowledgement.rst"]

with open(file = "./README.rst", mode = "w") as outfile:
    outfile.write(".. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.15493504.svg\n")
    outfile.write("  :target: https://doi.org/10.5281/zenodo.15493504\n\n")
    for filename in file_list:
        with open(file = filename, mode = "r") as infile:
            outfile.write(infile.read().split("Contents\n^^^^^^^^")[0].replace("../_static", "./docs/_static"))
        outfile.write("\n\n")
