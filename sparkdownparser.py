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
special_chars = {'*', '_', '-', '#', '=', '`'}

## Define classes
class Tag(object):

    def __init__(self, sparkdown):
        self.sparkdown = sparkdown
        self.tag = self.get_tag()
        self.open = self.get_open()
        self.close = self.get_close()
        self.block = self.get_block()

    def get_tag(self):
        d = {
            '#': 'h1',
            '##': 'h2',
            '**': 'strong',
            '*': 'em',
            '---': 'hr',
            '===': 'hr',
            '-': 'li'
        }
        try:
            return d[self.sparkdown]
        except KeyError:
            if self.sparkdown in {'p', 'html', 'body', 'head'}:
                return self.sparkdown
            else:
                raise KeyError

    def get_open(self):
        if self.tag in {'hr', 'br'}:
            return '<' + self.tag + '/>'
        else:
            return '<' + self.tag + '>'

    def get_close(self):
        if self.tag in {'hr', 'br'}:
            return '<' + self.tag + '/>'
        else:
            return '</' + self.tag + '>'

    def get_block(self):
        if self.tag in {'code', 'ul', 'ol', 'quote', 'p'}:
            return True
        else:
            return False


class StreamHandler(object):

    def __init__(self):
        self.block = False
        self.list = False
        self.heading = False
        self.paragraph = False
        self.newline_counter = 0
        self.token = ''
        self.stream = []

    def add(self, item):
        try:
            self.block = item.block
        except AttributeError:
            if item == '\n':
                self.newline_counter += 1
                if self.paragraph:
                    self.newline_counter = 0
                    self.stream.append(Tag('p'))
                    self.stream.append(item)
        else:
            self.heading = item.tag
            if item.tag == 'li' and not self.list:
                self.list = True
                self.stream.append(Tag('ul'))
                self.stream.append(Tag('li'))
        return self.stream


class Converter(object):

    def __init__(self):
        self.HTML = ''
        self.handler = StreamHandler()

    def convert(self, string):
        stream = ['&*&html', '&*&body']
        token = ''
        heading = False
        paragraph = False
        list = False
        newline_count = 0
        for char in string:
            if char == '\n':
                newline_count += 1
                if heading:
                    stream += ['&*&' + heading]
                    heading = False
                elif paragraph:
                    stream += ['&*&p']
                    newline_count = 0
                else:
                    pass
            elif char in special_chars:
                token += char
            else:
                if newline_count > 2 and not heading:
                    paragraph = True
                    stream += ['&*&p']
                    newline_count = 0
                try:
                    tag = Tag(token)
                except KeyError:
                    tag = False
                token = ''
                if tag:
                    if tag[0] == 'h' and len(tag) == 2:
                        heading = tag
                        if char == ' ':
                            char = ''
                    stream += ['&*&' + tag.tag, char]
                else:
                    stream += [c for c in token + char]
        print ''.join(stream)
        tag_track = ['x']
        html = ''
        for item in stream + ['&*&body', '&*&html']:
            #print tag_track
            if '&*&' == item[:3] and item != tag_track[-1]:
                if item != '&*&hr' and item != '&*&br':
                    tag_track.append(item)
                html += '<' + item.split('&*&')[1] + '>'
            elif '&*&' == item[:3] and item == tag_track[-1]:
                tag_track.pop()
                html += '</' + item.split('&*&')[1] + '>'
            else:
                html += item
        print html


## Define functions
def main():
    import docopt

    args = docopt.docopt(doc=__doc__, version='Sparkdown Parser version 1e-100')

    with open(args['--input'], 'rU') as f:
        string = f.read()
        converter = Converter()
        html = converter.convert(string=string)

## Boilerplate
if __name__ == '__main__':
    main()
else:
    pass