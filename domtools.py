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

    def __init__(self, tag, parent, text='', token='', tokenx=0):
        self.tag = tag
        self.open_tag = '<{}>'.format(self.tag)
        self.close_tag = '</{}>'.format(self.tag)
        self.token = token
        self.tokenx = tokenx
        self.kind = self.get_kind()
        self.id = []
        self.classes = []
        self.terminator, self.parent_to_skip = self.get_terminator()
        self.children = [text]
        self.parent = parent
        self.skip = 0
        #print self.__dict__

    def get_kind(self):
        inline_set = {'br', 'span', 'strong', 'em', 'hr'}
        if self.tag in inline_set:
            return 'inline'
        else:
            return 'block'

    def get_terminator(self):
        d = {
            'h1': ('\n', 0),
            'h2': ('\n', 0),
            'h3': ('\n', 0),
            'h4': ('\n', 0),
            'h5': ('\n', 0),
            'strong': (self.token, self.tokenx),
            'em': (self.token, self.tokenx),
            'hr': ('\n', 0),
            'p': ('\n', 0)
        }
        try:
            return d[self.tag]
        except KeyError:
            return ('eof', 0)

    def append(self, element):
        #print element
        if isinstance(element, Element):
            if element.token != self.terminator:
                if self.skip == 0:
                    print 'Appending', element.tag
                    self.children.append(element)
                    return self.children[-1]
                else:
                    return self
            else:
                print 'Terminating', self.tag, 'because of "', element, '" which matches', self.terminator
                print 'Moving up to', self.parent.tag
                self.parent.skip = self.parent_to_skip
                return self.parent.append(element)
        elif type(element) == str:
            if element == self.terminator:
                print 'Terminating', self.tag, 'because of "', element, '" which matches', self.terminator
                print 'Moving up to', self.parent.tag
                self.parent.skip = self.parent_to_skip
                return self.parent.append(element)
            else:
                #print 'Appending', self.children[-1]
                if self.skip == 0:
                    try:
                        self.children[-1] += element
                    except Exception:
                        self.children.append(element)
                else:
                    self.skip -= 1
                return self
        else:
            return self

    def __str__(self):
        out = '{}{}{}'.format(self.open_tag, ''.join([str(child) for child in self.children]), self.close_tag)
        return out


class DOM(Element):

    def __init__(self, text=''):
        Element.__init__(self, tag='dom', text=text, parent=None)
        self.close_tag = ''
        self.open_tag = ''


class H1(Element):

    def __init__(self, parent, text='', token='', tokenx=0):
        Element.__init__(self, tag='h1', text=text, parent=parent)
        print self.token


class H2(Element):

    def __init__(self, parent, token='', text='', tokenx=0):
        Element.__init__(self, tag='h2', text=text, parent=parent)

class H3(Element):

    def __init__(self, parent, token='', text='', tokenx=0):
        Element.__init__(self, tag='h3', text=text, parent=parent)

class H4(Element):

    def __init__(self, parent, token='', text='', tokenx=0):
        Element.__init__(self, tag='h4', text=text, parent=parent)

class H5(Element):

    def __init__(self, parent, token='', text='', tokenx=0):
        Element.__init__(self, tag='h5', text=text, parent=parent)


class Strong(Element):

    def __init__(self, parent, token, tokenx, text=''):
        Element.__init__(self, tag='strong', text=text, parent=parent, token=token, tokenx=tokenx)


class Em(Element):

    def __init__(self, parent, token, tokenx, text=''):
        Element.__init__(self, tag='em', text=text, parent=parent, token=token, tokenx=tokenx)


class Hr(Element):

    def __init__(self, parent, token='', text='', tokenx=0):
        Element.__init__(self, tag='hr', text=text, parent=parent)
        self.close_tag = ''


class Br(Element):

    def __init__(self, parent, token='', text='', tokenx=0):
        Element.__init__(self, tag='br', text=text, parent=parent)
        self.close_tag = ''


class P(Element):

    def __init__(self, parent, token='', text='', tokenx=0):
        Element.__init__(self, tag='p', text=text, parent=parent)



## Define functions

def main():

    return None

## Boilerplate
if __name__ == '__main__':
    main()
else:
    pass