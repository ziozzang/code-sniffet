#!/usr/bin/python
# -*- coding:utf-8 -*-
# JSON 파싱. keep ordered.
import json
import collections

a = json.load(open("hadoop.json","r"),  object_pairs_hook=collections.OrderedDict)
for i in a["Resources"].items():
  print "Name: %s" % i[0]
  print " >>  Type: %s" % i[1]["Type"]
