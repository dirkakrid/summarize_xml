#!/usr/bin/env python2
import xml.etree.ElementTree as ET
import sys
import re


whitespace = re.compile('\s+')
cache = {}


def getRecord(element, key):
    if key in cache:
        record = cache[key]
    else:
        record = {
            'tag':      element.tag,
            'key':      key,
            'text':     [],
            'attrib':   [],
            'children': {}}
    return record


def compileAttributes(element, record):
    for key in element.attrib.keys():
        if key not in record['attrib']:
            record['attrib'].append(key)
    return record


def recurseChildren(element, record, path):
    for child in element:
        data = parse(child, path)
        tag = data['tag']
        if tag not in record['children']:
            record['children'][tag] = data

    return record


def textlen(text):
    if isinstance(text, (str, unicode)):
        text = whitespace.sub('', text)
        return len(text)
    else:
        return 0


def hasText(element, record):
    if textlen(element.text) > 0:
        record['text'].append('has_text')
    if textlen(element.tail) > 0:
        record['text'].append('has_tail')
    record['text'] = list(set(record['text']))

    return record


def parse(element, path=[]):
    path = path + [element.tag]  # important, do not append, do not +=
    key = "+".join(path[-2:])

    record = getRecord(element, key)
    record = compileAttributes(element, record)
    record = recurseChildren(element, record, path)
    record = hasText(element, record)

    cache[key] = record

    return record


def dump(element, depth=0, history=[]):

    history = history + [element['key']]  # important, do not append, do not +=

    if len(element['text']) > 0:
        text = " [" + ", ".join(element['text']) + "]"
    else:
        text = ""

    if len(element['attrib']) > 0:
        attrib = " (" + ", ".join(element['attrib']) + ")"
    else:
        attrib = ""

    print "%s%s%s%s" % ("    "*depth, element['tag'], attrib, text)

    for child in element['children'].values():
        if child['key'] not in history:  # NO CIRCULAR REFERENCES
            dump(child, depth+1, history)


def usage():
    print "Usage:  %s <filename>\n" % sys.argv[0]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        tree = ET.parse(sys.argv[1])
        dump(parse(tree.getroot()))
    else:
        usage()
