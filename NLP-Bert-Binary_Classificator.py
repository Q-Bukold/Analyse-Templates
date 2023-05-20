import pandas as pd
#pip install simpletransformers
from simpletransformers.classification import ClassificationModel, ClassificationArgs
from sys import argv
from sys import stderr
import logging
import torch
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# -> prevented error
#Log:
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

def pre_process_traindata(filename):
    df = pd.read_excel(filename)
    df = df[["text", "task1"]]
    df.loc[df['task1'] == "NOT", 'task1'] = 0
    df.loc[df["task1"] == "HOF", "task1"] = 1
    df.columns = ["text", "labels"]
    return df
  

print("Preprocessing Data")
annotations = pre_process_traindata("DATA.xlsx")

#shuffle data and drop old index
annotations = annotations.sample(frac=1, random_state=1).reset_index(drop=True)

# create training-data <-- df
train_df = annotations.head(int(len(annotations)*0.8))
selected_columns = ["text", "labels"]
train_df = train_df[selected_columns]

# create eval-data <-- df
eval_df = annotations.tail(int(len(annotations)*0.2))
selected_columns = ["text", "labels"]
eval_df = eval_df[selected_columns]

print(len(train_df))
print(len(eval_df))

print ("TRAINIEREN")
model_args = {
  'use_multiprocessing' : False,
  'use_multiprocessing_for_evaluation' : False,
  'multiprocessing_chunksize' : 1,
  'dataloader_num_workers' : 1,
  'num_train_epochs': 1,
  'overwrite_output_dir': True}
  
model = ClassificationModel('distilbert', 'distilbert-base-german-cased',
use_cuda=False, 
args= model_args)

#save model
model.train_model(train_df)
model.model.save_pretrained('model1405')
model.tokenizer.save_pretrained('model1405')
model.config.save_pretrained('model1405/')

# EVALUATE 
print("Starting Evaluation:")
result, model_outputs, wrong_predictions = model.eval_model(eval_df)
print("Results:")
for i in result:
    print(i, result[i])
    
#tp = true positives
#tn = true negatives
#fp = false positives
#fn = false negaives
#auroc = precision
#auprc = average precison

#insight into predictions:
#for n, dic in enumerate(wrong_predictions):
#    print("Annotation Label:", dic.label)
#    print(dic.text_a)
#    print(10*'+')
