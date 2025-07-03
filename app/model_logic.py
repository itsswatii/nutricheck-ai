# app/model_logic.py

import pandas as pd

INGREDIENT_RULES = {
    "citric acid": {"category": "Good", "reason": "Generally safe, but can be irritating in large amounts."},
    "sodium benzoate": {"category": "Bad", "reason": "Preservative with potential long-term effects."},
    "xanthan gum": {"category": "Good", "reason": "Safe for most, but may cause bloating."},
    "artificial flavor": {"category": "Bad", "reason": "Contains unknown chemicals."},
    "high fructose corn syrup": {"category": "Bad", "reason": "Linked to obesity and diabetes."},
    "salt": {"category": "Good", "reason": "Safe in moderation."},
    "sea salt": {"category": "Good", "reason": "Natural source of sodium, moderate use recommended."},
    "natural flavor": {"category": "Good", "reason": "Common and usually plant-derived, vague labeling."},
    "caramel color": {"category": "Bad", "reason": "Some types may contain carcinogens."},
    "sugar": {"category": "Good", "reason": "Moderation is key."}
}

def flag_ingredients(input_csv="../data/ingredient_sample.csv", output_csv="../data/flagged_ingredients.csv"):
    df = pd.read_csv(input_csv)

    df["category"] = df["ingredient"].map(lambda x: INGREDIENT_RULES.get(x, {}).get("category", "Unknown"))
    df["reason"] = df["ingredient"].map(lambda x: INGREDIENT_RULES.get(x, {}).get("reason", "Not found in rulebook"))

    df.to_csv(output_csv, index=False)
    print(f"✅ Flagged ingredients saved to {output_csv}")
    print(df.head())

if __name__ == "__main__":
    flag_ingredients()

