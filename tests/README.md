# Baseline Accuracy

For the current **60** test cases present in "tests.json", the <em>spacy</em> model gives **27.12%** acc while the <em>fcoref</em> model gives **33.89%** with **0.9** as threshold on cosine similarity. The results are reported in the respective csv files. **76.28%** with "ksgr5566/bartlg-e4.71" hf model.

To report accuracy on the available tests:
```
cd to parent directory of the project
python -m coref.tests.eval --spacy 
python -m coref.tests.eval --fcoref
python -m coref.tests.eval --hf --model "{model_name}"
python -m coref.tests.eval --all --model "{model_name}"
```