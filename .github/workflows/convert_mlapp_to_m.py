from zipfile import ZipFile
import xml.etree.ElementTree as ET
import tempfile
import os
from typing import List, Tuple

def convert_mlapp_to_m(source_file: str | os.PathLike) -> Tuple[List, str]:
    """ convert a .mlapp file to a human readable .m file """

    # check that .mlapp exists
    if not os.path.exists(source_file):
        return (None, ".mlapp file does not exist!")
    
    # unzip the .mlapp file
    with tempfile.TemporaryDirectory() as temp_dir:
        with ZipFile(source_file, "r") as zip_object:
            zip_object.extractall(path = temp_dir)
        
        # check if `document.xml` exists 
        xml_path = temp_dir + os.sep + "matlab/document.xml"
        if not os.path.exists(xml_path):
            return (None, "./matlab/document.xml not found.")

        # parse `document.xml` for full codebase        
        root = ET.parse(xml_path).getroot()

        code = None

        # automatically search {xmlns}t for code
        code_element = root.find(".//"+root.find(".").tag.replace("document","t"))

        # extract code from .xml
        if code_element is not None:
            code = code_element.text
        else:
            # if auto search fails, iterate through elements looking for the `classdef`
            for element in root.iter():
                if element.text and "classdef" in element.text:
                    code = element.text

    if code is None:
        return (None, "No code found!")
    
    # write code to Quant4D.m
    with open("./docs/source/Quant4D.m", "w", encoding="utf-8") as out_file:
        out_file.write(code)
    
    # return the code and the success status
    return (code, "File converted successfully.")
    
file_path = "./src/Quant4D.mlapp"
code, status = convert_mlapp_to_m(file_path)