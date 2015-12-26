"""
A series of rules to match against
"""


class SaveRule(object):
    pass


class RuleChain(object):

    def __init__(self):
        self._rule_queue = []
        self._rule_pointer = 0

        # Stack that represents the dom.  As we pop the
        # stack we will decriment the select pointer as
        # we leave elements we previously selected
        self._select_dec_stack = []

        self.results = []

    def _intermediate_result(self, tag):
        if len(self._rule_queue) == self._rule_pointer + 1:
            self.results.append(tag)
            self._rule_pointer += 1
            self._select_dec_stack.append(1)
        elif isinstance(self._rule_queue[self._rule_pointer + 1], SaveRule):
            self.results.append(tag)
            self._rule_pointer += 2
            self._select_dec_stack.append(2)
        else:
            self._rule_pointer += 1
            self._select_dec_stack.append(1)

    def add(self, rule):
        """
        Add a new rule to this RuleChain
        """
        self._rule_queue.append(rule)

    def current_rule(self):
        """
        Gets the current rule we are trying to match,
        based on the rule pointer.
        """
        if self._rule_pointer == len(self._rule_queue):
            return None
        return self._rule_queue[self._rule_pointer]

    def pop(self):
        """
        Move us back down the rule queue as we exit
        tags in the dom.  _select_dec_stack effectively
        tracks our dom location.
        """
        self._rule_pointer -= self._select_dec_stack.pop()
