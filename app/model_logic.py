import pandas as pd
import os

def clean_ingredient(name):
    """
    Normalize ingredient names by:
    - Converting to lowercase
    - Stripping whitespace
    - Removing 4-digit numeric suffixes like '_9943'
    """
    name = str(name).lower().strip()
    if "_" in name and name.split("_")[-1].isdigit() and len(name.split("_")[-1]) == 4:
        name = "_".join(name.split("_")[:-1])
    return name

def flag_ingredients(input_csv="../data/ingredient_sample.csv", 
                     rules_csv="../data/ingredient_rules_large.csv", 
                     output_csv="../data/flagged_ingredients.csv"):
    if not os.path.exists(input_csv):
        print(f"❌ Input file not found: {input_csv}")
        return

    print("🔍 Loading input ingredients...")
    df = pd.read_csv(input_csv)
    df["cleaned_ingredient"] = df["ingredient"].apply(clean_ingredient)

    print("📘 Loading rules from:", rules_csv)
    rules_df = pd.read_csv(rules_csv)
    rules_df["ingredient"] = rules_df["ingredient"].apply(clean_ingredient)

    #rules_map = rules_df.set_index("ingredient").to_dict("index")
    rules_map = rules_df.drop_duplicates(subset="ingredient").set_index("ingredient").to_dict("index")


    print("🚩 Flagging ingredients...")
    flagged_data = []
    for original, cleaned in zip(df["ingredient"], df["cleaned_ingredient"]):
        if cleaned in rules_map:
            category = rules_map[cleaned]["category"]
            reason = rules_map[cleaned]["reason"]
        else:
            category = "Unknown"
            reason = "Not found in rulebook"
        flagged_data.append({
            "ingredient": original,
            "category": category,
            "reason": reason
        })

    flagged_df = pd.DataFrame(flagged_data)
    flagged_df.to_csv(output_csv, index=False)
    print(f"✅ Flagged ingredients saved to {output_csv}")
    print(flagged_df.head())

if __name__ == "__main__":
    flag_ingredients()

