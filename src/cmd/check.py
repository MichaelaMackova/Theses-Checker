#----------------------------------------------------------------------------
# File          : check.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 31.1.2023
# Last Updated  : 21.11.2024
# ---------------------------------------------------------------------------


import sys
import os
from theses_checker_package.theses_checker import Checker
import argparse


COLOR_RESET = "\u001b[0m"
COLOR_OK = "\u001b[32;1m"
COLOR_WARNING = "\u001b[33;1m"

NO_MISTAKES = " -> " + COLOR_OK + "no mistakes found" + COLOR_RESET
MISTAKES_FOUND = " -> " + COLOR_WARNING + "mistakes were found" + COLOR_RESET

# ---------------------------------------------- MAIN --------------------------------------------------------

parser = argparse.ArgumentParser(description="Makes a new pdf file called '*_annotated.pdf' in the folder, where this program is saved. If no check flag is given, everything will be checked.") # TODO:
parser.add_argument('in_files', nargs='+', help="path to files to be checked; only '*.pdf' are supported")
parser.add_argument('--embedded_PDF', action='store_false', help="if used, embedded PDF files will be treated as part of the PDF; otherwise, they will be considered as images")
parser.add_argument('-o', '--overflow', action='store_true', help="overflow check")
parser.add_argument('-i', '--image_width', action='store_true', help="image width check")
parser.add_argument('-H', '--Hyphen', action='store_true', help="hyphen check")
parser.add_argument('-t', '--TOC', action='store_true', help="table of content section check")
parser.add_argument('-s', '--space_bracket', action='store_true', help="space before left bracket check")
parser.add_argument('-e', '--empty_chapter', action='store_true', help="text between titles check")
parser.add_argument('-b', '--bad_reference', action='store_true', help=" '??' -> bad reference check")
#parser.add_argument('--out_file', default="annotated.pdf", help="name of created annotated file, default name is 'annotated.pdf'; usable with only one IN_FILES otherwise ignored")
args = parser.parse_args(sys.argv[1:])



if(not (args.overflow or args.image_width or args.Hyphen or args.TOC or args.space_bracket or args.empty_chapter or args.bad_reference)):
    args.overflow = True
    args.image_width = True
    args.Hyphen = True
    args.TOC = True
    args.space_bracket = True
    args.empty_chapter = True
    args.bad_reference = True

for file in args.in_files:
    if(not os.path.exists(file)):
        print("File '" + file + "' does not exist.")
        continue
    if(file[-4:] != ".pdf"):
        print("File '" + file + "' is not supported.")
        continue
    checker = Checker(file)
    # if(len(args.in_files) > 1):
    #     args.out_file = os.path.basename(file)[:-4] + "_annotated.pdf"
    out_file = os.path.basename(file)[:-4] + "_annotated.pdf"
    checker.annotate(out_file, args.embedded_PDF, args.overflow, args.Hyphen, args.image_width, args.TOC, args.space_bracket, args.empty_chapter, args.bad_reference)
    mistake_state = MISTAKES_FOUND if checker.mistakes_found else NO_MISTAKES 
    print("New file '" + out_file + "' was created." + mistake_state)