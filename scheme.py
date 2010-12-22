#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import sys
import parser
import objects
import symbol

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    code_tree = parser.split_code_tree(f.read().decode('utf-8'))
    f.close()
    obj_tree = objects.to_scheme(code_tree)
    run_objs = objects.OPair(objects.OSymbol('begin'), obj_tree)
    try: print objects.default_env.eval(run_objs)
    except Exception, err: print err
