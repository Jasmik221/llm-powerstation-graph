import unittest

from energy_graph import parse_description


class ParserTests(unittest.TestCase):
    def test_example_creates_expected_graph(self):
        graph = parse_description(
            "Szyna B1 ma napięcie 110 kV. "
            "Szyna B2 ma napięcie 110 kV. "
            "Szyna B1 jest połączona linią L1 z szyną B2 o długości 10 km. "
            "Do szyny B2 podłączono odbiór O1 o mocy 20 MW."
        ).as_property_graph()
        self.assertEqual(len(graph["nodes"]), 4)
        self.assertEqual(len(graph["relationships"]), 3)
        self.assertIn({"type": "TO_BUS", "from": "L1", "to": "B2"}, graph["relationships"])

    def test_rejects_unknown_bus(self):
        with self.assertRaisesRegex(ValueError, "niezdefiniowaną szynę"):
            parse_description(
                "Szyna B1 ma napięcie 110 kV. "
                "Szyna B1 jest połączona linią L1 z szyną B2."
            )

    def test_rejects_unrecognized_sentence(self):
        with self.assertRaisesRegex(ValueError, "Nie rozpoznano zdania"):
            parse_description("Linia łączy stacje na północy.")


if __name__ == "__main__":
    unittest.main()
