#----------------------------------------------------------------------------
# File          : check.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 31.1.2023
# ---------------------------------------------------------------------------


import sys
import os
from theses_checker import Checker
import argparse


COLOR_RESET = "\u001b[0m"
COLOR_OK = "\u001b[32;1m"
COLOR_WARNING = "\u001b[33;1m"

NO_MISTAKES = " -> " + COLOR_OK + "no mistakes found" + COLOR_RESET
MISTAKES_FOUND = " -> " + COLOR_WARNING + "mistakes were found" + COLOR_RESET

# ---------------------------------------------- MAIN --------------------------------------------------------

parser = argparse.ArgumentParser(description="Makes a new pdf file called '*_annotated.pdf' in the folder, where this program is saved. If no check flag is given, everything will be checked.") # TODO:
parser.add_argument('in_files', nargs='+', help="path to files to be checked; only '*.pdf' are supported")
parser.add_argument('-o', '--overflow', action='store_true', help="overflow check")
parser.add_argument('-i', '--image_width', action='store_true', help="image width check")
parser.add_argument('-H', '--Hyphen', action='store_true', help="hyphen check")
parser.add_argument('-t', '--TOC', action='store_true', help="table of content section check")
#parser.add_argument('--out_file', default="annotated.pdf", help="name of created annotated file, default name is 'annotated.pdf'; usable with only one IN_FILES otherwise ignored")
args = parser.parse_args(sys.argv[1:])



if(not (args.overflow or args.image_width or args.Hyphen or args.TOC)):
    args.overflow = True
    args.image_width = True
    args.Hyphen = True
    args.TOC = True

for file in args.in_files:
    if(file[-4:] != ".pdf"):
        print("File '" + file + "' is not supported.")
        continue
    checker = Checker(file)
    # if(len(args.in_files) > 1):
    #     args.out_file = os.path.basename(file)[:-4] + "_annotated.pdf"
    out_file = os.path.basename(file)[:-4] + "_annotated.pdf"
    checker.annotate(out_file,args.overflow,args.Hyphen,args.image_width, args.TOC)
    mistake_state = MISTAKES_FOUND if checker.mistakes_found else NO_MISTAKES 
    print("New file '" + out_file + "' was created." + mistake_state)
