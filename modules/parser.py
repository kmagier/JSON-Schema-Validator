allowed_tokens = ['NEWLINE', 'WS', 'STRING', 'NUMBER', 'OCB', 'CCB', 'OSB', 'CSB', 'COLON', 'COMMA']

class Parser:

    ##### Parser header #####
    def __init__(self, scanner):
        self.next_token = scanner.next_token
        self.token = None

    def take_token(self, token_type):
        self.token = self.next_token()
        while self.token.type in ('NEWLINE', 'WS'):
            self.token = self.next_token()
        if type(token_type) is tuple:
            if self.token.type not in token_type:
                self.error(token_type)
        else:
            if self.token.type != token_type:
                self.error(token_type)

    ##### Parser body #####
    def start(self):
        self.take_token('OCB')
        self.parse_dictionary()
        self.take_token('EOF')

    def parse_dictionary(self):
        start_line, start_column = self.token.line, self.token.column
        expected_dict_group = ('STRING', 'NUMBER', 'CCB')
        self.take_token(expected_dict_group)
        while self.token.type != 'CCB':
            self.parse_dictionary_key()
            self.take_token(('COMMA', 'CCB'))
            if self.token.type == 'COMMA':
                self.take_token(expected_dict_group)

        end_line, end_column = self.token.line, self.token.column
        print(f"DICT[OK]: FROM: ({start_line:2d},{start_column:2d}) TO: ({end_line:2d},{end_column:2d}) (line, column) ")
        
    def parse_dictionary_key(self):
        self.take_token('COLON')
        self.parse_dictionary_value()

    def parse_dictionary_value(self):
        expected_dict_value_groups = ('STRING', 'NUMBER', 'OCB', 'OSB')
        self.take_token(expected_dict_value_groups)
        if self.token.type == 'OCB':
             self.parse_dictionary()
        elif self.token.type == 'OSB':
             self.parse_list()
            
    def parse_list(self):
        start_line, start_column = self.token.line, self.token.column
        expected_list_groups = ('STRING', 'NUMBER', 'OCB', 'CSB')
        self.take_token(expected_list_groups)
        while self.token.type != 'CSB':
            if self.token.type == 'OCB':
                self.parse_dictionary()
            elif self.token.type == 'OSB':
                self.parse_list()

            self.take_token(('COMMA', 'CSB'))
            if self.token.type == 'COMMA':
                self.take_token(expected_list_groups)

        end_line, end_column = self.token.line, self.token.column
        print(f"LIST[OK]: FROM: ({start_line:2d},{start_column:2d}) TO: ({end_line:2d},{end_column:2d}) (line, column)")


    def error(self, token_type):
        type, value, line, column = self.token
        expected_type = ' or '.join(token_type) if isinstance(token_type, tuple) else token_type
        raise RuntimeError(
            f'Invalid token: "{value}" at {(line, column)}. '
            f'Expected: {expected_type} but got {type}.'
        )