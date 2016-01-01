from copy import copy
import re
import six
from xml.sax.handler import ContentHandler
from xml import sax

import saxophone.rules
from saxophone.rulechain import RuleChain, SaveRule


class Parser(ContentHandler):

    def __init__(self, document=None, fp=None):
        if document is None and fp is None:
            raise Exception("You must provide a document or file pointer")

        self._document = document
        self._fp = fp

        self._rule_chains = {}
        self._current_rule_chain = None

        self._tag_stack = []

    def new(self, name):
        chain = RuleChain()
        self._current_rule_chain = chain
        self._rule_chains[name] = chain
        return self

    def name(self, name):
        """
        Match by tag type (name)
        """
        self.current_rule_chain().add(saxophone.rules.NameRule(name))
        return self

    def attr(self, key, value):
        """
        Match by attribute value
        """
        self.current_rule_chain().add(saxophone.rules.AttrRule(key, value))
        return self

    def regex_attr(self, key, value):
        """
        Regular expression matcher for attributes.  Both
        the attribute name and value are regex matches.
        """
        self.current_rule_chain().add(
            saxophone.rules.RegexAttrRule(key, value))
        return self

    def hasattr(self, key):
        """
        Match by existence of attribute
        """
        self.current_rule_chain().add(saxophone.rules.HasAttrRule(key))
        return self

    def id(self, value):
        """
        Find tag by id
        """
        self.current_rule_chain().add(saxophone.rules.AttrRule("id", value))
        return self

    def combine(self, *rules):
        """
        This should probably be called and, but since 'and' is
        a keyword it tends to confuse syntax highlighters and
        such.
        """
        self.current_rule_chain().add(saxophone.rules.AndRule(*rules))
        return self

    def save(self):
        self.current_rule_chain().add(SaveRule())
        return self

    def parse(self):
        if self._document is not None:
            sax.parseString(self._document, self)
        else:
            sax.parseString(self._fp, self)
        if len(self._rule_chains) == 1:
            return self._current_rule_chain.results
        return {k: v.results for k, v in six.iteritems(self._rule_chains)}

    def current_rule_chain(self):
        if self._current_rule_chain is None:
            chain = RuleChain()
            self._current_rule_chain = chain
            self._rule_chains["First"] = chain
        return self._current_rule_chain

    def startElement(self, name, attrs):
        current_element = make_tag(name, attrs)
        self._tag_stack.append(current_element)
        for chain in self._rule_chains.values():
            chain.current_result = None
            current_rule = chain.current_rule()
            if current_rule is None:
                chain._select_dec_stack.append(0)
                continue
            if current_rule.match(current_element) is True:
                    chain._intermediate_result(current_element)
                    continue
            chain._select_dec_stack.append(0)

    def endElement(self, name):
        self._tag_stack.pop()
        for chain in self._rule_chains.values():
            chain.pop()

    def characters(self, content):
        c = re.sub("\s+$", "", re.sub("^\s+", "", content))
        self._tag_stack[-1]['content'] = c


def make_tag(name, attrs):
    return {
        "name": name,
        "attrs": dict(copy(attrs)),
        "content": None
    }
