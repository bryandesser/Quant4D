# open README.rst file for writing
with open(file = "./README.rst", mode = "w") as outfile:

    # add DOI sheild at the top
    outfile.write(".. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.15493504.svg\n")
    outfile.write("  :target: https://doi.org/10.5281/zenodo.15493504\n\n")

    # start with index page, make sure the Table of Contents toc tree is not
    # included
    with open(file = "./docs/source/index.rst", mode = "r") as infile:
        outfile.write(infile.read().split("Contents\n^^^^^^^^")[0].replace("../_static", "./docs/_static"))
        outfile.write("\n\n")
    
    # add a link to Read the Docs
    outfile.write("Documentation\n")
    outfile.write("=============\n\n")
    outfile.write("Quant4D documentation is available at `quant4d.readthedocs.io <https://quant4d.readthedocs.io/en/latest>`_.\n\n")

    # include installation documentation
    with open(file = "./docs/source/installation.rst", mode = "r") as infile:
        outfile.write(infile.read().replace("../_static", "./docs/_static"))
        outfile.write("\n\n")

    # include acknowledgement documentation
    with open(file = "./docs/source/acknowledgement.rst", mode = "r") as infile:
        outfile.write(infile.read().replace("../_static", "./docs/_static"))
