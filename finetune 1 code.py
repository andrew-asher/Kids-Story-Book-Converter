import pandas as pd
import tensorflow as tf
from transformers import T5Tokenizer, TFT5ForConditionalGeneration, get_linear_schedule_with_warmup

# Load the datasets
from datasets import load_dataset

dataset = load_dataset("allenai/multinews_dense_oracle")

# Select 90% of the dataset for training
n_samples = int(len(dataset['train']) * 0.9)
data = {'text': dataset['train']['document'][:n_samples], 'summary': dataset['train']['summary'][:n_samples]}

# Initialize the tokenizer
tokenizer = T5Tokenizer.from_pretrained('t5-base', use_fast=False)

# Tokenize and preprocess the dataset
tokenized_inputs = tokenizer(list(data['text']), max_length=512, truncation=True, padding='max_length', return_tensors='tf')
tokenized_outputs = tokenizer(list(data['summary']), max_length=512, truncation=True, padding='max_length', return_tensors='tf')

# Define the T5 model architecture
model = TFT5ForConditionalGeneration.from_pretrained('t5-base')

# Define optimizer with variable learning rate
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
warmup_steps = int(0.1 * n_samples / 16)  # 10% of train data for warm-up
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=n_samples)

# Loss function remains the same
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0))
    loss_ = loss_object(real, pred)
    mask = tf.cast(mask, dtype=loss_.dtype)
    loss_ *= mask
    return tf.reduce_sum(loss_)/tf.reduce_sum(mask)

# Accuracy function remains the same
def accuracy(y_true, y_pred):
    y_pred = tf.reshape(y_pred, (tf.shape(y_pred)[0], tf.shape(y_pred)[1], tf.shape(y_pred)[2]))
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.cast(y_true, tf.int32), tf.argmax(y_pred, axis=-1, output_type=tf.int32)), dtype=tf.float32))
    return accuracy

# Compile the model
model.compile(optimizer=optimizer, loss=loss_function, metrics=[accuracy])

# Prepare the inputs for training
inputs = {
    'input_ids': tokenized_inputs['input_ids'],
    'attention_mask': tokenized_inputs['attention_mask'],
    'labels': tokenized_outputs['input_ids'],
}

# Pad token is 0 for T5 models
pad_token_id = tokenizer.pad_token_id
inputs['decoder_input_ids'] = tf.pad(inputs['labels'][:, :-1], [[0, 0], [1, 0]], constant_values=pad_token_id)

# Fine-tune the model
model.fit(inputs, tokenized_outputs['input_ids'], batch_size=16, epochs=3, callbacks=[scheduler])

# Save the trained model
model.save_pretrained('/Users/andrewasher/Education/Research Project/Andrew/custom-t5-model/model')
