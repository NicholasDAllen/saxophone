Saxaphone
-------

What is saxophone?
===================

Saxaphone is a fast xml parser built on sax, but with an easy to use query interface (think minidom or jquery).

What it isn't
==============

Saxaphone isn't recommended as your general-purpose XML parser.  It's good for quickly extracting small bits of data from a large xml document.

Basic Usage
======

Saxaphone has selectors much like jQuery.  To select all of the table tags in a document you can do the following:

    from saxophone import Parser

    with open(path) as fp:
        table = Parser(document).name("table").parse()

Or select by attribute:

    parser.attr("id", "my-table").parse()

Since id is a special attribute, it has it's own rule.  Also, elements can be grabbed contextually. To get all the rows in a table:

    parser.id("my-table").name("tr").parse()

To save the table element as well, use 'save':

    parser.id("my-table").save().name('tr').parse()


Multiple Rule Chains
===================

A parser can have multiple rules

    parser.new("table").id("my-table")
    parser.new("rows").id("my-table").name("tr")
    results = parser.parse()

    print results["table"]
    > [{"name": "table"...
    print results["rows"]
    > [{"name": "tr"...

Rule Types
================

- parser.name - Match by tag name
- parser.id(id) - Match by id
- parser.attr(key, value) - Match by attribute & attribute value
- parser.hasattr(key) - Match tags that have an attribute
- parser.regex_attr - Match attribute and value by regular expression
- parser.combine - Combine multiple rules
