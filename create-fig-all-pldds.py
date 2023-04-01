import os
import glob
import pickle
import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

# ==============================================================================
def generate_output_images(model_dicts, args):
    plt.figure(figsize=(args.width, args.height), dpi=args.dpi, constrained_layout=True)
    plt.title(args.title)
    
    for value in model_dicts:
        title = ''
        if args.mlegend:
            title = "%s (%s: %5.3f)" % (value['label'], value['rtype'], value['ranking'])      
        plt.plot(value['model']["plddt"],label=title)
        
    plt.xlabel("Residue")    
    plt.ylabel("pLDDT")
    plt.ylim(0, 100)
    
    if args.mlegend:
        if len(model_dicts) > 5:
            plt.legend(loc='lower left', bbox_to_anchor=(1, 0.5), fontsize='x-small')
        else:
            plt.legend(loc='lower right')
            
    plt.savefig(args.output) 

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
    help="path to directory with models",    
)
parser.add_argument(
    "-o",
    "--output",
    type=Path,
    default="plddts.png",
    help="path to output figure with pLDDTs (predicted Local Distance Difference Tests)",    
)
parser.add_argument(
    "-r",
    "--ranking",
    type=Path,
    default="ranking_plddts.log",
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
    default="Predicted LDDTs",
    help="figure title",
)
parser.add_argument(
    "--sort",
    type=str,
    default="ranking",
    help="sort model by 'ranking' or 'name'",
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

print("\n> Loading models ...")
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
                        'rtype': rtype,
                        'model': pickle.load(open(path,'rb'))})

print("> Number of models: {0}".format(len(model_dicts)))

if len(model_dicts) == 0:
    print('')
    quit()
    
if not ('plddt' in model_dicts[0]['model']):
    print('')
    print(model_dicts[0]['model'].keys())
    print('\nNo plddt present in data!\n')
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


