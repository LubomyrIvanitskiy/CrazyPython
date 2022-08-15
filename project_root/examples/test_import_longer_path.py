import os
import sys
import pathlib

sys.path.append(str(pathlib.Path(os.path.realpath(__file__)).parent) + os.sep + "nested")
import greetings
