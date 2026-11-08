"""Importer for verified Indian Food Composition Tables (IFCT 2017) CSV data.
Run with: python -m app.seed.import_ifct path/to/ifct_data.csv
"""
import sys
import csv
import os
from datetime import date
from sqlalchemy import select
from app.db.session import SyncSessionLocal
import app.db.models as models


def import_ifct_csv(csv_path: str):
    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' does not exist.")
        return

    print(f"Importing verified IFCT data from: {csv_path}")
    db = SyncSessionLocal()
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            imported_count = 0
            for row in reader:
                name = row.get("name")
                if not name:
                    continue

                existing = db.execute(select(models.Ingredient).where(models.Ingredient.name == name)).scalar_one_or_none()
                if not existing:
                    existing = models.Ingredient(
                        name=name,
                        local_names={
                            "hi": row.get("local_name_hi", ""),
                            "ta": row.get("local_name_ta", ""),
                        },
                        category=row.get("category", "cereal_millet"),
                        diet_class=row.get("diet_class", "vegan"),
                        cost_per_kg_inr=100.0,
                        cost_as_of=date.today(),
                        availability="high",
                        data_status="verified",
                        version=1,
                    )
                    db.add(existing)
                    db.flush()

                # Add nutrients
                nutrients_map = {
                    "energy": ("energy_kcal", "kcal"),
                    "protein": ("protein_g", "g"),
                    "iron": ("iron_mg", "mg"),
                    "folate": ("folate_ug", "ug"),
                    "b12": ("b12_ug", "ug"),
                    "vit_c": ("vit_c_mg", "mg"),
                    "calcium": ("calcium_mg", "mg"),
                    "fat": ("fat_g", "g"),
                    "added_sugar": ("added_sugar_g", "g"),
                    "sodium": ("sodium_mg", "mg"),
                    "fibre": ("fibre_g", "g"),
                }

                for nut_code, (col_name, unit) in nutrients_map.items():
                    raw_val = row.get(col_name)
                    if raw_val is not None and raw_val.strip() != "":
                        try:
                            val = float(raw_val)
                            # Update or insert
                            nut_obj = db.execute(
                                select(models.IngredientNutrient).where(
                                    models.IngredientNutrient.ingredient_id == existing.id,
                                    models.IngredientNutrient.nutrient_code == nut_code,
                                    models.IngredientNutrient.source == "IFCT_2017",
                                )
                            ).scalar_one_or_none()

                            if nut_obj:
                                nut_obj.amount_per_100g = val
                            else:
                                nut_obj = models.IngredientNutrient(
                                    ingredient_id=existing.id,
                                    nutrient_code=nut_code,
                                    amount_per_100g=val,
                                    unit=unit,
                                    source="IFCT_2017",
                                    source_ref=row.get("source_ref", "IFCT 2017 NIN Table 1"),
                                )
                                db.add(nut_obj)
                        except ValueError:
                            pass

                imported_count += 1

            db.commit()
            print(f"Successfully processed {imported_count} ingredients from IFCT dataset.")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        import_ifct_csv(sys.argv[1])
    else:
        print("Usage: python -m app.seed.import_ifct data/ifct_2017.csv")

