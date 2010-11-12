#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys
import unittest
import parser
import objects
import symbol
import sym_list
import sym_logic
import sym_num

def run_scheme(filepath):
    f = open(filepath, 'r')
    code_tree = parser.split_code_tree(f.read().decode('utf-8'))
    f.close()
    obj_tree = objects.to_scheme(code_tree)
    run_objs = objects.OPair(objects.OSymbol('begin'), obj_tree)
    return objects.default_env.eval(run_objs)

class TestScheme(unittest.TestCase):

    def test_change_money(self):
        self.assertEqual(run_scheme('test/change-money.scm'), 9)

    def test_change_money_list(self):
        self.assertEqual(run_scheme('test/change-money-list.scm'), 9)

    def test_church(self):
        self.assertEqual(run_scheme('test/church.scm'), 2)

    def test_last_pair(self):
        self.assertEqual(run_scheme('test/last-pair.scm'), 5)

    def test_mobile(self):
        self.assertEqual(run_scheme('test/mobile.scm'), True)

    def test_reverse_tree(self):
        li = list(run_scheme('test/reverse-tree.scm'))
        self.assertEqual(list(li[0]), [4, 3])
        self.assertEqual(list(li[1]), [2, 1])

    def test_reverse(self):
        self.assertEqual(list(run_scheme('test/reverse.scm')), [5, 4, 3, 2, 1])

    def test_same_partiy(self):
        self.assertEqual(list(run_scheme('test/same-partiy.scm')), [3, 5, 7])

    def test_subset(self):
        subset = str(run_scheme('test/subset.scm'))
        self.assertEqual(subset,
                         '(() (3) (2) (2 3) (1) (1 3) (1 2) (1 2 3))')

if __name__ == '__main__': unittest.main()