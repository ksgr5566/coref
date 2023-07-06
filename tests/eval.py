import os
import json
import pandas as pd
from argparse import ArgumentParser
from sentence_transformers import SentenceTransformer, util


THRESHOLD = 0.9

parser = ArgumentParser()
parser.add_argument("--spacy", action="store_true")
parser.add_argument("--fcoref", action="store_true")

args = parser.parse_args()
if args.spacy and not args.fcoref:
    from .. import SpacyModel as Model
    results_file = 'spacy_results.csv'
elif args.fcoref and not args.spacy:
    from .. import FastCoref as Model
    results_file = 'fcoref_results.csv'
else:
    raise ValueError("Please specify a single model to evaluate.")


current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
test_file_path = os.path.join(current_directory, 'tests.json')
save_path = os.path.join(current_directory, results_file)

with open(test_file_path, 'r') as f:
    data = json.load(f)

tests = data["data"]

model = Model()
sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

df = pd.DataFrame(columns=['Example Number', 'Output', 'Prediction', 'Cosine Score', 'Comment'])
accuracy = 0
for count, item in enumerate(tests):
    text = model(item["Input"])
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