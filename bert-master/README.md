# BERT QA



### SQuAD 1.1

I have trained the model with squad data set but for training purpose i have used partial data for training and saved the model for prediction.

The Stanford Question Answering Dataset (SQuAD) is a popular question answering
benchmark dataset. BERT (at the time of the release) obtains state-of-the-art
results on SQuAD with almost no task-specific network architecture modifications
or data augmentation. However, it does require semi-complex data pre-processing
and post-processing to deal with (a) the variable-length nature of SQuAD context
paragraphs, and (b) the character-level answer annotations which are used for
SQuAD training. This processing is implemented and documented in `run_squad.py`.

To run on SQuAD, you will first need to download the dataset. The
[SQuAD website](https://rajpurkar.github.io/SQuAD-explorer/) does not seem to
link to the v1.1 datasets any longer, but the necessary files can be found here:

*   [train-v1.1.json](https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json)


Download these to some directory `$SQUAD_DIR`.

In run_squad folder we have to mention the following hyperparameter for training.We have to download the Bert BASE model and give the path for vocab file,config file,check point.
python run_squad.py \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --do_train=True \
  --train_file=$SQUAD_DIR/train-v1.1.json \
  --do_predict=True \
  --predict_file=NONE
  --train_batch_size=12 \
  --learning_rate=3e-5 \
  --num_train_epochs=2.0 \
  --max_seq_length=384 \
  --doc_stride=128 \
  --output_dir=/tmp/squad_base/
  
  We have to run the check_modified.py file for prediction.It will take input as  paragraph text and question in json format . It will predict the Bert score and answer in json format.I have implemented the code in Tensorflow and used Flask service for rest api and use postman for giving the post request to the method.(get_pred is the starting point of the flask service)
  
  In future i will trained the model with the total squad data and it will predict more accurately.Bert score can give you the confidence score and it will help you to also predict the answer from the text.
```

