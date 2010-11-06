#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
import objects
import evals

def list_list(symbols, objs):
    return objs
list_list.e = True
evals.default_env.add('list', list_list)

def list_null(symbols, objs):
    return objs.car is None
list_null.e = True
evals.default_env.add('null?', list_null)

def list_pair(symbols, objs):
    return isinstance(objs.car, objects.OPair)
list_pair.e = True
evals.default_env.add('pair?', list_pair)

def list_cons(symbols, objs):
    return objects.OPair(objs[0], objs[1])
list_cons.e = True
evals.default_env.add('cons', list_cons)

def list_car(symbols, objs):
    return objs.car.car
list_car.e = True
evals.default_env.add('car', list_car)

def list_cdr(symbols, objs):
    return objs.car.cdr
list_cdr.e = True
evals.default_env.add('cdr', list_cdr)

def list_caar(symbols, objs):
    return objs.car.car.car
list_caar.e = True
evals.default_env.add('caar', list_caar)

def list_cadr(symbols, objs):
    return objs.car.cdr.car
list_cadr.e = True
evals.default_env.add('cadr', list_cadr)

def list_cdar(symbols, objs):
    return objs.car.car.cdr
list_cdar.e = True
evals.default_env.add('cdar', list_cdar)

def list_caddr(symbols, objs):
    return objs.car.cdr.cdr.car
list_caddr.e = True
evals.default_env.add('caddr', list_caddr)

def list_append(symbols, objs):
    r = []
    for obj in objs:
        if obj is None: continue
        for o in obj: r.append(o)
    return objects.make_list(r)
list_append.e = True
evals.default_env.add('append', list_append)

def list_map(symbols, objs):
    l, r = objects.load_list(objs.cdr), []
    while l[0]:
        t = map(lambda i: i.car, l)
        r.append(objs.car(symbols, objects.make_list(t)))
        l = map(lambda i: i.cdr, l)
    return objects.make_list(r)
list_map.e = True
evals.default_env.add('map', list_map)

def list_filter(symbols, objs):
    if objs[1] is None: return None
    r = []
    for o in objs[1]:
        if objs.car(symbols, objects.make_list([o,])): r.append(o)
    return objects.make_list(r)
list_filter.e = True
evals.default_env.add('filter', list_filter)
