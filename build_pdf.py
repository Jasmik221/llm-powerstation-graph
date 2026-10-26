from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    XPreformatted,
)


ROOT = Path(r"C:\Users\demon\Documents\ChatGPT\Inżynierka")
OUT = ROOT / "materiały_na_spotkanie"
ASSETS = OUT / "assets"
PDF_PATH = OUT / "Raport_poczatkowy_pracy_inzynierskiej.pdf"

NAVY = colors.HexColor("#16324F")
BLUE = colors.HexColor("#2E75B6")
PALE_BLUE = colors.HexColor("#EAF2F8")
PALE_GRAY = colors.HexColor("#F3F5F7")
MID_GRAY = colors.HexColor("#66727C")
LIGHT_BORDER = colors.HexColor("#D9D9D9")
WHITE = colors.white
BLACK = colors.black


pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", r"C:\Windows\Fonts\ariali.ttf"))
pdfmetrics.registerFont(TTFont("Consolas", r"C:\Windows\Fonts\consola.ttf"))


styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "ReportTitle", fontName="Arial-Bold", fontSize=24, leading=29,
    alignment=TA_CENTER, textColor=BLACK, spaceAfter=10 * mm,
)
SUBTITLE = ParagraphStyle(
    "Subtitle", fontName="Arial", fontSize=13, leading=17,
    alignment=TA_CENTER, textColor=MID_GRAY, spaceAfter=6 * mm,
)
H1 = ParagraphStyle(
    "H1", fontName="Arial-Bold", fontSize=16, leading=20,
    textColor=BLACK, spaceBefore=4 * mm, spaceAfter=3 * mm, keepWithNext=True,
)
H2 = ParagraphStyle(
    "H2", fontName="Arial-Bold", fontSize=12.5, leading=16,
    textColor=BLACK, spaceBefore=3 * mm, spaceAfter=2 * mm, keepWithNext=True,
)
BODY = ParagraphStyle(
    "Body", fontName="Arial", fontSize=9.5, leading=13.4,
    textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=2.7 * mm,
)
SMALL = ParagraphStyle(
    "Small", fontName="Arial", fontSize=8.3, leading=10.5,
    textColor=BLACK, alignment=TA_LEFT,
)
CAPTION = ParagraphStyle(
    "Caption", fontName="Arial-Italic", fontSize=8.2, leading=10.5,
    textColor=MID_GRAY, alignment=TA_CENTER, spaceBefore=1.5 * mm, spaceAfter=3 * mm,
)
BULLET = ParagraphStyle(
    "Bullet", fontName="Arial", fontSize=9.4, leading=12.5,
    leftIndent=5 * mm, firstLineIndent=-3.2 * mm, bulletIndent=0,
    textColor=BLACK, alignment=TA_LEFT, spaceAfter=1.8 * mm,
)
CODE = ParagraphStyle(
    "Code", fontName="Consolas", fontSize=7.8, leading=10.2,
    textColor=colors.HexColor("#233746"), leftIndent=3 * mm, rightIndent=3 * mm,
    spaceBefore=2 * mm, spaceAfter=3 * mm,
)
META = ParagraphStyle(
    "Meta", fontName="Arial", fontSize=9.2, leading=12,
    textColor=MID_GRAY, alignment=TA_CENTER,
)


def p(text, style=BODY):
    return Paragraph(text, style)


def h1(text):
    return Paragraph(text, H1)


def h2(text):
    return Paragraph(text, H2)


def bullets(items):
    return [Paragraph("• " + escape(item), BULLET) for item in items]


def styled_table(headers, rows, widths, font_size=7.8, center_cols=()):
    data = [[Paragraph(f'<font color="#FFFFFF"><b>{escape(str(v))}</b></font>', SMALL) for v in headers]]
    for row in rows:
        data.append([Paragraph(escape(str(v)), SMALL) for v in row])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="CENTER", splitByRow=1)
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, LIGHT_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for r in range(1, len(data)):
        commands.append(("BACKGROUND", (0, r), (-1, r), PALE_BLUE if r % 2 == 0 else WHITE))
    for c in center_cols:
        commands.append(("ALIGN", (c, 1), (c, -1), "CENTER"))
    table.setStyle(TableStyle(commands))
    return table


def code_block(text):
    table = Table([[XPreformatted(escape(text), CODE)]], colWidths=[172 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_GRAY),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C8D0D7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def figure(path, width_mm, caption):
    img = Image(str(path), width=width_mm * mm)
    iw, ih = img.imageWidth, img.imageHeight
    img.drawHeight = img.drawWidth * ih / iw
    img.hAlign = "CENTER"
    return KeepTogether([img, Paragraph(caption, CAPTION)])


def on_page(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFont("Arial", 7.7)
        canvas.setFillColor(MID_GRAY)
        canvas.drawString(19 * mm, 287 * mm, "Raport początkowy pracy inżynierskiej")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawRightString(191 * mm, 10 * mm, f"Strona {page}")
    canvas.restoreState()


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(PDF_PATH), pagesize=A4,
        leftMargin=19 * mm, rightMargin=19 * mm,
        topMargin=18 * mm, bottomMargin=17 * mm,
        title="Raport początkowy pracy inżynierskiej",
        author="",
        subject="System generowania grafów infrastruktury energetycznej z wykorzystaniem modeli LLM",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=on_page)])
    story = []

    # Cover
    story += [Spacer(1, 33 * mm)]
    story += [Paragraph("RAPORT POCZĄTKOWY", ParagraphStyle("Eyebrow", parent=META, fontName="Arial-Bold", textColor=BLUE, fontSize=10))]
    story += [Spacer(1, 5 * mm)]
    story += [Paragraph("System generowania grafów infrastruktury energetycznej z wykorzystaniem modeli LLM", TITLE)]
    story += [Paragraph("Stan przygotowań i koncepcja prototypu", SUBTITLE)]
    story += [Spacer(1, 35 * mm)]
    story += [Paragraph("<b>Temat pracy</b>", META), Spacer(1, 3 * mm)]
    story += [Paragraph("Implementacja modeli LLM wspierających infrastrukturę energetyczną z użyciem baz grafowych", ParagraphStyle("Topic", parent=BODY, fontName="Arial-Bold", fontSize=11, leading=15, alignment=TA_CENTER))]
    story += [Spacer(1, 35 * mm)]
    story += [Paragraph("Materiał na spotkanie z promotorem<br/>21 października 2026", META)]
    story += [PageBreak()]

    story += [h1("Cel dokumentu")]
    story += [p("Dokument podsumowuje decyzje podjęte na początku pracy inżynierskiej oraz przedstawia proponowany kierunek implementacji. Głównym zadaniem systemu będzie przekształcanie tekstowych opisów infrastruktury elektroenergetycznej w ustrukturyzowane grafy przechowywane w Neo4j. Pierwsza wersja prototypu wykorzysta sieć pandapower case14 jako źródło danych referencyjnych.")]
    story += [p("Najważniejszym kolejnym krokiem jest zatwierdzenie modelu grafowego i minimalnego zakresu danych. Po tej decyzji można zaimplementować deterministyczny konwerter pandapower do Neo4j, a następnie uruchomić niezależną ścieżkę ekstrakcji informacji z tekstu przez LLM.")]
    story += [h1("Zakres pracy")]
    story += bullets([
        "Ocena zdolności modeli językowych do rozpoznawania elementów infrastruktury, ich właściwości i wzajemnych połączeń.",
        "Opracowanie procesu konwersji wyekstrahowanych informacji do grafu właściwościowego.",
        "Implementacja prototypu łączącego Python, modele LLM, walidację danych i Neo4j.",
        "Wizualizacja grafu oraz podstawowa analiza topologii i połączeń.",
        "Porównanie grafów wygenerowanych przez LLM z grafem referencyjnym utworzonym bez udziału modelu.",
    ])
    story += [h1("Stan przygotowań")]
    story += [styled_table(["Obszar", "Aktualne ustalenie", "Status"], [
        ["Dane startowe", "pandapower.networks.case14()", "ustalone"],
        ["Baza grafowa", "Neo4j i model property graph", "ustalone"],
        ["Backend", "Python", "ustalone"],
        ["Integracja LLM", "Wymienny adapter dla API oraz modeli lokalnych przez Ollama", "koncepcja"],
        ["Format pośredni", "JSON zgodny ze schematem i walidowany przez Pydantic", "koncepcja"],
        ["Ewaluacja", "Porównanie z grafem referencyjnym oraz analiza błędów", "koncepcja"],
        ["Implementacja", "Kod prototypu i eksperymenty", "do wykonania"],
    ], [33 * mm, 111 * mm, 28 * mm], center_cols=(2,))]

    story += [PageBreak(), h1("Dane wejściowe pandapower case14")]
    story += [p("Sieć case14 stanowi niewielki, kontrolowany przykład, który pozwala sprawdzić pełny proces bez wprowadzania na początku dużego zbioru danych. Dane są przechowywane w tabelach pandas DataFrame. Każdy rekord może zostać odwzorowany na węzeł grafu, a kolumny wskazujące szyny umożliwiają utworzenie relacji.")]
    story += [styled_table(["Tabela", "Liczba", "Węzeł", "Główne odwołania"], [
        ["net.bus", "14", "Bus", "indeks 0-13, name 1-14, geo"],
        ["net.line", "15", "Line", "from_bus, to_bus"],
        ["net.trafo", "5", "Transformer", "hv_bus, lv_bus"],
        ["net.gen", "4", "Generator", "bus"],
        ["net.load", "11", "Load", "bus"],
        ["net.ext_grid", "do potwierdzenia", "ExternalGrid", "bus"],
        ["net.shunt", "do potwierdzenia", "Shunt", "bus"],
    ], [29 * mm, 30 * mm, 40 * mm, 73 * mm], center_cols=(1,))]
    story += [Spacer(1, 3 * mm)]
    story += [p("<b>Indeks rekordu i pole name mają inne znaczenie.</b> Dla szyn indeks DataFrame przyjmuje wartości od 0 do 13, natomiast name zawiera oznaczenia od 1 do 14. Relacje trzeba tworzyć na podstawie indeksów używanych w kolumnach from_bus, to_bus, hv_bus, lv_bus i bus. Nazwa powinna pozostać właściwością opisową.")]
    story += [p("Przed implementacją należy przypiąć wersję pandapower w pliku zależności. Pozwoli to zachować powtarzalność wyników i uniknąć różnic w strukturze danych między wersjami biblioteki.")]
    story += [h2("Minimalny zakres pierwszej wersji")]
    story += bullets([
        "Wczytanie tabel bus, line, trafo, gen i load oraz sprawdzenie ext_grid i shunt.",
        "Zachowanie oryginalnego indeksu pandapower w polu pp_index.",
        "Utworzenie stabilnego identyfikatora source_id zawierającego nazwę sieci, typ elementu i indeks.",
        "Przeniesienie parametrów wymaganych do identyfikacji, wizualizacji i pierwszych eksperymentów.",
        "Oddzielenie danych wejściowych od wyników obliczeń rozpływu mocy, takich jak res_bus i res_line.",
    ])

    story += [PageBreak(), h1("Architektura systemu")]
    story += [p("Prototyp będzie zawierał dwie ścieżki generowania grafu. Pierwsza przekształci dane pandapower bezpośrednio do Neo4j i utworzy wynik referencyjny. Druga przetworzy opis tekstowy przez model LLM, zapisze wynik w JSON, zweryfikuje go i dopiero wtedy utworzy graf. Obie ścieżki powinny korzystać z tego samego modelu domenowego.")]
    story += [figure(ASSETS / "architektura.png", 171, "Rysunek 1  Proponowana architektura prototypu")]
    story += [h2("Odpowiedzialność komponentów")]
    story += [styled_table(["Komponent", "Odpowiedzialność"], [
        ["Moduł pandapower", "Wczytuje sieć referencyjną i udostępnia tabele DataFrame."],
        ["Konwerter referencyjny", "Mapuje rekordy tabel na węzły, właściwości i relacje Neo4j."],
        ["Adapter LLM", "Zapewnia wspólny interfejs dla zewnętrznego API i lokalnej Ollamy."],
        ["Warstwa promptów", "Przekazuje reguły ekstrakcji, schemat odpowiedzi i przykłady few shot."],
        ["Walidator", "Sprawdza strukturę JSON, typy, jednostki, identyfikatory i relacje."],
        ["Repozytorium Neo4j", "Tworzy graf wyłącznie na podstawie zweryfikowanych obiektów."],
        ["Moduł ewaluacji", "Porównuje graf wygenerowany z referencyjnym i zapisuje błędy."],
    ], [45 * mm, 127 * mm])]

    story += [PageBreak(), h1("Proces tworzenia grafu referencyjnego")]
    story += [p("Graf referencyjny powstanie klasycznym skryptem Pythona. LLM nie uczestniczy w tym procesie, dlatego wynik może służyć jako punkt odniesienia podczas ewaluacji.")]
    story += bullets([
        "Wczytanie net = pandapower.networks.case14().",
        "Odczyt wybranych tabel i kolumn oraz normalizacja brakujących wartości.",
        "Utworzenie węzłów Bus przed elementami wskazującymi szyny.",
        "Utworzenie węzłów Line, Transformer, Generator, Load i pozostałych urządzeń.",
        "Utworzenie relacji na podstawie indeksów pandapower.",
        "Sprawdzenie liczby węzłów i relacji oraz zapis manifestu importu.",
    ])
    story += [h2("Zasada identyfikacji")]
    story += [p("Każdy element powinien mieć stabilny identyfikator niezależny od pola name. Proponowany format source_id zapobiega kolizjom między typami elementów i między różnymi sieciami testowymi.")]
    story += [code_block("case14:bus:0\ncase14:line:0\ncase14:trafo:0\ncase14:load:0")]
    story += [h2("Kontrole jakości importu")]
    story += [styled_table(["Kontrola", "Oczekiwany wynik"], [
        ["Liczba szyn", "14 węzłów Bus"],
        ["Liczba linii", "15 węzłów Line"],
        ["Liczba transformatorów", "5 węzłów Transformer"],
        ["Liczba generatorów", "4 węzły Generator"],
        ["Liczba odbiorów", "11 węzłów Load"],
        ["Integralność relacji", "Każda relacja wskazuje istniejący węzeł Bus"],
        ["Unikalność", "Brak powtórzonych source_id w obrębie etykiety"],
    ], [57 * mm, 115 * mm])]

    story += [PageBreak(), h1("Proces generowania grafu z opisu")]
    story += [p("Model językowy nie powinien bezpośrednio wykonywać zapytań zapisujących dane. Jego zadaniem będzie przygotowanie propozycji struktury w kontrolowanym formacie. Backend pozostanie odpowiedzialny za reguły biznesowe, walidację i transakcję Neo4j.")]
    story += [styled_table(["Etap", "Działanie", "Możliwy błąd"], [
        ["1", "Użytkownik wprowadza opis infrastruktury", "Brak danych koniecznych do odtworzenia grafu"],
        ["2", "Prompt przekazuje schemat i reguły ekstrakcji", "Niejednoznaczna instrukcja lub za mało przykładów"],
        ["3", "LLM identyfikuje encje, właściwości i relacje", "Pominięcie, duplikat lub halucynacja"],
        ["4", "Model zwraca dane zgodne z JSON Schema", "Błąd składni albo niedozwolony typ"],
        ["5", "Pydantic i reguły domenowe sprawdzają wynik", "Nieistniejący identyfikator lub zła jednostka"],
        ["6", "Warstwa repozytorium zapisuje graf", "Naruszenie constraint lub błąd transakcji"],
    ], [13 * mm, 83 * mm, 76 * mm], center_cols=(0,))]
    story += [h2("Wstępny kontrakt JSON")]
    story += [code_block('{\n  "network_id": "example_01",\n  "nodes": [\n    {"id": "B1", "type": "Bus", "properties": {"vn_kv": 110}},\n    {"id": "L1", "type": "Line", "properties": {"length_km": 10}}\n  ],\n  "relationships": [\n    {"type": "FROM_BUS", "from": "L1", "to": "B1"}\n  ]\n}')]
    story += [p("Schemat odpowiedzi powinien ograniczać wartości pola type do uzgodnionego słownika. Walidacja semantyczna musi dodatkowo sprawdzać istnienie wskazanych obiektów, dopuszczalne kierunki relacji, jednostki oraz wartości wymagane dla poszczególnych typów.")]

    story += [PageBreak(), h1("Wstępny model bazy grafowej")]
    story += [p("Proponowany model traktuje linie i transformatory jako osobne węzły. Dzięki temu ich parametry techniczne pozostają bezpośrednio dostępne, a odwzorowanie jest zbliżone do struktury tabel pandapower. Rozwiązanie upraszcza też ocenę, czy LLM poprawnie rozpoznał konkretny element infrastruktury.")]
    story += [figure(ASSETS / "schemat_grafu.png", 170, "Rysunek 2  Wstępny schemat węzłów i relacji Neo4j")]
    story += [p("Identyfikator techniczny może mieć postać <b>source_id = sieć:typ:pp_index</b>, na przykład case14:bus:0. Oryginalny indeks pozostaje dodatkowo dostępny w polu pp_index.")]

    story += [PageBreak(), h1("Typy węzłów")]
    story += [h2("Typy węzłów")]
    story += [styled_table(["Etykieta", "Znaczenie", "Przykładowe właściwości"], [
        ["Bus", "Szyna lub węzeł elektryczny", "source_id, pp_index, name, vn_kv, type, zone, geo, in_service"],
        ["Line", "Linia elektroenergetyczna", "source_id, pp_index, length_km, r_ohm_per_km, x_ohm_per_km, max_i_ka"],
        ["Transformer", "Transformator dwuuzwojeniowy", "source_id, pp_index, sn_mva, vn_hv_kv, vn_lv_kv, vk_percent, tap_pos"],
        ["Generator", "Generator sterowany", "source_id, pp_index, p_mw, vm_pu, min_q_mvar, max_q_mvar"],
        ["ExternalGrid", "Węzeł bilansujący lub sieć zewnętrzna", "source_id, pp_index, vm_pu, va_degree"],
        ["Load", "Odbiór mocy", "source_id, pp_index, p_mw, q_mvar, scaling, in_service"],
        ["Shunt", "Element poprzeczny", "source_id, pp_index, p_mw, q_mvar, step"],
    ], [28 * mm, 50 * mm, 94 * mm])]
    story += [PageBreak(), h1("Typy relacji")]
    story += [styled_table(["Relacja", "Źródło", "Cel", "Znaczenie"], [
        ["FROM_BUS", "Line", "Bus", "Początkowa szyna linii"],
        ["TO_BUS", "Line", "Bus", "Końcowa szyna linii"],
        ["HV_BUS", "Transformer", "Bus", "Strona wysokiego napięcia"],
        ["LV_BUS", "Transformer", "Bus", "Strona niskiego napięcia"],
        ["CONNECTED_TO", "Generator, Load, ExternalGrid, Shunt", "Bus", "Przyłączenie urządzenia do szyny"],
    ], [31 * mm, 51 * mm, 23 * mm, 67 * mm], center_cols=(0, 2))]
    story += [p("Zakres właściwości jest wstępny. Ostateczną listę należy zatwierdzić po wydrukowaniu pełnych nazw kolumn w używanej wersji pandapower oraz po ustaleniu, które parametry będą oceniane w eksperymentach.")]

    story += [PageBreak(), h1("Ograniczenia i zapis w Neo4j")]
    story += [p("W pierwszej wersji wystarczą ograniczenia unikalności dla source_id w każdej etykiecie. Właściwości wymagane i typy danych można sprawdzać przede wszystkim w warstwie Pydantic, co pozwoli zachować zgodność także w Neo4j Community Edition.")]
    story += [code_block("CREATE CONSTRAINT bus_source_id IF NOT EXISTS\nFOR (n:Bus) REQUIRE n.source_id IS UNIQUE;\n\nCREATE CONSTRAINT line_source_id IF NOT EXISTS\nFOR (n:Line) REQUIRE n.source_id IS UNIQUE;\n\nCREATE CONSTRAINT transformer_source_id IF NOT EXISTS\nFOR (n:Transformer) REQUIRE n.source_id IS UNIQUE;")]
    story += [p("Import powinien używać MERGE dla elementów identyfikowanych przez source_id oraz transakcji obejmującej spójny fragment sieci. Dane referencyjne i wyniki LLM warto rozdzielić polem graph_variant albo osobnymi bazami, aby przypadkowo ich nie połączyć.")]
    story += [h2("Przykładowe wzorce Cypher")]
    story += [code_block("MERGE (b:Bus {source_id: $source_id})\nSET b += $properties;\n\nMATCH (l:Line {source_id: $line_id})\nMATCH (b:Bus {source_id: $bus_id})\nMERGE (l)-[:FROM_BUS]->(b);")]
    story += [h2("Otwarte decyzje dotyczące modelu")]
    story += bullets([
        "Czy zachować osobne etykiety Generator i ExternalGrid, czy wprowadzić wspólną etykietę Source.",
        "Czy wyniki obliczeń pandapower przechowywać jako właściwości, osobne węzły pomiarowe lub poza grafem pierwszej wersji.",
        "Czy relacje mają zawierać metadane pochodzenia, pewność ekstrakcji i fragment tekstu źródłowego.",
        "Czy różne warianty grafu przechowywać w jednej bazie z network_id, czy w osobnych bazach Neo4j.",
    ])

    story += [PageBreak(), h1("Potencjalny widok aplikacji")]
    story += [p("Interfejs pierwszej wersji może składać się z jednego ekranu roboczego. Użytkownik wprowadza opis, wybiera model i uruchamia generowanie. System pokazuje wynik walidacji, graf oraz właściwości wybranego elementu. Dodatkowe funkcje mogą obejmować eksport JSON, porównanie z grafem referencyjnym i listę wykrytych błędów.")]
    story += [figure(ASSETS / "makieta_aplikacji.png", 170, "Rysunek 3  Robocza makieta głównego widoku aplikacji")]
    story += [styled_table(["Obszar widoku", "Zakres funkcji"], [
        ["Panel wejściowy", "Opis tekstowy, wybór modelu, parametry promptu i uruchomienie procesu."],
        ["Podgląd grafu", "Węzły, relacje, filtrowanie typów i zaznaczanie elementów."],
        ["Panel szczegółów", "Właściwości wybranego węzła lub relacji oraz status walidacji."],
        ["Wynik procesu", "Lista ostrzeżeń, błędów, czas odpowiedzi i możliwość eksportu."],
    ], [43 * mm, 129 * mm])]

    story += [PageBreak(), h1("Plan ewaluacji")]
    story += [p("Ewaluacja powinna oddzielać poprawność struktury od poprawności właściwości. Sam fakt utworzenia prawidłowego JSON nie oznacza, że graf wiernie odtwarza opis. Dla każdego testu należy zachować tekst wejściowy, oczekiwany graf, odpowiedź modelu, wynik walidacji i listę różnic.")]
    story += [styled_table(["Poziom", "Metryka", "Interpretacja"], [
        ["Węzły", "precision, recall, F1", "Czy model wykrywa właściwe elementy i nie dodaje nieistniejących."],
        ["Relacje", "precision, recall, F1", "Czy połączenia, kierunki i typy relacji są poprawne."],
        ["Właściwości", "exact match lub błąd liczbowy", "Czy wartości i jednostki odpowiadają opisowi."],
        ["Walidacja", "odsetek poprawnych odpowiedzi", "Jak często wynik przechodzi schemat bez naprawy."],
        ["Stabilność", "zgodność między powtórzeniami", "Jak bardzo wynik zależy od losowości modelu."],
        ["Efektywność", "czas, tokeny, koszt", "Jaki jest koszt uzyskania pojedynczego grafu."],
    ], [28 * mm, 54 * mm, 90 * mm])]
    story += [h2("Proponowane warianty eksperymentów")]
    story += bullets([
        "Opis prosty, w którym każde zdanie przedstawia jeden obiekt albo relację.",
        "Opis z parametrami technicznymi, jednostkami i kilkoma obiektami w jednym zdaniu.",
        "Opis niepełny lub niejednoznaczny, wymagający zgłoszenia braków zamiast zgadywania.",
        "Porównanie zero shot, few shot oraz structured outputs.",
        "Porównanie co najmniej jednego modelu lokalnego i jednego modelu przez API.",
        "Powtórzenie testów dla kilku ustawień temperatury i losowych uruchomień.",
    ])
    story += [h2("Kategorie błędów")]
    story += [styled_table(["Kod", "Kategoria", "Przykład"], [
        ["E1", "Pominięcie obiektu", "Brak transformatora opisanego w tekście"],
        ["E2", "Obiekt nadmiarowy", "Generator niewystępujący w opisie"],
        ["E3", "Błędny typ", "Linia rozpoznana jako transformator"],
        ["E4", "Błędna relacja", "Nieprawidłowa szyna początkowa"],
        ["E5", "Błędna właściwość", "Niepoprawna długość lub moc"],
        ["E6", "Błąd jednostki", "MW zinterpretowane jako kW"],
        ["E7", "Błąd formatu", "Odpowiedź niezgodna z JSON Schema"],
    ], [15 * mm, 55 * mm, 102 * mm], center_cols=(0,))]

    story += [PageBreak(), h1("Plan dalszych prac")]
    story += [styled_table(["Etap", "Zakres", "Rezultat"], [
        ["1 Analiza danych", "Pełny wydruk kolumn case14, wybór pól i przypięcie wersji pandapower", "Specyfikacja mapowania"],
        ["2 Model Neo4j", "Etykiety, relacje, source_id, constraints i reguły walidacji", "Zatwierdzony schemat"],
        ["3 Graf referencyjny", "Konwerter DataFrame do Neo4j oraz testy integralności", "Referencyjna sieć case14"],
        ["4 Integracja LLM", "Adapter modeli, prompt, JSON Schema i modele Pydantic", "Pierwsza ekstrakcja z tekstu"],
        ["5 Aplikacja", "API, ekran roboczy, wizualizacja i eksport", "Prototyp demonstracyjny"],
        ["6 Ewaluacja", "Zbiór opisów, porównanie modeli i analiza błędów", "Wyniki do rozdziału badawczego"],
        ["7 Rozszerzenie", "Dodatkowe sieci, dane autentyczne lub fine tuning", "Opcjonalny zakres końcowy"],
    ], [34 * mm, 91 * mm, 47 * mm])]
    story += [h2("Najbliższe zadania")]
    story += bullets([
        "Zapisać pełne listy kolumn dla tabel case14 i określić minimalne właściwości każdego typu.",
        "Zatwierdzić reprezentowanie linii i transformatorów jako osobnych węzłów.",
        "Przygotować klasy Pydantic wspólne dla importu referencyjnego i wyniku LLM.",
        "Uruchomić Neo4j lokalnie i utworzyć constraints.",
        "Zaimplementować import szyn, a następnie kolejnych elementów wraz z relacjami.",
        "Przygotować pierwszy opis tekstowy odtwarzający wybrany fragment case14.",
    ])

    story += [PageBreak(), h1("Pytania do promotora")]
    story += [p("Spotkanie powinno doprowadzić przede wszystkim do zatwierdzenia zakresu pierwszej wersji. Poniższe pytania porządkują decyzje, które wpływają na implementację i późniejszą ewaluację.")]
    questions = [
        "Czy przedstawiony zakres prototypu jest wystarczający dla pracy inżynierskiej?",
        "Czy linie i transformatory powinny pozostać osobnymi węzłami grafu?",
        "Które parametry techniczne muszą znaleźć się w minimalnym schemacie pierwszej wersji?",
        "Czy case14 wystarczy do demonstracji, jeśli ewaluacja obejmie dodatkowe sieci testowe?",
        "Czy prototyp ma wykonywać obliczenia rozpływu mocy, czy skupić się na ekstrakcji, grafie i analizie topologii?",
        "Ile modeli oraz strategii promptowania należy porównać, aby część eksperymentalna była wystarczająca?",
        "Czy wymagane są autentyczne dane infrastrukturalne, czy wystarczą sieci testowe i opisy generowane na ich podstawie?",
    ]
    for i, q in enumerate(questions, 1):
        story += [Paragraph(f"<b>{i}.</b> {escape(q)}", ParagraphStyle(f"Q{i}", parent=BODY, leftIndent=7 * mm, firstLineIndent=-7 * mm, spaceAfter=4 * mm))]
    story += [h2("Proponowany wynik spotkania")]
    story += bullets([
        "Zatwierdzony zakres prototypu i rola sieci case14.",
        "Zatwierdzony wstępny schemat Neo4j oraz lista elementów do pierwszego importu.",
        "Ustalona liczba modeli, wariantów promptowania i sieci testowych w ewaluacji.",
        "Decyzja, czy obliczenia elektroenergetyczne należą do zakresu implementacji.",
    ])

    story += [PageBreak(), h1("Podsumowanie")]
    story += [p("Koncepcja systemu jest już określona na poziomie przepływu danych i podziału odpowiedzialności. Najważniejszym elementem pierwszej implementacji będzie wspólny model domenowy używany zarówno przez konwerter pandapower, jak i ścieżkę LLM. Pozwoli on porównywać wyniki bez dodatkowych transformacji oraz precyzyjnie klasyfikować błędy.")]
    story += [p("Rozpoczęcie od case14 ogranicza złożoność i zapewnia znany punkt odniesienia. Po zbudowaniu grafu referencyjnego kolejne prace mogą koncentrować się na jakości ekstrakcji, niezawodności walidacji i porównaniu modeli. Dodatkowe sieci i dane rzeczywiste powinny zostać włączone dopiero po ustabilizowaniu schematu oraz procesu ewaluacji.")]
    story += [h1("Źródła")]
    refs = [
        "Dokumentacja pandapower, Power System Test Cases, case14, https://pandapower.readthedocs.io/en/v3.5.6/networks/power_system_test_cases.html",
        "Repozytorium pandapower, https://github.com/e2nIEE/pandapower",
        "Neo4j, Graph database concepts, https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/",
        "Neo4j Cypher Manual, Create constraints, https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/",
        "Materiały robocze i wyniki analizy pandapower case14 przekazane w ramach przygotowania pracy.",
    ]
    for i, ref in enumerate(refs, 1):
        story += [Paragraph(f"{i}. {escape(ref)}", ParagraphStyle(f"Ref{i}", parent=SMALL, leftIndent=7 * mm, firstLineIndent=-7 * mm, spaceAfter=2 * mm))]

    doc.build(story)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
