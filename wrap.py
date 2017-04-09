#!/usr/bin/env python
# coding=utf-8

def log(fn):
    def wrap(*args,**kwargs):
        ret = fn()
        return print("\033[1;31;40m %s \033[0m" % ret)
    return wrap

@log
def boy():
    return "i am a boy"

boy()
