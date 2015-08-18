# -*- coding: utf-8 -*-
#! /usr/bin/env python
import json

with open("E:\projectall\project\confcrawl\confcrawl\config\example.conf","r")as f:
        config = f.read()
conf = json.loads(config)
print conf.get("start_urls",[])