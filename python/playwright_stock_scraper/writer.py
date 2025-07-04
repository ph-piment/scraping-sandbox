import csv
import json


def save_csv(data, output_file, fieldnames=None):
    if not fieldnames:
        fieldnames = list(data[0].keys())
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        print(f"✅ Saved to {output_file}")


def save_json(data, output_file, indent=2):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        print(f"✅ Saved to {output_file}")
