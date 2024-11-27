class ContextFreeGrammar:
    def __init__(self, filename: str):
        self.nonterminals = set()
        self.terminals = set()
        self.start_symbol = ""
        self.productions = {}

        # Read and parse the file
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith("Nonterminals:"):
                    self.nonterminals = set(line.split(":")[1].strip().split())
                elif line.startswith("Terminals:"):
                    self.terminals = set(line.split(":")[1].strip().split())
                elif line.startswith("Start:"):
                    self.start_symbol = line.split(":")[1].strip()
                elif line.startswith("Productions:"):
                    break

            # Parse productions after the 'Productions:' line
            for line in file:
                if '->' in line:
                    lhs, rhs = line.strip().split("->")
                    lhs = lhs.strip()
                    rhs = [prod.strip() for prod in rhs.split("|")]
                    self.productions[lhs] = rhs

    def __str__(self):
        return (f"Nonterminals: {self.nonterminals}\n"
                f"Terminals: {self.terminals}\n"
                f"Start Symbol: {self.start_symbol}\n"
                f"Productions:\n" +
                "\n".join(f"{nt} -> {' | '.join(self.productions[nt])}" for nt in self.productions))

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


if __name__ == "__main__":
    cfg = ContextFreeGrammar('empty_file.txt')
    print(cfg)
    print("Nonterminals:", cfg.get_nonterminals())
    print("Terminals:", cfg.get_terminals())
    print("Productions for S:", cfg.get_productions_for('S'))
    print("Is valid CFG?", cfg.is_valid_cfg())
