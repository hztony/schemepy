#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2010-11-02
@author: shell.xu
'''
from __future__ import with_statement
import objects

class Function(object):

    def __init__(self, name, envs, params, objs):
        self.name, self.envs = name, envs.clone()
        self.params, self.objs, self.evaled = params, objs, True

    def __call__(self, envs, objs):
        with self.envs:
            # print self.name, objs
            pn, pv = self.params, objs
            while pn is not objects.nil and pv is not objects.nil:
                if pn.car.name == '.':
                    self.envs.add(pn.cdr.car.name, pv)
                    break
                self.envs.add(pn.car.name, pv.car)
                pn, pv = pn.cdr, pv.cdr
            r = self.envs.evals(self.objs)
            # print self.name + ' end', r
            return r

@objects.default_env.decorater('define', False)
def define(envs, objs):
    if isinstance(objs[0], objects.OPair):
        func = Function(objs.car.car.name, envs, objs.car.cdr, objs.cdr)
        envs.add(objs[0].car.name, func)
    elif isinstance(objs[0], objects.OSymbol):
        envs.add(objs[0].name, envs.eval(objs[1]))
    else: raise Exception('define format error')

@objects.default_env.decorater('lambda', False)
def sym_lambda(envs, objs):
    return Function('<lambda>', envs, objs.car, objs.cdr)

@objects.default_env.decorater('begin', False)
def begin(envs, objs):
    with envs: return envs.evals(objs)

@objects.default_env.decorater('display', True)
@objects.default_env.decorater('error', True)
def display(envs, objs): print ' '.join(map(str, list(objs)))

@objects.default_env.decorater('symbol?', True)
def is_symbol(envs, objs): return isinstance(objs.car, objects.OSymbol)

@objects.default_env.decorater('eq?', True)
def is_eq(envs, objs):
    if isinstance(objs[0], objects.OSymbol) and \
            isinstance(objs[1], objects.OSymbol):
        return objs[0].name == objs[1].name
    else: return objs[0] is objs[1]

@objects.default_env.decorater('let', False)
def let(envs, objs):
    with envs:
        for p in objs.car:
            assert(isinstance(p.car, objects.OSymbol))
            envs.add(p.car.name, envs.evals(p.cdr))
        return envs.evals(objs.cdr)

# list functions
@objects.default_env.decorater('list', True)
def list_list(envs, objs): return objs

@objects.default_env.decorater('null?', True)
def list_null(envs, objs): return objs.car is objects.nil

@objects.default_env.decorater('pair?', True)
def list_pair(envs, objs): return isinstance(objs.car, objects.OPair)

@objects.default_env.decorater('cons', True)
def list_cons(envs, objs): return objects.OPair(objs[0], objs[1])

@objects.default_env.decorater('car', True)
def list_car(envs, objs): return objs.car.car

@objects.default_env.decorater('cdr', True)
def list_cdr(envs, objs): return objs.car.cdr

@objects.default_env.decorater('caar', True)
def list_caar(envs, objs): return objs.car.car.car

@objects.default_env.decorater('cadr', True)
def list_cadr(envs, objs): return objs.car.cdr.car

@objects.default_env.decorater('cdar', True)
def list_cdar(envs, objs): return objs.car.car.cdr

@objects.default_env.decorater('caddr', True)
def list_caddr(envs, objs): return objs.car.cdr.cdr.car

@objects.default_env.decorater('append', True)
def list_append(envs, objs):
    r = []
    for obj in objs: r.extend(obj)
    return objects.to_list(r)

@objects.default_env.decorater('map', True)
def list_map(envs, objs):
    l, r = objs.cdr, []
    while l[0] is not objects.nil:
        t = map(lambda i: i.car, l)
        r.append(objs.car(envs, objects.to_list(t)))
        l = map(lambda i: i.cdr, l)
    return objects.to_list(r)

@objects.default_env.decorater('filter', True)
def list_filter(envs, objs):
    return filter(lambda o: objs.car(envs, objects.OPair(o, objects.nil)),
                  objs[1])

# logic functions
@objects.default_env.decorater('not', True)
def logic_not(envs, objs): return not objs[0]

@objects.default_env.decorater('and', True)
def logic_and(envs, objs): return reduce(lambda x, y: x and y, objs)

@objects.default_env.decorater('or', True)
def logic_or(envs, objs): return reduce(lambda x, y: x or y, objs)

@objects.default_env.decorater('cond', False)
def logic_cond(envs, objs):
    elsecase = None
    for o in objs:
        assert(isinstance(o, objects.OPair)), '%s format error' % o
        if isinstance(o.car, objects.OSymbol) and o.car.name == 'else':
            elsecase = o.cdr
        elif envs.eval(o.car): return envs.evals(o.cdr)
    if elsecase: return envs.evals(elsecase)

@objects.default_env.decorater('if', False)
def logic_if(envs, objs):
    if envs.eval(objs[0]): return envs.eval(objs[1])
    elif objs.cdr.cdr is not objects.nil: return envs.eval(objs[2])

# number functions
@objects.default_env.decorater('number?', True)
def num_number(envs, objs): return isinstance(objs.car, (int, long, float))

@objects.default_env.decorater('+', True)
def num_add(envs, objs): return sum(objs)

@objects.default_env.decorater('-', True)
def num_dec(envs, objs):
    s = objs.car
    for o in objs.cdr: s -= o
    return s

@objects.default_env.decorater('*', True)
def num_mul(envs, objs): return reduce(lambda x, y: x*y, objs)

@objects.default_env.decorater('/', True)
def num_div(envs, objs):
    s = objs.car
    for o in objs.cdr: s /= o
    return s

@objects.default_env.decorater('=', True)
def num_eq(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] == objs[1]

@objects.default_env.decorater('<', True)
def num_lt(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] < objs[1]

@objects.default_env.decorater('>', True)
def num_gt(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] > objs[1]

@objects.default_env.decorater('>=', True)
def num_nlt(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] >= objs[1]

@objects.default_env.decorater('<=', True)
def num_ngt(envs, objs):
    return isinstance(objs[0], (int, long, float)) and \
        isinstance(objs[1], (int, long, float)) and objs[0] <= objs[1]

@objects.default_env.decorater('remainder', True)
def num_remainder(envs, objs):
    return objs[0] % objs[1]
