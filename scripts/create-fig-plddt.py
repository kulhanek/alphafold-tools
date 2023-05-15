
import os
import glob
import pickle
import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ==============================================================================
def generate_output_images(model_dict,args):
    plt.figure(figsize=(args.width, args.height), dpi=args.dpi, constrained_layout=True)
    plt.title(args.title)
    plt.plot(model_dict["plddt"],label=None)
    plt.xlabel("Residue")    
    plt.ylabel("pLDDT")
    plt.ylim(0, 100)    
    plt.savefig(args.output) 
    
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
    default="plddt.png",
    help="path to output figure with pLDDT (predicted Local Distance Difference Test)",    
)
parser.add_argument(
    "--width",
    type=float,
    default=5.0,
    help="figure width in inches",
)
parser.add_argument(
    "--height",
    type=float,
    default=4.0,
    help="figure height in inches",
)
parser.add_argument(
    "--dpi",
    type=int,
    default=600,
    help="figure resolution",
)
parser.add_argument(
    "--title",
    type=str,
    default="Predicted LDDT",
    help="figure title",
)
args = parser.parse_args()

if not args.input.exists():
    raise FileNotFoundError(args.input)

# ==============================================================================

print("BLA\n")

print("\nInput model: {0}".format(args.input))
model_dict = pickle.load(open(args.input,'rb'))
print("Model keys:")
for key in model_dict.keys():
    print("  * %s" % key)

if not ('plddt' in model_dict):
    print('\nNo plddt present in data!\n')
    quit()

print("\nCreating output file: {0}".format(args.output))
generate_output_images(model_dict,args)
print("Done\n")

