import time
import spacy
import torch
from typing import Union, List
from fastcoref import spacy_component
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class SpacyModel:
    def __init__(self):
        self.model = spacy.load("en_coreference_web_trf")

    def predict(self, text: str):
        doc = self.model(text)

        offset = 0
        reindex = []
        for chain in doc.spans:
            for idx, span in enumerate(doc.spans[chain]):
                if idx > 0:
                    reindex.append([span.start_char, span.end_char, doc.spans[chain][0].text])

        for span in sorted(reindex, key=lambda x:x[0]):
            text = text[0:span[0] + offset] + span[2] + text[span[1] + offset:]
            offset += len(span[2]) - (span[1] - span[0])
        
        return text

    def __call__(self, text: str):
        return self.predict(text)
    
class FastCoref:
    def __init__(self):
        self.model = spacy.load("en_core_web_sm", exclude=["parser", "lemmatizer", "ner", "textcat"])
        self.model.add_pipe("fastcoref")

    def predict(self, text: str):
        doc = self.model(text, component_cfg={"fastcoref": {'resolve_text': True}})
        return doc._.resolved_text

    def __call__(self, text: str):
        return self.predict(text)
    
class HFModel:
    def __init__(self, model_name: str):
        try:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        except:
            raise ValueError("Provide a valid public Seq2SeqLM model name from HuggingFace")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

    def __validate_prompt(self, prompts: List[str]):
        for prompt in prompts:
            try:
                prompt.split('User: ')[1].split('AI: ')[0]
                prompt.split('AI: ')[1].split('User: ')[0]
                prompt.split('User: ')[2]
            except:
                print(prompt)
                raise ValueError("Prompt must be of the form 'User: <user ques> AI: <AI response> User: <user ques>'")
    
    def predict(self, prompts: Union[str, List[str]], temperature: float = 0.7, max_length: int = 512, num_beams: int = 5) -> List[str]:
        if type(prompts) == str: prompts = [prompts]
        self.__validate_prompt(prompts)
        start = time.time()
        encoded_prompt = self.tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            output = self.model.generate(
                **encoded_prompt, 
                max_length=max_length, 
                num_beams=num_beams,
                temperature=temperature
            )
        decode = self.tokenizer.batch_decode(output, skip_special_tokens=True)
        end = time.time()
        print(f"Time taken: {end - start} for {len(prompts)} prompts")
        return decode
    
    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)