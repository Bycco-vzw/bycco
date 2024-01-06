import csv
from pathlib import Path

rootdir = Path("..")

def process_i18n():
    with (rootdir / "share" / "data" / "i18n - all.csv").open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        allrows = []
        for r in reader:
            allrows.append(r)
    for l in ["en", "fr", "nl", "de"]:
        with (rootdir / "bycco_frontend" / "lang" / f"{l}.json").open(
            "w", encoding="utf8"
        ) as f:
            f.write("{\n")
            for r in allrows:
                if r["server"] != "1":  
                    f.write(f'"{r["key"]}": "{r[l]}",\n')
            f.write('"ZZZ": "ZZZ"\n')
            f.write("}\n")

if __name__ == "__main__":
    process_i18n()

