
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
    
    my_cmap = "bwr"
    if args.palette == 'green1':
        cmap_colors = (
            (0.0                ,  0.26666666666666666,  0.10588235294117647),
            (0.0                ,  0.42745098039215684,  0.17254901960784313),
            (0.13725490196078433,  0.54509803921568623,  0.27058823529411763),
            (0.13725490196078433,  0.54509803921568623,  0.27058823529411763),
            (0.25490196078431371,  0.6705882352941176 ,  0.36470588235294116),
            (0.45490196078431372,  0.7686274509803922 ,  0.46274509803921571),
            (0.63137254901960782,  0.85098039215686272,  0.60784313725490191),
            (0.7803921568627451 ,  0.9137254901960784 ,  0.75294117647058822),
            (0.89803921568627454,  0.96078431372549022,  0.8784313725490196 ),
            (0.96862745098039216,  0.9882352941176471 ,  0.96078431372549022)
            )        
        my_cmap = LinearSegmentedColormap.from_list('my', cmap_colors, args.ncsegs)
    elif args.palette == 'green2':
        cmap_colors = [(0.000, 0.266,  0.105), (1.000, 1.000, 1.000)]
        my_cmap = LinearSegmentedColormap.from_list('my', cmap_colors, args.ncsegs)
    elif args.palette == 'bwr':
        my_cmap = "bwr"
    else:
        my_cmap = args.palette
        
    plt.imshow(model_dict["predicted_aligned_error"], cmap=my_cmap, vmin=0, vmax=30)
    plt.colorbar(label="Expected position error [Å]")
    plt.xlabel("Scored residue")
    plt.ylabel("Aligned residue")
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
    default="pae.png",
    help="path to output figure with PAE (predicted aligned error)",    
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
    default="Predicted aligned error (PAE)",
    help="figure title",
)
parser.add_argument(
    "--ncsegs",
    type=int,
    default=256,    
    help="number of color segments",
)
parser.add_argument(
    "--palette",
    type=str,
    default='green1',    
    help="color palette: green1 (AlphaFoldDB), green2 (AlphaFoldDB like), bwr (ColabFold), or others by matplotlib",
)
args = parser.parse_args()

if not args.input.exists():
    raise FileNotFoundError(args.input)

# ==============================================================================

print("\nInput model: {0}".format(args.input))
model_dict = pickle.load(open(args.input,'rb'))
print("Model keys:  " + str(model_dict.keys()))

if not ('predicted_aligned_error' in model_dict):
    print('\nNo predicted_aligned_error present in data!\n')
    quit()

print("\nCreating output file: {0}".format(args.output))
generate_output_images(model_dict,args)
print("Done\n");

