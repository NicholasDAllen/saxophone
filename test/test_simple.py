import unittest

import saxophone
from saxophone.rules import NameRule, AttrRule


class SimpleTest(unittest.TestCase):

    def test_get_tags(self):

        # Setup
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <div>
                        <table>
                            <tr id="a">
                                <th></th>
                            </tr>
                            <tr id="b">
                                <td></td>
                            </tr>
                            <tr id="c">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                    </div>"""

        # Run test
        parser = saxophone.Parser(xml)
        results = parser.name("tr").parse()
        self.assertEqual(len(results), 3)
        for r in results:
            self.assertEqual(r["name"], "tr")

    def test_get_attrs(self):

        # Setup
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <div>
                        <table>
                            <tr id="a">
                                <th></th>
                            </tr>
                            <tr id="b" >
                                <td id="test" cell="best"></td>
                            </tr>
                            <tr id="c">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                        <div id="foo" cell="best"></div>
                    </div>"""

        # Run test
        parser = saxophone.Parser(xml)
        results = parser.name("tr").attr("cell", "best").parse()
        self.assertEqual(len(results), 1)
        for tr in results:
            self.assertEqual(tr["attrs"]['id'], 'test')

    def test_save(self):

        # Setup
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <div>
                        <table>
                            <tr id="a">
                                <th></th>
                            </tr>
                            <tr id="b" >
                                <td id="test" cell="best"></td>
                            </tr>
                            <tr id="c">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                        <div id="foo" cell="best"></div>
                    </div>"""

        # Run test
        parser = saxophone.Parser(xml)
        results = parser.name("tr").save().attr("cell", "best").parse()
        self.assertEqual(len(results), 4)
        for r in results:
            if r["name"] == "td":
                self.assertEqual(r['attrs']['id'], 'test')
            else:
                self.assertEqual(r["name"], "tr")

    def test_hasattr(self):
        # Setup
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <div>
                        <table>
                            <tr id="a">
                                <th>foo</th>
                            </tr>
                            <tr id="b" >
                                <td id="test" cell="best"></td>
                            </tr>
                            <tr id="c">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                        <div id="foo" cell="best"></div>
                    </div>"""

        # Run test
        parser = saxophone.Parser(xml)
        results = parser.hasattr("cell").parse()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["attrs"]["id"], "test")
        self.assertEqual(results[1]["attrs"]["id"], 'foo')

    def test_content(self):
        # Setup
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <div>
                        <table>
                            <tr id="a">
                                <th>foo</th>
                            </tr>
                            <tr id="b" >
                                <td id="test" cell="best"></td>
                            </tr>
                            <tr id="c">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                        <div id="foo" cell="best"></div>
                    </div>"""

        # Run test
        parser = saxophone.Parser(xml)
        results = parser.id("a").name("th").parse()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], 'foo')

    def test_regex_attr(self):
        # Setup
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <div>
                        <table>
                            <tr test_1='1'>
                                <th>foo</th>
                            </tr>
                            <tr test_2='2'>
                                <td id="test" cell="best"></td>
                            </tr>
                            <tr id="c" test_3="a">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                        <div id="foo" cell="best"></div>
                    </div>"""

        # Run test
        parser = saxophone.Parser(xml)
        results = parser.regex_attr(r"test_\d", r"\d").parse()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["attrs"]["test_1"], '1')
        self.assertEqual(results[1]["attrs"]["test_2"], '2')

    def test_and(self):
        # Setup
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <div>
                        <table>
                            <tr test_1='1'>
                                <th>foo</th>
                            </tr>
                            <tr test_2='2'>
                                <td id="test" cell="best"></td>
                            </tr>
                            <tr id="c" test_3="a">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                        <div id="foo" cell="best"></div>
                    </div>"""

        # Run test
        parser = saxophone.Parser(xml)
        results = parser.combine(NameRule("div"), AttrRule("cell", "best")).parse()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "div")
        self.assertEqual(results[0]['attrs']["cell"], "best")

if __name__ == "__main__":
    unittest.main()
