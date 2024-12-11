from CFG.ContextFreeGrammar import ContextFreGrammar as Cfg, RecursiveDescentParser

if __name__ == "__main__":
    grammar1 = Cfg('grammar')
    """
    print(grammar1)
    print("Nonterminals:", grammar1.get_nonterminals())
    print("Terminals:", grammar1.get_terminals())
    print("Productions for A:", grammar1.get_productions_for('A'))
    print("Is valid CFG?", grammar1.is_valid_cfg())
    print('\n')
    grammar = Cfg('g1')
    print(grammar)
    print("Nonterminals:", grammar.get_nonterminals())
    print("Terminals:", grammar.get_terminals())
    print("Productions for A:", grammar.get_productions_for('A'))
    print("Is valid CFG?", grammar.is_valid_cfg())
    """

    input_sequence = ["a", "c", "b"]

    # Initialize and run the parser
    parser = RecursiveDescentParser(grammar1, input_sequence)
    result = parser.parse()

    # Output the result
    print(f"Result: {result}")