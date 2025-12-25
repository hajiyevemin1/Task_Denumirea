import fitz

doc = fitz.open("Denumirea2.pdf")
page = doc[0]

x_lines = set()

for d in page.get_drawings():
    for it in d["items"]:
        if it[0] == "re":
            rect = fitz.Rect(it[1])

            if abs(rect.x0 - rect.x1) < 1:
                x_lines.add(round(rect.x0, 2))

x_bounds = sorted(x_lines)
print(x_bounds)