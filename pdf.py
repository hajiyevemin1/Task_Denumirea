import fitz
import re
import pandas as pd

pdf_file = "Denumirea.pdf"

columns = [
    "N/o",
    "Data anuntului",
    "IDNO",
    "Denumirea",
    "Adresa",
    "Din",
    "In",
]


x_bounds = [
    33.36,
    53.16,
    101.16,
    169.34,
    310.97,
    472.75,
    639.82,
    807.60,
]


def read_cell(page, x0, x1, y0, y1):
    r = fitz.Rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1)
    t = page.get_text("text", clip=r)
    lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
    return re.sub(r"\s+", " ", " ".join(lines))


def get_y_lines(page):
    ys = set()
    for d in page.get_drawings():
        for it in d["items"]:
            if it[0] == "re":
                r = it[1]
                if (r.y1 - r.y0) < 2 and (r.x1 - r.x0) > 200:
                    ys.add(round(r.y0, 2))
    return sorted(ys)


def parse_page(page, y_min, y_max):
    y_lines = [y for y in get_y_lines(page) if y_min <= y <= y_max]
    rows = []

    for y0, y1 in zip(y_lines[:-1], y_lines[1:]):
        row = [
            read_cell(page, x_bounds[i], x_bounds[i+1], y0, y1)
            for i in range(len(x_bounds) - 1)
        ]

        if not row[0].strip() or row[0] == "N/o":
            continue


        rows.append(row)

    return rows


doc = fitz.open(pdf_file)

rows = []

for page_index in range(len(doc)):
    page = doc.load_page(page_index)

    if page_index == 0:
        y_min = 120
    else:
        y_min = 20

    rows += parse_page(page, y_min, 560)

df = pd.DataFrame(rows, columns=columns)
df["Data anuntului"] = pd.to_datetime(
    df["Data anuntului"],
    format="%d.%m.%Y",
    errors="coerce"
)

df.to_csv("task_complete.csv", index=False, encoding="utf-8-sig")
