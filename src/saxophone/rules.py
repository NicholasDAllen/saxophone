
import re


class AttrRule(object):
    """
    Match by exact tag attribute
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def match(self, tag):
        return tag["attrs"].get(self.key) == self.value


class RegexAttrRule(object):

    def __init__(self, key, value):
        self.key = re.compile(key)
        self.value = re.compile(value)

    def match(self, tag):
        for key, value in tag['attrs'].iteritems():
            if self.key.match(key) and self.value.match(value):
                return True
        return False


class NameRule(object):
    """
    Match by tag name
    """

    def __init__(self, name):
        self.name = name

    def match(self, tag):
        return tag["name"] == self.name


class HasAttrRule(object):
    """
    Match if tag has attribute
    """
    def __init__(self, key):
        self.key = key

    def match(self, tag):
        return self.key in tag["attrs"]


class AndRule(object):
    """
    Match multiple rules on one element
    """
    def __init__(self, *rules):
        self.rules = rules

    def match(self, tag):
        return all((r.match(tag) for r in self.rules))
