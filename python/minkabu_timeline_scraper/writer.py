import csv


def save_csv(data, output_file, fieldnames=None):
    if not fieldnames:
        fieldnames = list(data[0].keys())
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
