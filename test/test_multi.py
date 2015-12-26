import unittest

import saxophone


class MultiTest(unittest.TestCase):

    def test_multiple_rules(self):

        # Setup
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <div>
                        <table id="first">
                            <tr id="a">
                                <th>Foo</th>
                            </tr>
                            <tr id="b">
                                <td></td>
                            </tr>
                            <tr id="c">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                        <table id="second">
                            <tr id="a">
                                <th></th>
                            </tr>
                            <tr id="b">
                                <td>Bar</td>
                            </tr>
                            <tr id="c">
                                <td></td>
                                <td></td>
                            </tr>
                        </table>
                    </div>"""

        # Run test
        parser = saxophone.Parser(xml)
        parser.id("first").id("a").name("th")
        parser.new("Second").id("second").id("b").name("td")
        results = parser.parse()
        self.assertEqual(results["First"][0]["name"], "th")

if __name__ == "__main__":
    unittest.main()
