import os
import sys
import json
import subprocess
import pandas as pd
from tqdm import tqdm
from argparse import ArgumentParser
from sentence_transformers import SentenceTransformer, util


THRESHOLD = 0.9

parser = ArgumentParser()
parser.add_argument("--spacy", action="store_true")
parser.add_argument("--fcoref", action="store_true")
parser.add_argument("--hf", action="store_true")
parser.add_argument("--model", type=str, default="")
parser.add_argument("--all", action="store_true")

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

args = parser.parse_args()
if args.all:
    results = []
    if not os.path.exists(os.path.join(current_directory, 'spacy_results.csv')):
        subprocess.run([sys.executable, "-m", "coref.tests.eval", "--spacy"])
    if not os.path.exists(os.path.join(current_directory, 'fcoref_results.csv')):
        subprocess.run([sys.executable, "-m", "coref.tests.eval", "--fcoref"])
    if not os.path.exists(os.path.join(current_directory, 'hf_results.csv')):
        subprocess.run([sys.executable, "-m", "coref.tests.eval", "--hf", args.model])
    spacy_df = pd.read_csv(os.path.join(current_directory, 'spacy_results.csv'))
    fcoref_df = pd.read_csv(os.path.join(current_directory, 'fcoref_results.csv'))
    hf_df = pd.read_csv(os.path.join(current_directory, 'hf_results.csv'))
    df = pd.merge(spacy_df, fcoref_df, on=['Example Number', 'Output', 'Comment'], suffixes=('_spacy', '_fcoref'), how='outer')
    df = pd.merge(df, hf_df, on=['Example Number', 'Output', 'Comment'], suffixes=(None, '_hf'), how='outer')
    df.to_csv(os.path.join(current_directory, 'results.csv'), index=False)
    sys.exit()
elif args.spacy and not args.fcoref and not args.hf:
    from .. import SpacyModel as Model
    results_file = 'spacy_results.csv'
elif args.fcoref and not args.spacy and not args.hf:
    from .. import FastCoref as Model
    results_file = 'fcoref_results.csv'
elif args.hf and not args.spacy and not args.fcoref:
    from .. import HFModel as Model
    results_file = 'hf_results.csv'
else:
    raise ValueError("Please specify a single model or run all.")


test_file_path = os.path.join(current_directory, 'tests.json')
save_path = os.path.join(current_directory, results_file)

with open(test_file_path, 'r') as f:
    data = json.load(f)

tests = data["data"]

sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
df = pd.DataFrame(columns=['Example Number', 'Output', 'Prediction', 'Cosine Score', 'Comment'])
accuracy = 0

if args.spacy or args.fcoref:
    model = Model()
elif args.hf:
    model = Model(args.model)

for count, item in tqdm(enumerate(tests)):
    text = model(item["Input"])
    if args.hf:
        text = text[0]
    prediction = text.split("User:")[-1]
    output = item["Output"][6:]
    comment = "None"
    if "Comment" in item:
        comment = item["Comment"]

    prediction_embedding = sentence_model.encode(prediction, convert_to_tensor=True)
    output_embedding = sentence_model.encode(output, convert_to_tensor=True)
    
    cosine_score = util.pytorch_cos_sim(prediction_embedding, output_embedding).item()
    new_row = pd.Series({'Example Number': count + 1, 'Output': output, 'Prediction': prediction, 'Cosine Score': round(cosine_score, 2), 'Comment': comment})  
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    if cosine_score > THRESHOLD:
        accuracy += 1

print(f'Accuracy: {accuracy / len(tests)}')
df.to_csv(save_path, index=False)