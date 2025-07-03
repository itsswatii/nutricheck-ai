# app/hf_loader.py

from datasets import load_dataset
import pandas as pd

def load_openfood_ingredients(top_n=1000, save_csv=True):
    print("🔄 Streaming OpenFoodFacts product-database (food split)...")

    # Use correct split: 'food' not 'train'
    ds = load_dataset("openfoodfacts/product-database", split="food", streaming=True)

    ingredients = set()
    for example in ds:
        tags = example.get("ingredients_tags")
        if tags:
            for tag in tags:
                tag = tag.replace("en:", "").replace("_", " ").strip()
                if tag:
                    ingredients.add(tag)
        if len(ingredients) >= top_n:
            break

    df = pd.DataFrame(list(ingredients), columns=["ingredient"])

    if save_csv:
        df.to_csv("../data/ingredient_sample.csv", index=False)
        print("✅ Saved to data/ingredient_sample.csv")

    return df

if __name__ == "__main__":
    df = load_openfood_ingredients()
    print(df.head())



