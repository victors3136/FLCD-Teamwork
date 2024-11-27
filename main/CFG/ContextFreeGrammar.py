class ContextFreGrammar:
    NONTERMINALS: int = 0
    TERMINALS: int = 1
    PRODUCTIONS: int = 2
    START_SYMBOL: int = 3

    @staticmethod
    def str_to_section(string: str) -> str or None:
        match string:
            case 'Nonterminals':
                return ContextFreGrammar.NONTERMINALS
            case 'Terminals':
                return ContextFreGrammar.TERMINALS
            case 'Productions':
                return ContextFreGrammar.PRODUCTIONS
            case 'Start Symbol':
                return ContextFreGrammar.START_SYMBOL
            case _:
                return None

    @staticmethod
    def filter_lines(lines: [str]) -> [str]:
        return [line
                for line in lines
                if line is not None and len(line) != 0]

    def __init__(self, filename: str):
        self.nonterminals = set()
        self.terminals = set()
        self.start_symbol = ""
        self.productions = {}

        with open(filename, 'r') as file:
            lines = ContextFreGrammar.filter_lines(file.readlines())

        current_section = None
        prev_section = None
        for line in lines:
            line = line.strip()

            if line.startswith("#"):
                prev_section = current_section
                current_section = ContextFreGrammar.str_to_section(line.strip("#"))
            if not current_section and prev_section:
                match prev_section:
                    case ContextFreGrammar.NONTERMINALS:
                        pass
                    case ContextFreGrammar.TERMINALS:
                        pass
                    case ContextFreGrammar.PRODUCTIONS:
                        pass
                    case ContextFreGrammar.START_SYMBOL:
                        pass
                    case _:
                        pass
            else:
                # error
                pass

    def __str__(self):
        return (f"Non-Terminals: {self.nonterminals}\n"
                f"Terminals: {self.terminals}\n"
                f"Start Symbol: {self.start_symbol}\n"
                f"Productions:\n" +
                "\n".join(f"{prod} -> {' | '.join(self.productions[prod])}"
                          for prod in self.productions))

    def get_nonterminals(self):
        return self.nonterminals

    def get_terminals(self):
        return self.terminals

    def get_productions(self):
        return self.productions

    def get_productions_for(self, nonterminal):
        return self.productions.get(nonterminal, [])

    def is_valid_cfg(self):
        if not all(lhs in self.nonterminals for lhs in self.productions):
            return False

        for rhs_list in self.productions.values():
            for rhs in rhs_list:
                if not all(symbol in self.nonterminals.union(self.terminals) for symbol in rhs):
                    return False
        return True
