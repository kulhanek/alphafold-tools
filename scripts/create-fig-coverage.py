import os
import glob
import pickle
import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================

def generate_output_images(feature_dict,args):
    msa = feature_dict['msa']
    seqid = (np.array(msa[0] == msa).mean(-1))
    seqid_sort = seqid.argsort()
    non_gaps = (msa != 21).astype(float)
    non_gaps[non_gaps == 0] = np.nan
    final = non_gaps[seqid_sort] * seqid[seqid_sort, None]

    plt.figure(figsize=(args.width, args.height), dpi=args.dpi, constrained_layout=True)
    plt.title(args.title)
    plt.imshow(final,
               interpolation='nearest', aspect='auto',
               cmap="rainbow_r", vmin=0, vmax=1, origin='lower')
    plt.plot((msa != 21).sum(0), color='black')
    plt.xlim(-0.5, msa.shape[1] - 0.5)
    plt.ylim(-0.5, msa.shape[0] - 0.5)
    plt.colorbar(label="Sequence identity to query", )
    plt.xlabel("Residue")
    plt.ylabel("Sequences")
    plt.savefig(args.output) 

# ==============================================================================

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input",
    type=Path,
    required=True,
    help="path to input features.pkl file",    
)
parser.add_argument(
    "-o",
    "--output",
    type=Path,
    default="coverage.png",
    help="path to output figure with MSA coverage",    
)
parser.add_argument(
    "--width",
    type=float,
    default=4.0,
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
    default="Sequence coverage",
    help="figure title",
)
args = parser.parse_args()

if not args.input.exists():
    raise FileNotFoundError(args.input)

# ==============================================================================

print("\nInput features: {0}".format(args.input))
feature_dict = pickle.load(open(args.input,'rb'))
print("Features keys:")
for key in feature_dict.keys():
    print("  * %s" % key)

print("\nCreating output file: {0}".format(args.output))
generate_output_images(feature_dict,args)
print("Done\n");

