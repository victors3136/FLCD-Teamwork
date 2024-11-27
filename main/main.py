from CFG.ContextFreeGrammar import ContextFreGrammar as Cfg

if __name__ == "__main__":
    grammar = Cfg('grammar')
    print(grammar)
    print("Nonterminals:", grammar.get_nonterminals())
    print("Terminals:", grammar.get_terminals())
    print("Productions for A:", grammar.get_productions_for('A'))
    print("Is valid CFG?", grammar.is_valid_cfg())


    grammar = Cfg('g1')
    print(grammar)
    print("Nonterminals:", grammar.get_nonterminals())
    print("Terminals:", grammar.get_terminals())
    print("Productions for A:", grammar.get_productions_for('A'))
    print("Is valid CFG?", grammar.is_valid_cfg())