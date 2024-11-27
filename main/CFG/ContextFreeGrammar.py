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
        return [line.strip()
                for line in lines
                if line is not None and len(line.strip()) != 0]

    def __init__(self, filename: str):
        self.nonterminals: set[str] = set()
        self.terminals: set[str] = set()
        self.start_symbol: str = ""
        self.productions: dict = {}

        with open(filename, 'r') as file:
            lines: [str] = ContextFreGrammar.filter_lines(file.readlines())

        new_section: int or None = None
        section: int or None = None
        for line in lines:
            line = line.strip()

            if line.startswith("#"):
                section = new_section
                new_section = ContextFreGrammar.str_to_section(line.strip("#"))
            if not new_section and section:
                match section:
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
