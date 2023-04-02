
import os
import glob
import pickle
import json
import argparse
from pathlib import Path
import numpy as np
    
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
    default="plddt.dat",
    help="path to text file pLDDT (predicted Local Distance Difference Test) values",    
)
args = parser.parse_args()

if not args.input.exists():
    raise FileNotFoundError(args.input)

# ==============================================================================

print("\nInput model: {0}".format(args.input))
model_dict = pickle.load(open(args.input,'rb'))
print("Model keys:")
for key in model_dict.keys():
    print("  * %s" % key)

if not ('plddt' in model_dict):
    print('\nNo plddt present in data!\n')
    quit()

print("\nCreating output file: {0}".format(args.output))
f = open(args.output,"wt")
for r, plddt in enumerate(model_dict['plddt']):
    f.write("%10d %10.6f\n" % (r+1,plddt)) 
f.close()
print("Done\n")

