class ContextFreGrammar:
    NONTERMINALS: int = 0
    TERMINALS: int = 1
    PRODUCTIONS: int = 2
    START_SYMBOL: int = 3

    @staticmethod
    def str_to_section(string: str) -> int or None:
        match string.strip():
            case 'Non-terminals':
                return ContextFreGrammar.NONTERMINALS
            case 'Terminals':
                return ContextFreGrammar.TERMINALS
            case 'Productions':
                return ContextFreGrammar.PRODUCTIONS
            case 'Start symbol':
                return ContextFreGrammar.START_SYMBOL
            case _:
                return None

    @staticmethod
    def filter_lines(lines: list[str]) -> list[str]:
        return [line.strip()
                for line in lines
                if line and len(line.strip()) != 0]

    def __init__(self, filename: str):
        self.nonterminals: set[str] = set()
        self.terminals: set[str] = set()
        self.start_symbol: str = ""
        self.productions: dict[str, list[list[str]]] = {}

        with open(filename, 'r') as file:
            lines: [str] = ContextFreGrammar.filter_lines(file.readlines())

        section: int or None = None
        for line in lines:
            line = line.strip()

            if line.startswith("#"):
                section = ContextFreGrammar.str_to_section(line.strip("#").strip())
                continue

            if section is not None:
                match section:
                    case ContextFreGrammar.NONTERMINALS:
                        self.nonterminals.add(line)
                    case ContextFreGrammar.TERMINALS:
                        self.terminals.add(line.strip('"'))
                    case ContextFreGrammar.PRODUCTIONS:
                        lhs, rhs = line.split("->")
                        lhs = lhs.strip()
                        rhs = [item.strip() for item in rhs.strip().split()]
                        if rhs == ['eps']:
                            rhs = []
                        if lhs in self.productions:
                            self.productions[lhs].extend([rhs])
                        else:
                            self.productions[lhs] = [rhs]
                    case ContextFreGrammar.START_SYMBOL:
                        self.start_symbol = line.strip()

    def __str__(self):
        return (f"Non-Terminals: {self.nonterminals}\n"
                f"Terminals: {self.terminals}\n"
                f"Start Symbol: {self.start_symbol}\n"
                f"Productions:\n" +
                "\n".join(f"{nonterminal} -> {' | '.join(' '.join(blabla) for blabla in self.productions[nonterminal])}"
                          for nonterminal in self.productions))

    def get_nonterminals(self) -> set[str]:
        return self.nonterminals

    def get_terminals(self) -> set[str]:
        return self.terminals

    def get_productions(self) -> dict[str, list[list[str]]]:
        return self.productions

    def get_productions_for(self, nonterminal):
        return self.productions.get(nonterminal, [])

    def is_valid_cfg(self):
        return all(lhs in self.nonterminals for lhs in self.productions)


class ParseException(Exception):
    pass

class RecursiveDescentParser:
    NORMAL: str = "normal"
    BACKTRACK: str = "backtrack"
    ERROR: str = "error"
    FINAL: str = "final"

    def error(self) -> None:
        self.state = self.ERROR

    def all_good(self) -> None:
        self.state = self.NORMAL

    def insuccess(self) -> None:
        self.state = self.BACKTRACK

    def end(self) -> None:
        self.state = self.FINAL

    def current_input(self) -> str:
        if len(self.input_stack) <= self.index:
            raise ParseException(
                f"Could not retrieve current input for current index {self.index} and input stack of length {len(self.input_stack)}")
        return self.input_stack[self.index]

    def __init__(self, grammar: ContextFreGrammar, input_sequence) -> None:
        self.grammar: ContextFreGrammar = grammar
        self.input_sequence = input_sequence
        self.state: str = RecursiveDescentParser.NORMAL
        self.index: int = 0
        self.working_stack: list[str] = []
        self.input_stack = [grammar.start_symbol]
        self.parse_table: list[str] = []
        self.current_nonterminal_prod_id: dict[str, int] = {}

    def __str__(self) -> str:
        return f"State: {self.state}, Index: {self.index}, Input Stack: {self.input_stack}, Working Stack: {self.working_stack}"

    def expand(self) -> None:
        """
        Perform the Expand action:
        - If the head of the input stack is a nonterminal, expand it using its first production.
        - Update the working stack and input stack accordingly.
        """
        if not self.input_stack:
            raise ParseException("You should not call 'expand' when the input stack is empty!")

        current: str = self.input_stack.pop(0)
        if current not in self.grammar.get_nonterminals():
            raise ParseException(
                f"You should not call 'expand' when the top is a terminal!\nHead was {current}")

        # first time encountering this non-terminal?
        #  => make sure to remember it!
        if current not in self.current_nonterminal_prod_id:
            self.current_nonterminal_prod_id[current] = 0

        production_index: int = self.current_nonterminal_prod_id[current]
        productions: list[list[str]] = self.grammar.get_productions_for(current)

        # non-terminal with no productions?! -> I guess this is also an error produced by wrong code :)
        if not productions:
            raise ParseException(
                f"You created a non-terminal with no productions\nThe terminal is {current}")

        current_production = productions[production_index]
        self.working_stack.append(f"{current}{production_index + 1}")
        self.input_stack = current_production + self.input_stack

        self.current_nonterminal_prod_id[current] = production_index + \
                                                    (1 if production_index + 1 < len(productions) else 0)

    def advance(self) -> None:
        """
        Perform the Advance action:
        - Match the terminal at the head of the input stack with the current input symbol.
        - Update the working stack, input stack, and current index.
        """
        if not self.input_stack:
            raise ParseException("You should not call 'expand' when the input stack is empty!")

        head = self.input_stack.pop(0)
        if self.index >= len(self.input_sequence) or head != self.input_sequence[self.index]:
            self.error()
            return

        self.working_stack.append(head)
        self.index += 1

    def momentary_insuccess(self) -> None:
        """
        Perform the Momentary Insuccess action:
        - If the terminal at the head of the input stack does not match the current input symbol,
        transition to the backtrack state.
        """
        if not self.input_stack:
            raise ParseException("You should not call 'momentary_insuccess' when the input stack is empty!")

        current = self.input_stack[0]

        if self.index < len(self.input_sequence) and current != self.input_sequence[self.index]:
            self.insuccess()

    def back(self):
        """
        Perform the Back action:
        - If the head of the working stack is a terminal, move it back to the input stack
          and step back in the input sequence.
        """
        # we can't go back
        # so there are no more opportunities to explore
        if not self.working_stack or self.index <= 0:
            self.error()
            return

        current = self.working_stack.pop()

        # TODO not sure if this check needed here
        if current not in self.grammar.get_terminals():
            raise ParseException("You should not backtrack on a non-terminal")

        self.input_stack.insert(0, current)
        self.index -= 1

    def another_try(self) -> None:
        """
        Perform the 'Another Try' action:
        - If the head of the working stack is a nonterminal and another production exists for it,
          switch to the next production.
        - Otherwise, backtrack by removing the nonterminal from the working stack and restoring it
          to the input stack.
        - If no more productions exist and the nonterminal is the start symbol with index 1,
          raise a parse error.
        """
        if not self.working_stack:
            raise ParseException("Cannot perform 'another_try' because the working stack is empty.")

        head = self.working_stack.pop()

        # Check if the head represents a non-terminal or terminal
        if head[-1].isdigit():  # This assumes that non-terminals do not end with digits
            nonterminal = head[:-1]  # Extract the non-terminal part
        else:
            raise ParseException("You should not call 'another_try' on a terminal.")

        production_index = self.current_nonterminal_prod_id[nonterminal]
        productions = self.grammar.get_productions_for(nonterminal)

        if not productions:
            raise ParseException(f"No productions exist for nonterminal {nonterminal}.")

        if production_index + 1 >= len(productions):
            self.input_stack.insert(0, nonterminal)
            if self.index == 0 and nonterminal == self.grammar.start_symbol:
                raise ParseException("Parsing failed: no more options for the start symbol.")
            self.insuccess()
            return

        next_production_index = production_index + 1
        next_production = productions[next_production_index]

        self.working_stack.append(f"{nonterminal}{next_production_index + 1}")
        current_production = productions[production_index]

        # Delete current production from the input stack
        for _ in current_production:
            self.input_stack.pop(0)

        self.input_stack = next_production + self.input_stack
        self.all_good()

    def success(self) -> None:
        """
        Perform the Success action:
        - If the input stack is empty, and we've reached the end of the input sequence,
          transition to the final state.
        - Otherwise, it's an error, because we haven't successfully parsed the input.
        """
        if self.index != len(self.input_sequence) or self.input_stack:
            raise ParseException(
                "Parsing unsuccessful: either input stack is not empty or input sequence is incomplete.")
        self.end()

    def parse(self):
        while self.state not in {self.ERROR, self.FINAL}:
            print(self.__str__())

            if self.state == self.NORMAL:
                if self.index == len(self.input_sequence) and not self.input_stack:
                    self.success()
                elif self.input_stack[0] in self.grammar.get_nonterminals():
                    self.expand()
                elif self.input_stack[0] in self.grammar.get_terminals():
                    if self.input_stack[0] == self.input_sequence[self.index]:
                        self.advance()
                    else:
                        self.momentary_insuccess()
                else:
                    self.error()

            elif self.state == self.BACKTRACK:
                if self.working_stack and self.working_stack[-1] in self.grammar.get_terminals():
                    self.back()
                else:
                    self.another_try()

        if self.state == self.FINAL:
            return "Sequence accepted"
        else:
            return "Error: Parsing failed"


