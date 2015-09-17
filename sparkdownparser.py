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

import domtools

## Define global variables
#readahead = 6  # how many characters to read from the stack at a time

## Define classes
class Buffer(object):

    def __init__(self, filename, size=1000):
        '''
        Yields a character at a time from a file in a memory-efficient way.
        :return: Buffer object
        '''
        self.filename = filename
        self.memory_size = size
        self.file = open(filename, 'rU')
        self.memory = '\n'
        self.eof = False
        self.fill_memory()

    def reset(self):
        self.__init__(self.filename, self.memory_size)
        return None

    def fill_memory(self):
        counter = 0
        new_line = self.file.readline()
        while counter < self.memory_size and new_line != '':
            #print counter, new_line
            self.memory += new_line
            counter += 1
            new_line = self.file.readline()
        if counter < self.memory_size:
            self.eof = True
            return '\e\o\f'
        else:
            self.memory += '\n'
            return 'full'

    def get_char(self):
        try:
            char = self.memory[0]
        except IndexError:
            if not self.eof:
                self.fill_memory()
                self.get_char()
            else:
                raise EOFError
        else:
            self.memory = self.memory[1:]
            #print 'supplied ', char
            #print char
            return char


class Stack(object):

    def __init__(self, size=6):
        '''
        The stack of characters which are used to interpret Sparkdown.
        :param size: The maximum size of the stack.
        :return: A Stack object
        '''
        self.size = size
        self.stack = []
        self.new = True

    def get_current_char(self):
        if len(self.stack) < self.size and self.new:
            return ''
        else:
            self.new = False
            try:
                return self.stack[0]
            except IndexError:
                return '\n'

    def push(self, char):
        #print char
        if len(self.stack) < self.size + 1:
            self.stack.append(char)
            return self.stack
        else:
            self.stack = self.stack[1:]
            self.stack.append(char)
            return self.stack

    def get_stack_string(self):
        return ''.join(self.stack)


class Rulebook(object):

    def __init__(self):
        '''
        Set of rules for Sparkdown.
        :return: A Rulebook object.
        '''
        self.tokens = {
            '#': {
                    ' ': {
                        1: domtools.H1,
                        2: domtools.H2,
                        3: domtools.H3,
                        4: domtools.H4,
                        5: domtools.H5
                    }
            },
            '-': {
                '\n': {
                    3: domtools.Hr
                }
            },
            '*': {
                '\n': {
                    3: domtools.Hr
                },
                ' ': {
                    n: domtools.Strong for n in xrange(1, 3)
                },
                'alpha': {
                    n: domtools.Strong for n in xrange(1, 3)
                }
            },
            '_': {
                ' ': {
                    n: domtools.Em for n in xrange(1, 3)
                },
                'alpha': {
                    n: domtools.Em for n in xrange(1, 3)
                }
            },
            '\n': {
                'alpha': {
                    n: domtools.P for n in xrange(2, 1000)
                }
            }
        }


class Grammar(object):

    def __init__(self):
        '''
        Interpreter of stack contents, maintains short-range context.
        :return: A grammar object.
        '''
        self.current_token = ''
        self.current_token_count = 0
        self.listening = False
        self.rulebook = Rulebook()

    def lookup(self, stack):
        '''
        Translates stack contents.
        :param stack: A Sparkdown Stack object.
        :return: '' if waiting for token to complete, else the translated token
        '''
        current_char = stack.get_current_char()
        #print self.listening, self.current_token_count, current_char
        return_string = ['']
        if current_char in self.rulebook.tokens:
            if not self.listening:
                self.current_token = current_char
                self.listening = True
                self.current_token_count = 1
            elif current_char == self.current_token:
                self.current_token_count += 1
                if self.current_token_count > stack.size:
                    return_string[0] = self.current_token_count * self.current_token
                    self.current_token = ''
                    self.current_token_count = 0
                    self.listening = False
            else:
                self.current_token = current_char
                self.listening = True
                self.current_token_count = 1
        elif self.listening:
            try:
                terminator_tree = self.rulebook.tokens[self.current_token]
            except KeyError:
                print '{} not in rulebook'.format(self.current_token)
            else:
                try:
                    import string
                    if current_char in string.letters + '.,;:"\'':
                        current_char2 = 'alpha'
                    else:
                        current_char2 = current_char
                        current_char = ''
                    number_tree = terminator_tree[current_char2]
                except KeyError:
                    print '{} not a terminator for {}'.format(current_char, self.current_token)
                    return_string[0] = current_char
                    self.current_token = ''
                    self.current_token_count = 0
                    self.listening = False
                else:
                    try:
                        return_string = [number_tree[self.current_token_count], current_char,
                                         self.current_token, self.current_token_count]
                    except KeyError:
                        print '{} x {} not a rule'.format(self.current_token_count, current_char)
                        return_string = self.current_token_count * self.current_token + current_char
                        self.current_token = ''
                        self.current_token_count = 0
                        self.listening = False
                    else:
                        self.current_token = ''
                        self.current_token_count = 0
                        self.listening = False
        else:
            return_string[0] = current_char
        #print self.listening, self.current_token_count, '"{}"'.format(current_char), return_string
        return tuple(return_string)


class Parser(object):

    def __init__(self, buffer, dom, grammar, lookahead=6):
        '''
        An abstraction of a PEG parser reading from a Sparkdown Buffer object.
        :param buffer: a Sparkdown Buffer object
        :return: a Parser object
        '''
        self.buffer = buffer
        self.lookahead = lookahead
        #self.filename = filename
        #self.file = open(self.filename, 'w')
        self.dom = dom
        self.string_out = ''
        self.stack = Stack(size=self.lookahead)
        self.grammar = grammar
        self.current_element = self.dom

    def parse(self):
        while True:
            try:
                new_char = self.buffer.get_char()
            except EOFError:
                #print 'eof'
                while len(self.stack.stack) > 0:
                    self.stack.stack.pop(0)
                    out_element = self.grammar.lookup(self.stack)
                    try:
                        element, char = out_element
                    except ValueError:
                        #print out_element[0]
                        self.current_element.append(out_element[0])
                    else:
                        self.current_element = self.current_element.append(
                            element(text=char, parent=self.current_element)
                        )
                        print self.current_element.tag
                break
            else:
                self.stack.push(char=new_char)
                out_element = self.grammar.lookup(self.stack)
                #print self.stack.get_stack_string()
                #print out_element, self.current_element
                try:
                    #print out_element
                    element, char, token, tokenx = out_element
                except ValueError:
                    #print out_element[0]
                    self.current_element = self.current_element.append(out_element[0])
                else:
                    el = element(text=char, parent=self.current_element, token=token, tokenx=tokenx)
                    #print 'Trying to append ', el.tag, isinstance(el, domtools.Element)
                    self.current_element = self.current_element.append(el)
                    print self.current_element.tag


## Define functions

def main():
    import docopt

    args = docopt.docopt(doc=__doc__, version='Sparkdown Parser version 1e-100')
    #print args

    buffer = Buffer(filename=args['--input'])
    dom = domtools.DOM()
    parser = Parser(buffer=buffer, dom=dom, grammar=Grammar(), lookahead=7)

    parser.parse()

    print parser.dom

    return None

## Boilerplate
if __name__ == '__main__':
    main()
else:
    pass