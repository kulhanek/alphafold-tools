import os
import glob
import pickle
import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.colors import LinearSegmentedColormap

# ==============================================================================
def generate_output_images(model_dicts, args):
    
    nrows = int(len(model_dicts)/5)
    ncols = 5
    
    fig, axes = plt.subplots(nrows, ncols, sharex=True, sharey=True, constrained_layout=True)
    fig.set_figwidth(args.width)
    fig.set_figheight(args.height)
    fig.set_dpi(args.dpi)
    
    fig.suptitle(args.title)
    fig.supxlabel("Scored residue")
    fig.supylabel("Aligned residue")
    
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
    
    for n, item in enumerate(model_dicts):
        if args.mlegend:
            title = "%s (%s: %5.3f)" % (item['label'], item['rtype'], item['ranking'])
            axes.flat[n].set_title(title,fontsize='x-small')
        im = axes.flat[n].imshow(pickle.load(open(item['path'],'rb'))["predicted_aligned_error"], cmap=my_cmap, vmin=0, vmax=30)
        
    fig.colorbar(im, ax=axes, label="Expected position error [Å]", shrink=0.6)

    plt.savefig(args.output, bbox_inches="tight") 

# ==============================================================================
parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input",
    type=Path,
    required=True,
    help="path to directory with models (wildcars are permitted)",    
)
parser.add_argument(
    "-p",
    "--pattern",
    type=str,
    default="*model*.pkl",
    help="search pattern",    
)
parser.add_argument(
    "-o",
    "--output",
    type=Path,
    default="paes.png",
    help="path to output figure with PAEs (predicted aligned errors)",    
)
parser.add_argument(
    "-r",
    "--ranking",
    type=Path,
    default="ranking_paes.log",
    help="path to text file with model rankings",    
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
    default="Predicted PAEs",
    help="figure title",
)
parser.add_argument(
    "--sort",
    type=str,
    default="ranking",
    help="sort model by 'ranking' or 'name'",
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
parser.add_argument(
    "--no-legend",  
    help="do not show model legend",
    dest='mlegend',
    action='store_false'
)
parser.set_defaults(mlegend=True)
args = parser.parse_args()

# ==============================================================================

def key_by_name(item):
    return item['path']

def key_by_ranking(item):
    return item['ranking']

# ==============================================================================

print("\nInput path:         {0}".format(args.input))
print("Model name pattern: {0}".format(args.pattern))

pattern = os.path.join(args.input,args.pattern)

print("")
print("> Loading models ...")
# list models
model_paths = list(glob(pattern))

# load pkl files
model_dicts = []
for path in model_paths:
    print(path)
    basedir = os.path.dirname(path)
    modelname = Path(path).stem.replace("result_","")
    rankfile = os.path.join(basedir,"ranking_debug.json")
    ranking = 0.0
    rtype = "none"
    if os.path.isfile(rankfile):
        with open(rankfile, 'r') as f:
            ranking_dict = json.load(f)
            if 'iptm+ptm' in ranking_dict:
                ranking = ranking_dict["iptm+ptm"][modelname]
                rtype = "iptm+ptm"
            if 'plddts' in ranking_dict:
                ranking = ranking_dict["plddts"][modelname]
                rtype = "plddt"
                
    model_dicts.append({'label': '',
                        'path': path,
                        'ranking': ranking,
                        'rtype': rtype,})
#                        'model': pickle.load(open(path,'rb'))})

print("> Number of models: {0}".format(len(model_dicts)))

if len(model_dicts) == 0:
    print('')
    quit()
    
if not ('predicted_aligned_error' in pickle.load(open(model_dicts[0]['path'],'rb'))):
    print('')
    print("Available model keys:")
    for key in pickle.load(open(model_dicts[0]['path'],'rb')).keys():
        print("  * %s" % key)
    print('\nNo predicted_aligned_error present in data!\n')
    quit()    

# sort models
print("")
msort = False
if args.sort == 'name':
    print("> Sorted models by names ...")    
    model_dicts.sort(key=key_by_name)
    msort = True
    
if args.sort == 'ranking':
    print("> Sorted models by ranking ...")       
    model_dicts.sort(key=key_by_ranking,reverse=True)   
    msort = True
    
if msort == False:
    print("> Unsorted models ...") 

f = open(args.ranking,"wt")
for n, model in enumerate(model_dicts):
    model['label'] = "M%03d" % (n+1)
    print("%s %-50s %-10s %5.3f" % (model['label'], model['path'], model['rtype'], model['ranking']))
    f.write("%s %-50s %-10s %5.3f\n" % (model['label'], model['path'], model['rtype'], model['ranking']))
f.close()

# generate figure
print("\nCreating output file: {0}".format(args.output))
generate_output_images(model_dicts,args)
print("Done\n")


