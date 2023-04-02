
import os
import glob
import pickle
import json
import argparse
from pathlib import Path

# ==============================================================================
parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input",
    type=Path,
    required=True,
    help="path to input model.pkl file",    
)
parser.add_argument(
    "-o",
    "--output",
    type=Path,
    default="pae.dat",
    help="path to text file with PAE (predicted aligned error) values",    
)
parser.add_argument(
    "--gnuplot",  
    help="add new lines after rows",
    dest='gnuplot',
    action='store_true'
)
parser.set_defaults(gnuplot=False)
args = parser.parse_args()

if not args.input.exists():
    raise FileNotFoundError(args.input)

# ==============================================================================

print("\nInput model: {0}".format(args.input))
model_dict = pickle.load(open(args.input,'rb'))
print("Model keys:")
for key in model_dict.keys():
    print("  * %s" % key)

if not ('predicted_aligned_error' in model_dict):
    print('\nNo predicted_aligned_error present in data!\n')
    quit()

print("\nCreating output file: {0}".format(args.output))
f = open(args.output,"wt")
for y, row in enumerate(model_dict['predicted_aligned_error']):
    for x, pae in enumerate(row):
        f.write("%10d %10d %10.6f\n" % (x+1,y+1,pae))
    if args.gnuplot == True:
        f.write("\n")
f.close()
print("Done\n");

