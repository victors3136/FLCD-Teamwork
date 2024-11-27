from CFG.ContextFreeGrammar import ContextFreGrammar as Cfg

if __name__ == "__main__":
    grammar = Cfg('grammar.txt')
    print(grammar)
    print("Nonterminals:", grammar.get_nonterminals())
    print("Terminals:", grammar.get_terminals())
    print("Productions for S:", grammar.get_productions_for('S'))
    print("Is valid CFG?", grammar.is_valid_cfg())