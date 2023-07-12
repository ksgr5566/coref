from datasets import load_dataset
from argparse import ArgumentParser
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


parser = ArgumentParser()
parser.add_argument("--model", type=str, default="")
parser.add_argument("--epochs", type=float, default=1)
parser.add_argument("--batch_size", type=int, default=2)
parser.add_argument("--checkpoint", type=str, default="")
                    

args = parser.parse_args()

try:
    model_name = args.model # "facebook/bart-large" # 't5-base' #
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
except:
    raise ValueError("Model not found")

def process_data_to_model_inputs(batch):
  inputs = tokenizer(batch['Input'], padding='max_length', truncation=True, max_length=512)
  outputs = tokenizer(batch['Output'], padding='max_length', truncation=True, max_length=512)

  inputs['labels'] = outputs['input_ids']
  return inputs

train_data = load_dataset('json', data_files='./train.json', field='data')
test_data = load_dataset('json', data_files='./test.json', field='data')
dev_data = load_dataset('json', data_files='./dev.json', field='data')

tokenized_train_dataset = train_data.map(process_data_to_model_inputs, batched=True)
tokenized_test_dataset = test_data.map(process_data_to_model_inputs, batched=True)
tokenized_dev_dataset = dev_data.map(process_data_to_model_inputs, batched=True)

train_dataset = tokenized_train_dataset['train']
test_dataset = tokenized_test_dataset['train']
dev_dataset = tokenized_dev_dataset['train']

training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    num_train_epochs=args.epochs,
    per_device_train_batch_size=args.batch_size,
    per_device_eval_batch_size=args.batch_size,
    warmup_steps=500,  # for lr scheduler
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    do_train=True,
    do_eval=True,
    evaluation_strategy="epoch",
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=dev_dataset,
)

if not args.checkpoint == "":
    trainer.train(resume_from_checkpoint=f"./results/{args.checkpoint}")
else:
    trainer.train()
