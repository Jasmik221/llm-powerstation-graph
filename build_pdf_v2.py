from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle

import build_pdf as base


ROOT = Path(r"C:\Users\demon\Documents\ChatGPT\Inżynierka")
OUT = ROOT / "materiały_na_spotkanie"
ASSETS = OUT / "assets"
PDF_PATH = OUT / "Wstepne_ustalenia_pracy_inzynierskiej.pdf"


def img_font(size: int, bold: bool = False):
    path = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    return ImageFont.truetype(path, size)


def centered(draw, box, title, subtitle, title_color, subtitle_color):
    x1, y1, x2, y2 = box
    f1 = img_font(38, True)
    f2 = img_font(25)
    b1 = draw.textbbox((0, 0), title, font=f1)
    b2 = draw.textbbox((0, 0), subtitle, font=f2)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
    total = h1 + 24 + h2
    y = y1 + (y2 - y1 - total) / 2
    draw.text((x1 + (x2 - x1 - w1) / 2, y), title, font=f1, fill=title_color)
    draw.text((x1 + (x2 - x1 - w2) / 2, y + h1 + 24), subtitle, font=f2, fill=subtitle_color)


def down_arrow(draw, x, y1, y2):
    draw.line((x, y1, x, y2 - 18), fill="#7D8790", width=6)
    draw.polygon([(x, y2), (x - 16, y2 - 22), (x + 16, y2 - 22)], fill="#7D8790")


def make_full_architecture(path: Path):
    img = PILImage.new("RGB", (1800, 1700), "#FFFFFF")
    d = ImageDraw.Draw(img)
    d.text((90, 55), "Robocza architektura całego systemu", font=img_font(48, True), fill="#000000")
    d.text((90, 120), "Technologie i podział modułów pozostają propozycją do omówienia", font=img_font(26), fill="#66727C")

    boxes = [
        ((270, 220, 1530, 420), "Frontend", "React + TypeScript", "#DCEBFF", "#2E75B6", "#174EA6"),
        ((270, 500, 1530, 700), "Backend API", "Python + FastAPI", "#E3E8FF", "#6673D9", "#3846B7"),
        ((270, 780, 1530, 1015), "Moduł ekstrakcji LLM", "adapter modeli + encje + atrybuty + relacje", "#F1E2FF", "#AA55D4", "#7622A8"),
        ((270, 1095, 1530, 1325), "Walidacja i transformacja", "JSON Schema + Pydantic + reguły domenowe", "#FFF2C8", "#E8AA20", "#A95300"),
        ((270, 1405, 1530, 1620), "Neo4j", "zapis + analiza + zapytania + dane do wizualizacji", "#DDF8E8", "#2BB673", "#006B42"),
    ]
    for box, title, subtitle, fill, outline, text_color in boxes:
        d.rounded_rectangle(box, radius=38, fill=fill, outline=outline, width=5)
        centered(d, box, title, subtitle, text_color, text_color)
    for a, b in zip(boxes[:-1], boxes[1:]):
        down_arrow(d, 900, a[0][3] + 10, b[0][1] - 10)
    img.save(path, quality=95)


def on_page(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFont("Arial", 7.7)
        canvas.setFillColor(base.MID_GRAY)
        canvas.drawString(19 * mm, 287 * mm, "Wstępne ustalenia do pracy inżynierskiej")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(base.MID_GRAY)
    canvas.drawRightString(191 * mm, 10 * mm, f"Strona {page}")
    canvas.restoreState()


def table(headers, rows, widths, center_cols=()):
    return base.styled_table(headers, rows, widths, center_cols=center_cols)


def fig(path, width_mm, caption):
    return base.figure(path, width_mm, caption)


def p(text):
    return base.p(text)


def h1(text):
    return base.h1(text)


def h2(text):
    return base.h2(text)


def bullets(items):
    return base.bullets(items)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    architecture = ASSETS / "architektura_calego_systemu.png"
    make_full_architecture(architecture)

    doc = BaseDocTemplate(
        str(PDF_PATH), pagesize=A4,
        leftMargin=19 * mm, rightMargin=19 * mm,
        topMargin=18 * mm, bottomMargin=17 * mm,
        title="Wstępne ustalenia do pracy inżynierskiej",
        author="",
        subject="Robocza koncepcja systemu LLM do generowania grafów infrastruktury energetycznej",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="notes", frames=[frame], onPage=on_page)])
    story = []

    title = ParagraphStyle("V2Title", parent=base.TITLE, fontSize=25, leading=30)
    subtitle = ParagraphStyle("V2Subtitle", parent=base.SUBTITLE, fontSize=13)
    note = ParagraphStyle("Working", parent=base.META, fontName="Arial-Bold", textColor=base.BLUE, fontSize=10)

    story += [Spacer(1, 35 * mm), Paragraph("MATERIAŁ ROBOCZY", note), Spacer(1, 5 * mm)]
    story += [Paragraph("Wstępne ustalenia do pracy inżynierskiej", title)]
    story += [Paragraph("System generowania grafów infrastruktury energetycznej z wykorzystaniem modeli LLM", subtitle)]
    story += [Spacer(1, 45 * mm)]
    story += [Paragraph("Dokument do rozmowy z promotorem<br/>Założenia mogą ulec zmianie po konsultacji", base.META)]
    story += [Spacer(1, 50 * mm)]
    story += [Paragraph("21 października 2026", base.META), PageBreak()]

    story += [h1("Charakter dokumentu")]
    story += [p("To robocze podsumowanie pomysłów z początku pracy. Dokument nie opisuje zatwierdzonej architektury ani ostatecznego zakresu implementacji. Ma pomóc podczas spotkania ustalić, które elementy warto zachować, uprościć albo zmienić.")]
    story += [h1("Główna idea")]
    story += [p("System ma przyjmować opis tekstowy infrastruktury energetycznej, rozpoznawać obiekty oraz relacje, przekształcać wynik do kontrolowanej struktury i zapisywać go w bazie grafowej. Użytkownik powinien następnie móc obejrzeć graf i wykonywać podstawowe zapytania lub analizy.")]
    story += [h1("Co jest ustalone, a co pozostaje propozycją")]
    story += [table(["Element", "Aktualny status", "Uwagi"], [
        ["LLM przekształca opis w encje i relacje", "główna idea pracy", "To rdzeń proponowanego systemu."],
        ["Grafowa reprezentacja infrastruktury", "główna idea pracy", "Szczegółowy model wymaga zatwierdzenia."],
        ["Neo4j", "wstępna propozycja", "Pasuje do grafu właściwościowego, ale wybór nie jest jeszcze ostateczny."],
        ["Python i FastAPI", "wstępna propozycja", "Możliwy backend prototypu."],
        ["React i TypeScript", "wstępna propozycja", "Możliwy frontend, jeśli powstanie osobny interfejs webowy."],
        ["Modele przez API lub Ollama", "wstępna propozycja", "Architektura powinna umożliwiać wymianę modelu."],
        ["pandapower i case14", "przykład do analizy", "Nie podjęto decyzji, że będzie to główne źródło danych."],
    ], [49 * mm, 39 * mm, 84 * mm], center_cols=(1,))]

    story += [PageBreak(), h1("Robocza architektura całego systemu")]
    story += [p("Poniższy układ pokazuje pełny przepływ od interfejsu użytkownika do bazy grafowej. Jest to propozycja organizacji prototypu, a nie zamknięta decyzja technologiczna.")]
    story += [fig(architecture, 150, "Rysunek 1  Robocza architektura aplikacji")]
    story += [p("Frontend odpowiadałby za wprowadzanie opisu i prezentację wyników. Backend koordynowałby wywołanie modelu, walidację danych i komunikację z Neo4j. Moduł LLM nie otrzymywałby bezpośredniego dostępu do bazy.")]

    story += [PageBreak(), h1("Rola poszczególnych części")]
    story += [table(["Część", "Możliwa technologia", "Odpowiedzialność"], [
        ["Frontend", "React + TypeScript", "Opis sieci, wybór modelu, podgląd grafu, błędy i eksport."],
        ["Backend API", "Python + FastAPI", "Sterowanie procesem, obsługa żądań, sesji i komunikacji między modułami."],
        ["Adapter modeli", "API dostawcy lub Ollama", "Wspólny interfejs umożliwiający podmianę modelu bez zmiany reszty systemu."],
        ["Ekstrakcja LLM", "prompt + structured output", "Rozpoznanie encji, atrybutów i relacji z opisu."],
        ["Walidacja", "JSON Schema + Pydantic", "Sprawdzenie formatu, typów, jednostek, identyfikatorów i relacji."],
        ["Transformacja", "Python", "Odwzorowanie zweryfikowanej struktury na węzły i relacje grafu."],
        ["Baza grafowa", "Neo4j", "Przechowywanie, zapytania, analiza topologii i dane do wizualizacji."],
    ], [38 * mm, 47 * mm, 87 * mm])]
    story += [h2("Główny przepływ")]
    story += bullets([
        "Użytkownik wprowadza opis sieci w interfejsie.",
        "Backend przekazuje opis, schemat odpowiedzi i instrukcję do wybranego modelu.",
        "LLM zwraca encje, właściwości i relacje w ustrukturyzowanym formacie.",
        "Walidator sprawdza wynik i przekazuje użytkownikowi błędy wymagające poprawy.",
        "Poprawne dane są mapowane na graf i zapisywane w Neo4j.",
        "Frontend pobiera graf lub wyniki zapytań i prezentuje je użytkownikowi.",
    ])

    story += [PageBreak(), h1("Możliwe źródła danych i graf referencyjny")]
    story += [p("Do oceny jakości LLM potrzebny będzie graf wzorcowy albo ręcznie przygotowany zbiór odpowiedzi. Sposób jego uzyskania nie został jeszcze ustalony. pandapower jest jedną z możliwych opcji, ponieważ udostępnia sieci testowe w ustrukturyzowanych tabelach, lecz można rozważyć również inne zbiory lub własne przykłady.")]
    story += [table(["Możliwość", "Zastosowanie", "Otwarte kwestie"], [
        ["pandapower", "Automatyczne utworzenie grafu referencyjnego z tabel DataFrame", "Wybór sieci, wersji biblioteki i zakresu parametrów"],
        ["Inne sieci testowe", "Sprawdzenie, czy podejście działa poza jednym przykładem", "Format danych i możliwość automatycznego mapowania"],
        ["Dane rzeczywiste", "Ocena na opisach bliższych praktyce", "Dostępność, kompletność i kwestie poufności"],
        ["Przykłady przygotowane ręcznie", "Małe scenariusze kontrolowane na początku projektu", "Nakład pracy i ryzyko małej reprezentatywności"],
    ], [39 * mm, 69 * mm, 64 * mm])]
    story += [h2("Dotychczas sprawdzony przykład case14")]
    story += [p("W ramach rozpoznania odczytano strukturę pandapower case14. Wynik pokazuje, że biblioteka nadaje się do eksperymentalnego mapowania tabel na graf, ale nie przesądza o jej wykorzystaniu w końcowym systemie.")]
    story += [table(["Tabela", "Liczba rekordów", "Możliwy węzeł grafu"], [
        ["net.bus", "14", "Bus"],
        ["net.line", "15", "Line"],
        ["net.trafo", "5", "Transformer"],
        ["net.gen", "4", "Generator"],
        ["net.load", "11", "Load"],
    ], [48 * mm, 48 * mm, 76 * mm], center_cols=(1,))]
    story += [p("Ważna obserwacja techniczna: indeks szyny w DataFrame ma wartości 0-13, natomiast pole name zawiera oznaczenia 1-14. Jeśli pandapower zostanie wybrane, relacje należy budować na podstawie indeksów, a name traktować jako właściwość opisową.")]

    story += [PageBreak(), h1("Wstępny model grafu")]
    story += [p("Poniższy schemat jest punktem startowym do rozmowy. Linie i transformatory zostały przedstawione jako osobne węzły, ponieważ ułatwia to przechowywanie ich parametrów oraz porównywanie elementów wykrytych przez LLM. Możliwy jest też prostszy wariant, w którym część elementów stanowi relacje z właściwościami.")]
    story += [fig(ASSETS / "schemat_grafu.png", 170, "Rysunek 2  Jedna z możliwych reprezentacji grafowej")]
    story += [h2("Przykładowe typy")]
    story += [table(["Węzły", "Relacje"], [
        ["Bus, Line, Transformer", "FROM_BUS, TO_BUS"],
        ["Generator, ExternalGrid", "CONNECTED_TO"],
        ["Load, Shunt", "HV_BUS, LV_BUS"],
    ], [86 * mm, 86 * mm])]

    story += [PageBreak(), h1("Przykładowe zapytania do grafu")]
    story += [p("Po zapisaniu grafu użytkownik mógłby zadawać pytania o jego elementy i połączenia. Poniższe propozycje pomagają określić minimalny zakres funkcji analitycznych prototypu. Ich dokładna postać zależy od uzgodnionego schematu grafu.")]
    story += [table(["Pytanie użytkownika", "Oczekiwany wynik", "Zastosowanie"], [
        ["Ile jest elementów każdego typu?", "Liczba szyn, linii, transformatorów, źródeł i odbiorów.", "Szybki przegląd zawartości grafu."],
        ["Co jest podłączone do wybranej szyny?", "Sąsiednie linie, transformatory, generatory i odbiory.", "Analiza otoczenia wskazanego elementu."],
        ["Które szyny łączy dana linia lub transformator?", "Dwa końce wybranego elementu oraz jego właściwości.", "Sprawdzenie relacji wyekstrahowanych z tekstu."],
        ["Jakie elementy leżą na trasie między dwiema szynami?", "Ścieżka połączeń albo informacja o jej braku.", "Analiza topologii sieci."],
        ["Które elementy mają niepełne dane?", "Lista obiektów bez wymaganych atrybutów lub połączeń.", "Kontrola jakości danych przed analizą."],
        ["Z którego fragmentu opisu pochodzi element?", "Obiekt i przypisany mu fragment tekstu, jeśli będzie przechowywany.", "Wyjaśnienie wyniku i ręczna korekta."],
    ], [59 * mm, 61 * mm, 52 * mm])]
    story += [h2("Dwa orientacyjne przykłady Cypher")]
    story += [p("Zliczenie elementów według etykiety węzła:")]
    story += [base.code_block("MATCH (n)\nRETURN labels(n)[0] AS typ, count(*) AS liczba\nORDER BY typ"), Spacer(1, 3 * mm)]
    story += [p("Linie podłączone do wskazanej szyny (parametr <font name='Courier'>$bus_id</font>):")]
    story += [base.code_block("MATCH (b:Bus {id: $bus_id})<-[:FROM_BUS|TO_BUS]-(l:Line)\nRETURN l.id AS linia, l.length_km AS dlugosc_km"), Spacer(1, 3 * mm)]
    story += [p("Przykłady zakładają, że identyfikator jest przechowywany jako właściwość id, a linia jest węzłem połączonym relacjami FROM_BUS i TO_BUS z szynami. Po decyzji o modelu grafu trzeba doprecyzować składnię oraz zakres zapytań dostępnych w interfejsie.")]

    story += [PageBreak(), h1("Wstępny format wyniku LLM")]
    story += [p("Model może zwracać wynik JSON zawierający listę obiektów i relacji. Dokładna struktura będzie zależeć od zatwierdzonego modelu grafu. Backend powinien przyjmować wyłącznie dane zgodne ze schematem oraz zgłaszać brakujące lub sprzeczne informacje.")]
    story += [base.code_block('{\n  "nodes": [\n    {"id": "B1", "type": "Bus", "properties": {"vn_kv": 110}},\n    {"id": "L1", "type": "Line", "properties": {"length_km": 10}}\n  ],\n  "relationships": [\n    {"type": "FROM_BUS", "from": "L1", "to": "B1"}\n  ]\n}')]
    story += [h2("Przykładowe reguły walidacji")]
    story += bullets([
        "Każdy obiekt ma identyfikator i typ należący do uzgodnionego słownika.",
        "Relacja wskazuje obiekty, które istnieją w tej samej odpowiedzi.",
        "Dany typ relacji łączy tylko dozwolone typy węzłów.",
        "Właściwości liczbowe mają określone jednostki i dopuszczalne zakresy.",
        "Brak informacji w opisie jest oznaczany jako brak, a nie uzupełniany domysłem modelu.",
    ])
    story += [h2("Co pozostaje do ustalenia")]
    story += bullets([
        "Czy jeden schemat ma obsługiwać różne rodzaje sieci energetycznych.",
        "Jak przechowywać fragment tekstu, z którego pochodzi obiekt lub relacja.",
        "Czy zapisywać poziom pewności modelu i informacje o użytym modelu lub promptach.",
        "Jak obsługiwać korekty użytkownika przed zapisem grafu.",
    ])

    story += [PageBreak(), h1("Możliwy widok aplikacji")]
    story += [p("Interfejs nie musi być rozbudowany. W pierwszym prototypie wystarczy ekran pozwalający wprowadzić opis, uruchomić ekstrakcję, zobaczyć wynik walidacji oraz obejrzeć wygenerowany graf. Makieta pokazuje jedynie możliwe rozmieszczenie funkcji.")]
    story += [fig(ASSETS / "makieta_aplikacji.png", 170, "Rysunek 3  Robocza makieta interfejsu")]
    story += [table(["Obszar", "Możliwy zakres"], [
        ["Opis", "Pole tekstowe, wybór modelu i uruchomienie procesu"],
        ["Graf", "Podgląd węzłów i relacji oraz filtrowanie typów"],
        ["Szczegóły", "Właściwości zaznaczonego elementu i źródło informacji"],
        ["Walidacja", "Lista ostrzeżeń, błędów i elementów wymagających zatwierdzenia"],
    ], [45 * mm, 127 * mm])]

    story += [PageBreak(), h1("Wstępna koncepcja ewaluacji")]
    story += [p("Ewaluacja powinna porównywać wynik LLM z oczekiwaną strukturą, niezależnie od tego, czy graf referencyjny powstanie z pandapower, innych danych czy zostanie przygotowany ręcznie.")]
    story += [table(["Obszar", "Przykładowa miara", "Pytanie"], [
        ["Węzły", "precision, recall, F1", "Czy model wykrył właściwe obiekty?"],
        ["Relacje", "precision, recall, F1", "Czy połączenia i ich kierunki są poprawne?"],
        ["Atrybuty", "exact match lub błąd liczbowy", "Czy wartości i jednostki zgadzają się z opisem?"],
        ["Format", "odsetek poprawnych odpowiedzi", "Jak często wynik przechodzi walidację bez naprawy?"],
        ["Efektywność", "czas, tokeny, koszt", "Jak drogie i szybkie jest pojedyncze przetworzenie?"],
    ], [36 * mm, 57 * mm, 79 * mm])]
    story += [h2("Możliwe porównania")]
    story += bullets([
        "Modele lokalne i modele dostępne przez API.",
        "Prompt bez przykładów i prompt zawierający kilka przykładów.",
        "Zwykła odpowiedź tekstowa i wymuszony structured output.",
        "Opisy proste, złożone, niepełne i niejednoznaczne.",
    ])
    story += [h2("To również wymaga uzgodnienia")]
    story += [p("Trzeba określić, ile modeli i wariantów promptów porównać oraz jakie dane zapewnią wystarczającą wiarygodność wyników w pracy inżynierskiej.")]

    story += [PageBreak(), h1("Proponowane następne kroki")]
    story += [table(["Krok", "Cel"], [
        ["1 Uzgodnienie zakresu", "Określenie, co dokładnie ma znaleźć się w działającym prototypie."],
        ["2 Wybór modelu grafu", "Zatwierdzenie typów węzłów, relacji i minimalnych właściwości."],
        ["3 Wybór danych", "Decyzja, czy wykorzystać pandapower, inne sieci, dane ręczne lub ich połączenie."],
        ["4 Mały eksperyment", "Opis kilku elementów, ekstrakcja do JSON i ręczne porównanie wyniku."],
        ["5 Graf w Neo4j", "Zapis zweryfikowanego przykładu i wykonanie podstawowych zapytań."],
        ["6 Prototyp aplikacji", "Połączenie interfejsu, backendu, modelu i bazy."],
        ["7 Ewaluacja", "Przygotowanie większego zbioru i porównanie wybranych wariantów."],
    ], [46 * mm, 126 * mm])]
    story += [h1("Pytania na spotkanie")]
    story += bullets([
        "Czy taka ogólna architektura systemu odpowiada zakresowi pracy?",
        "Czy frontend webowy jest potrzebny, czy wystarczy prostszy interfejs demonstracyjny?",
        "Czy Neo4j ma pozostać docelową bazą grafową?",
        "Czy linie i transformatory reprezentować jako węzły, czy jako relacje z właściwościami?",
        "Jakie źródło danych będzie odpowiednie do utworzenia grafu referencyjnego?",
        "Czy warto dalej analizować pandapower i case14, czy wybrać inne dane?",
        "Jak szeroka powinna być ewaluacja modeli i promptów?",
        "Czy obliczenia elektroenergetyczne wchodzą w zakres, czy system ma skupić się na ekstrakcji i grafach?",
    ])

    story += [PageBreak(), h1("Podsumowanie robocze")]
    story += [p("Najbardziej stabilnym elementem pomysłu jest przepływ od opisu tekstowego do grafu: LLM rozpoznaje informacje, backend je sprawdza i zapisuje w bazie grafowej. Pozostałe decyzje, w tym konkretne technologie, źródła danych, szczegółowy schemat grafu oraz zakres interfejsu, powinny zostać omówione z promotorem.")]
    story += [p("pandapower i case14 są na tym etapie przykładem, który pomógł sprawdzić, jak mogą wyglądać ustrukturyzowane dane infrastruktury. Nie oznacza to jeszcze wyboru tej biblioteki jako podstawy całej pracy.")]
    story += [h2("Materiały pomocnicze")]
    refs = [
        "pandapower Power System Test Cases: https://pandapower.readthedocs.io/en/v3.5.6/networks/power_system_test_cases.html",
        "pandapower repository: https://github.com/e2nIEE/pandapower",
        "Neo4j graph database concepts: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/",
    ]
    story += bullets(refs)

    doc.build(story)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
