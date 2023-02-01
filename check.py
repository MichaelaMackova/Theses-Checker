import sys
import os
from theses_checker import Checker
import argparse

# ---------------------------------------------- MAIN --------------------------------------------------------

parser = argparse.ArgumentParser(description="Makes a new pdf file called '*_annotated.pdf' in the folder, where this program is saved. If no check flag is given, everything will be checked.") # TODO:
parser.add_argument('in_files', nargs='+', help="path to files to be checked; only '*.pdf' are supported")
parser.add_argument('-o', '--overflow', action='store_true', help="overflow check")
parser.add_argument('-i', '--image_width', action='store_true', help="image width check")
parser.add_argument('-H', '--Hyphen', action='store_true', help="hyphen check")
#parser.add_argument('--out_file', default="annotated.pdf", help="name of created annotated file, default name is 'annotated.pdf'; usable with only one IN_FILES otherwise ignored")
args = parser.parse_args(sys.argv[1:])



if(not (args.overflow or args.image_width or args.Hyphen)):
    args.overflow = True
    args.image_width = True
    args.Hyphen = True

for file in args.in_files:
    if(file[-4:] != ".pdf"):
        print("File '" + file + "' is not supported.")
        continue
    checker = Checker(file)
    # if(len(args.in_files) > 1):
    #     args.out_file = os.path.basename(file)[:-4] + "_annotated.pdf"
    out_file = os.path.basename(file)[:-4] + "_annotated.pdf"
    checker.annotate(out_file,args.overflow,args.Hyphen,args.image_width)

print("--DONE--")
