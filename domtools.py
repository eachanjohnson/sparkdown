#!/usr/bin/env python

__author__ = 'Eachan Johnson'

__doc__ = '''
SparkdownParser
by Eachan Johnson, 2015

A Sparkdown-to-Web parser. Also a python module.

Usage:  sdparse --help
        sdparse --version
        sdparse [-v|-q] --input <file> --output <prefix>

Options:
    -h, --help                          Show this page and exit
    --version                           Show version number and exit
    -v, --verbose                       Be chatty
    -q, --quiet                         Be silent
    -i <file>, --input <file>           The Sparkdown file to parse
    -o <prefix>, --output <prefix>      Prefix to the output files
'''

## Define global variables
#readahead = 6  # how many characters to read from the stack at a time

## Define classes
class Element(object):

    def __init__(self, tag, text='', parent):
        self.tag = tag
        self.kind = self.get_kind()
        self.id = []
        self.classes = []
        self.terminator = get_terminator()
        self.text = text
        self.children = []
        self.parent = parent

    def get_kind(self):
        inline_set = {'br', 'span', 'strong', 'em', 'hr'}
        if self.tag in inline_set:
            return 'inline'
        else:
            return 'block'

    def get_terminator(self):
        import string
        d = {
            'h1': '\n',
            'h2': '\n',
            'strong': ' ,.;:' + string.letters,
            'em': ' ,.;:' + string.letters,
            'hr': '\n'
        }
        try:
            return d[self.tag]
        except KeyError:
            return ''

    def append(self, element):
        if type(Element) == Element:
            self.children.append(element)
            return element
        else:
            raise TypeError


class DOM(Element):

    def __init__(self, text=''):
        Element.__init__(self, tag='h1', text=text, parent=None)


class H1(Element):

    def __init__(self, text, parent):
        Element.__init__(self, tag='h1', text=text, parent=parent)


class H2(Element):

    def __init__(self, text, parent):
        Element.__init__(self, tag='h2', text=text, parent=parent)


class Strong(Element):

    def __init__(self, text, parent):
        Element.__init__(self, tag='strong', text=text, parent=parent)


class Em(Element):

    def __init__(self, text, parent):
        Element.__init__(self, tag='em', text=text, parent=parent)


class Hr(Element):

    def __init__(self, text):
        Element.__init__(self, tag='hr', text=text)

class Text(Element):

    def __init__(self, text):
        Element.__init__(self, tag='', text=text)

    def append(self, element):
        raise TypeError




## Define functions

def main():

    return None

## Boilerplate
if __name__ == '__main__':
    main()
else:
    pass