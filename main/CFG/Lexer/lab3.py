import re


class SymbolTable:
    def __init__(self, size):
        self.table_size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, name):
        return hash(name) % self.table_size

    def insert(self, name):
        hash_code = self.hash_function(name)
        bucket = self.table[hash_code]

        for item in bucket:
            if item[0] == name:
                return item[1]

        unique_code = f"{hash_code}.{len(bucket) + 1}"
        bucket.append((name, unique_code))
        return unique_code

    def display(self):
        with open("ST.out", "w") as file:
            file.write("Symbol Table Contents:\n")
            for i, bucket in enumerate(self.table):
                if bucket:
                    file.write(f"Bucket {i}: {bucket}\n")
        print("Symbol table written to ST.out")


class Lexer:
    def __init__(self, token_file, table):
        self.tokens = Lexer.load_tokens(token_file)
        self.symbol_table = table
        self.pif = []

    @staticmethod
    def load_tokens(token_file):
        tokens = {}
        with open(token_file, "r") as file:
            for index, line in enumerate(file.readlines()):
                token = line.strip()
                tokens[token] = index
        return tokens

    def tokenize(self, source_file):
        with open(source_file, "r") as file:
            source_code = file.readlines()

        line_number = 0
        for line in source_code:
            line_number += 1
            index = 0
            while index < len(line):
                if line[index].isspace():
                    index += 1
                    continue

                token, index = Lexer.extract_token(line, index)
                if token in self.tokens:
                    self.pif.append((token, self.tokens[token], -1))
                elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token):
                    code = self.symbol_table.insert(token)
                    self.pif.append((token, self.tokens["IDENTIFIER"], code))
                elif re.match(r'^\d+$', token):
                    code = self.symbol_table.insert(token)
                    self.pif.append((token, self.tokens["CONSTANT"], code))
                else:
                    print(f"Lexical error at line {line_number}, token '{token}'")
                    return

        print("Lexically correct")
        self.save_pif()

    @staticmethod
    def extract_token(line, index):
        operators = {'+', '-', '*', '/', '%', '=', '==', '<', '>', '->', '+=', '<=', '>='}
        token = ""
        if line[index].isalnum() or line[index] == '_':
            while index < len(line) and (line[index].isalnum() or line[index] == '_'):
                token += line[index]
                index += 1
        elif line[index] in '+-*/%<=>':
            while index < len(line) and token + line[index] in operators:
                token += line[index]
                index += 1
        elif line[index] in '()[];,':
            token = line[index]
            index += 1
        else:
            token = line[index]
            index += 1
        return token, index

    def save_pif(self):
        with open("PIF.out", "w") as file:
            file.write("Program Internal Form (PIF):\n")
            for entry in self.pif:
                file.write(f"{entry}\n")
        print("Program internal form written to PIF.out")


if __name__ == "__main__":
    symbol_table = SymbolTable(10)
    lexer = Lexer("token.in", symbol_table)

    lexer.tokenize("p2.txt")
    symbol_table.display()
