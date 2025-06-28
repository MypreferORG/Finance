from datasets import load_dataset

# Indicate the dataset id from the Hub
dataset_id = "sentence-transformers/natural-questions"
dataset = load_dataset(dataset_id, split="train")