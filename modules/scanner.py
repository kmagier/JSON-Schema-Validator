import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])


class Scanner:

    def __init__(self, input):
        self.tokens = []
        self.current_token_number = 0
        for token in self.tokenize(input):
            self.tokens.append(token)

    def tokenize(self, input_string):
        keywords = {'"$id"', '"$schema"', '"title"', '"properties"',
                    '"description"', '"required"', '"minimum"', '"maximum"',
                    '"minLength"', '"maxLength"', '"enum"', '"definitions"', '"$ref"'}
        token_specification = [
            ('NEWLINE', r'\n'),
            ('WS', r'[ \t]+'),
            ('STRING', r'"(?:\\.|[^"\\])*?"'),
            ('OCB', r'\{'),
            ('CCB', r'\}'),
            ('OSB', r'\['),
            ('CSB', r'\]'),
            ('NUMBER', r'\d+(\.\d*)?'),
            ('COLON', r':'),
            ('COMMA', r',')
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_number = 1
        current_position = line_start = 0
        match = get_token(input_string)
        while match is not None:
            type = match.lastgroup
            value = match.group(type)
            if type == 'NEWLINE':
                line_start = current_position
                line_number += 1 
            yield Token(type, value, line_number, match.start() - line_start)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError('Error: Unexpected character %r on line %d' % \
                               (input_string[current_position], line_number))
        yield Token('EOF', '', line_number, current_position - line_start)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number - 1 < len(self.tokens):
            return self.tokens[self.current_token_number - 1]
        else:
            raise RuntimeError('Error: No more tokens')
