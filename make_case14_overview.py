from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


OUT = Path(r"C:\Users\demon\Documents\ChatGPT\Inżynierka\materiały_na_spotkanie\assets\case14_podsumowanie.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1600, 1120
im = Image.new("RGB", (W, H), "#F7FAFD")
d = ImageDraw.Draw(im)


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def wrapped(text, f, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if d.textlength(candidate, font=f) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def cell_text(text, x, y, width, height, f, fill):
    lines = wrapped(text, f, width - 34)
    line_h = f.size + 8
    top = y + (height - len(lines) * line_h) / 2
    for i, line in enumerate(lines):
        d.text((x + 17, top + i * line_h), line, font=f, fill=fill)


d.text((80, 68), "Sieć testowa case14 w pandapower", font=font(56, True), fill="#17324D")
d.text((82, 143), "Elementy widoczne w dotychczas sprawdzonych tabelach", font=font(29), fill="#526779")

x0, x1 = 80, 1520
y0 = 225
header_h = 76
row_h = 130
columns = [80, 365, 550, 1060, 1520]

d.rounded_rectangle((x0, y0, x1, y0 + header_h + 5 * row_h), radius=18, fill="#FFFFFF", outline="#D4DEE8", width=2)
d.rounded_rectangle((x0, y0, x1, y0 + header_h), radius=18, fill="#183C5B")
d.rectangle((x0, y0 + 45, x1, y0 + header_h), fill="#183C5B")

heads = ["Tabela", "Liczba", "Rola w sieci", "Jak wiąże się z szynami"]
for i, head in enumerate(heads):
    cell_text(head, columns[i], y0, columns[i + 1] - columns[i], header_h, font(25, True), "#FFFFFF")

rows = [
    ("net.bus", "14", "Szyny - punkty połączenia elementów sieci", "Własny indeks 0-13; pole name ma oznaczenia 1-14"),
    ("net.line", "15", "Linie przesyłające energię między szynami", "Końce wskazują pola from_bus oraz to_bus"),
    ("net.trafo", "5", "Transformatory między stroną wyższego i niższego napięcia", "Końce wskazują pola hv_bus oraz lv_bus"),
    ("net.gen", "4", "Generatory - źródła mocy", "Każdy generator wskazuje szynę przez pole bus"),
    ("net.load", "11", "Odbiory - zapotrzebowanie na moc", "Każdy odbiór wskazuje szynę przez pole bus"),
]

for i, row in enumerate(rows):
    y = y0 + header_h + i * row_h
    if i % 2:
        d.rectangle((x0 + 1, y, x1 - 1, y + row_h), fill="#EDF4F9")
    if i:
        d.line((x0, y, x1, y), fill="#D9E3EB", width=2)
    for c, value in enumerate(row):
        f = font(31, True) if c == 1 else font(25, c == 0)
        color = "#126892" if c == 1 else "#20384A"
        cell_text(value, columns[c], y, columns[c + 1] - columns[c], row_h, f, color)

note_y = 1005
d.text((82, note_y), "Model poglądowy do pracy inżynierskiej", font=font(25, True), fill="#17324D")
d.text((82, note_y + 42), "case14 jest obecnie przykładem do analizy; wybór końcowych danych pozostaje otwarty.", font=font(24), fill="#526779")

im.save(OUT, optimize=True)
print(OUT)
