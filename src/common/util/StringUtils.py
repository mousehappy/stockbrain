# -*- coding: UTF-8 -*-
import random, string


def genRandomString(slen=8):
    return ''.join(random.sample(string.ascii_letters, slen))
