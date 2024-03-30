#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import datetime


def re_time(path):
    with open(path, 'r', encoding='utf-8-sig') as data:
        records = data.readlines()
