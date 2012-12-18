#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-12-18
@author: shell.xu
'''
from objects import *

all = ['Stack',]

class PrognStatus(object):
    def __init__(self, objs): self.objs, self.rslt = objs, None
    def __repr__(self): return 'progn ' + str(self.objs)

    def __call__(self, stack, envs, objs):
        if self.objs.cdr == nil: return stack.jump(self.objs.car, envs)
        t, self.objs = self.objs.car, self.objs.cdr
        return stack.call(t, envs)

class CallStatus(object):
    def __init__(self, objs): self.objs = objs
    def __repr__(self): return 'call ' + str(self.objs)

    def __call__(self, stack, envs, objs):
        if objs is None: return stack.call(self.objs[0], envs)
        if not objs.evaled:
            return stack.jump(ParamStatus(objs, self.objs.cdr, nil), envs)
        return stack.jump(ParamStatus(objs, nil,
                                      reversed_list(self.objs.cdr)), envs)

# TODO: this should be call status
class ParamStatus(object):
    def __init__(self, func, params, objs):
        self.func, self.params, self.objs = func, params, objs
    def __repr__(self):
        return 'call %s with (%s) <- (%s)' % (
            self.func, self.params, self.objs)

    def __call__(self, stack, envs, objs):
        if objs is not None: self.params = OCons(objs, self.params)
        if self.objs is nil: return stack.jump(self.func, envs, self.params)
        t, self.objs = self.objs.car, self.objs.cdr
        return stack.call(t, envs)

class Envs(object):
    def __init__(self, e=None):
        self.e, self.fast = e, {}
        self.genfast()
    # FIXME: getstate/setstate, otherwise save/load will not work
    def __getstate__(self): return self.e
    def __setstate__(self, state): self.e, self.fast = state, {}
    def __repr__(self): return objects.format_list(self.e)
    def genfast(self):
            for i in reversed_list(self.e): self.fast.update(i)
    def fork(self, r=None):
        if r is None: r = {}
        return Envs(OCons(r, self.e))
    def add(self, name, value):
        self.fast[name] = value
        self.e.car[name] = value
    def __getitem__(self, name): return self.fast[name]

class Stack(list):
    @classmethod
    def init(cls, code, builtin):
        stack = cls()
        stack.append((PrognStatus(code), Envs(to_list([{}, builtin,]))))
        return stack

    def save(self, r, f):
        self[0][1].e[1].clear()
        __import__('cPickle').dump((self, r), f, 2)
    @classmethod
    def load(cls, f, builtin):
        stack, r = __import__('cPickle').load(f)
        stack[0][1].e[1].update(builtin)
        for s in stack: s[1].genfast()
        return stack, r

    def func_call(self, func, envs):
        o = func[0]
        if not isinstance(o, OSymbol): return CallStatus(func)
        objs = envs[o.name]
        if not objs.evaled: return ParamStatus(objs, func.cdr, nil)
        return ParamStatus(objs, nil, reversed_list(func.cdr))

    def call(self, func, envs, args=None):
        if isinstance(func, OSymbol): return (envs[func.name],)
        if isinstance(func, OQuota): return (func.objs,)
        if isinstance(func, OCons):
            self.append((self.func_call(func, envs), envs))
        elif not callable(func): return (func,)
        else: self.append((func, envs))
        return (args,)

    def jump(self, func, envs, args=None):
        if isinstance(func, OSymbol): return (envs[func.name], self.pop(-1))
        if isinstance(func, OQuota): return (func.objs, self.pop(-1))
        if isinstance(func, OCons):
            self[-1] = (self.func_call(func, envs), envs)
        elif not callable(func): return (func, self.pop(-1))
        else: self[-1] = (func, envs)
        return (args,)

    def trampoline(self, r=None, debug=None, coredump=None):
        try:
            while self:
                if debug is not None: debug(self, r)
                o = self[-1]
                r = o[0](self, o[1], r)
                if isinstance(r, tuple): r = r[0]
                else: self.pop(-1)
            return r
        except Exception, err:
            if coredump:
                if isinstance(coredump, basestring):
                    with open(coredump, 'wb') as cd: self.save(r, cd)
                else: self.save(r, coredump)
            raise
