# -*- coding: utf-8 -*-
#! /usr/bin/env python
from HTMLParser import HTMLParser
import re
def strip_tags(string, allowed_tags=''):
    if allowed_tags != '':
    # Get a list of all allowed tag names.
        allowed_tags_list = re.sub(r'[\/<> ]+', '', allowed_tags).split(',')
        allowed_pattern = ''
        for s in allowed_tags_list:
            if s == '':
                continue;
      # Add all possible patterns for this tag to the regex.
            if allowed_pattern != '':
                allowed_pattern += '|'
                allowed_pattern += '<' + s + ' [^><]*>$|<' + s + '>|'
    # Get all tags included in the string.
        all_tags = re.findall(r'<]+>', string, re.I)
        for tag in all_tags:
      # If not allowed, replace it.
            if not re.match(allowed_pattern, tag, re.I):
                string = string.replace(tag, '')
    else:
    # If no allowed tags, remove all.
        string = re.sub(r'<[^>]*?>', '', string)
    return string
def strip_tags1(htmlStr):
        '''
        使用HTMLParser进行html标签过滤
        :param htmlStr:
        '''

        htmlStr = htmlStr.strip()
        htmlStr = htmlStr.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(htmlStr)
        parser.close()
        return  ''.join(result)
