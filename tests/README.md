# Baseline Accuracy

For the current 60 test cases present in "tests.txt", the <em>spacy</em> model gives **28.81%** acc while the <em>fcoref</em> model gives **37.28%**. The results are reported in the respective csv files.

To report accuracy on the available tests:
```
cd to parent directory of the project
python -m coref.tests.eval --spacy 
python -m coref.tests.eval --fcoref
```