# test_hf.py
from datasets import load_dataset

dataset = load_dataset("ag_news", split="train[:10]")
print(dataset[0])
