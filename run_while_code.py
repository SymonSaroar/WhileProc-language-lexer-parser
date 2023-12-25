#!/usr/bin/env python3
import argparse

from parse import *

parser = argparse.ArgumentParser("Interpret a WhileProc source code")
parser.add_argument("filename", metavar='f', help="Source File name of the WhileProc code (*.while)")

args = parser.parse_args()
with open(args.filename, "r") as source_file:
    source_code = "".join(source_file.readlines())
    tokens = lex(source_code)
    print(parse(tokens).run())
