import argparse
import time
import json
import sys
import os


class UserEntryRegulator:
    PTH = os.path.dirname(os.path.abspath(__file__)).split('hiroko')[0] + 'hiroko/'
    CONFIG_FILE = 'config/hiroko.json'
    DEF_RULES = set([
        'day-count',
        'last-system-snapshot-date',
        'max-deviation',
        'max-distance',
        'min-deviation',
        'min-distance',
        'output-population-size',
        'method',
    ])
    ENTRY_RULE_EXPANSION = {
        'd': 'day-count',
        's': 'output-population-size',
        'm': 'method',
    }

    def __init__(self):
        self.regulations = None

        # Create parsing tree
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', help='Days to distribute the revisions.', type=int)
        parser.add_argument('-s', help='Enter size of output for each generation.', type=int)
        parser.add_argument('-m', help='Method of convergence <random> or <genetic>.', type=str)

        # Load rules from command line
        pri_rule_book = self.loadPriorityRules(parser.parse_args())

        # Load rules from static file
        def_rule_book = self.loadStaticRules()

        # Create rule book
        self._rule_book = {**def_rule_book, **pri_rule_book}

        # Check the sanity of the rules created
        self.checkRuleSanity()

    def loadStaticRules(self):
        with open(UserEntryRegulator.PTH + UserEntryRegulator.CONFIG_FILE, 'rb') as jfile:
            static_regulations = json.loads(jfile.read().decode('utf-8'))
            return static_regulations

    def loadPriorityRules(self, parse_namespace):
        rules = {}
        if parse_namespace.d:
            rules[UserEntryRegulator.ENTRY_RULE_EXPANSION['d']] = parse_namespace.d
        if parse_namespace.s:
            rules[UserEntryRegulator.ENTRY_RULE_EXPANSION['s']] = parse_namespace.s
        if parse_namespace.m:
            rules[UserEntryRegulator.ENTRY_RULE_EXPANSION['m']] = parse_namespace.m
        return rules

    def checkRuleSanity(self):
        # Check rule amount
        if len(set(self._rule_book.keys()) - UserEntryRegulator.DEF_RULES) != 0:
            print('>> Invalid rules')
            sys.exit(1)

        days = self._rule_book[UserEntryRegulator.ENTRY_RULE_EXPANSION['d']]
        try:
            days = int(days)
            if days < 10 or days > 20:
                raise Exception
        except Exception:
            print('>> Day number must be an integer between 10 and 20, inclusive.')
            sys.exit(1)

        method = self._rule_book[UserEntryRegulator.ENTRY_RULE_EXPANSION['m']]
        if method != 'genetic' and method != 'random':
            print('>> Method can only be genetic or random')
            sys.exit(1)

        print('>> Rules are correct!')

    def isRuleBookUpdated(self):
        real_time = int(os.path.getmtime(UserEntryRegulator.PTH + UserEntryRegulator.CONFIG_FILE))
        stored_time = self._rule_book['last-system-snapshot-date']

        if real_time != stored_time:
            print('>> Snapshot times do not match')
            return False
        else:
            print('>> Config files are in sync!')
            return True

    def updateRuleBook(self, new_rule_book):
        self._rule_book = new_rule_book
        self._rule_book['last-system-snapshot-date'] = int(time.time())
        with open(UserEntryRegulator.PTH + UserEntryRegulator.CONFIG_FILE, 'wb') as jfile:
            jfile.write(json.dumps(self._rule_book, sort_keys=True, indent=4).encode('utf8'))

        print(
            '>> Updated Rule Book, new snapshot ->', self._rule_book['last-system-snapshot-date'])

    def fetchRuleBook(self):
        return self._rule_book
