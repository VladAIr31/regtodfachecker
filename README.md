#   Regex to DFA Converter

This Python script implements a process to convert regular expressions into equivalent Deterministic Finite Automata (DFA). The implementation follows a standard procedure involving several key stages:

##   Implementation Steps

1.  **Regular Expression to Postfix Conversion:**
    * The script begins by converting the input regular expression from infix notation (the conventional way we write expressions) to postfix notation (also known as Reverse Polish Notation or RPN). This conversion simplifies the subsequent processing of the expression.
    * The `infix_to_postfix(infix_expr)` function handles this conversion, taking into account operator precedence for regular expression operators such as concatenation (`.`), alternation (`|`), Kleene star (`*`), plus (`+`), and optional (`?`).
    * The `add_concat_operator(expr)` helper function explicitly inserts concatenation operators (`.`) to ensure correct evaluation order.

2.  **NFA Construction (Thompson's Construction):**
    * The next step involves building a Non-deterministic Finite Automaton (NFA) from the postfix representation of the regular expression. Thompson's construction algorithm is employed to achieve this. This algorithm provides a systematic way to build an NFA for any regular expression.
    * The `NFAFragment` class is used to represent components of the NFA during the construction process, containing a start state, an accept state, and a list of transitions.
    * Functions like `caracter(char)`, `concatenare(nfa1, nfa2)`, `alternare(nfa1, nfa2)`, `star(nfa1)`, `plus(nfa1)`, and `optional(nfa1)` are responsible for creating NFA fragments for individual symbols and regular expression operators.

3.  **NFA to DFA Conversion (Subset Construction):**
    * The core of the script lies in its ability to convert the constructed NFA into an equivalent DFA. The subset construction algorithm is used for this purpose. This algorithm is essential for creating a DFA that recognizes the same language as the original NFA.
    * Functions like `compute_lamd_closure(state, transitions)` (to compute the lambda closure of states) and `convert_nfa_to_dfa(nfa_config)` implement the subset construction.

4.  **DFA Simulation:**
    * Finally, the script includes a DFA simulator. This component takes a DFA and a word (string) as input and determines whether the DFA accepts the word.
    * The `check(dfa, word)` function performs this simulation.

##   Execution

To run the code:

1.  Ensure that both the Python script (`regtoDfa.py`) and the JSON file containing the test cases (`LFA-Assignment2_Regex_DFA_v2.json`) are located in the same directory.
2.  Open a command-line interface and navigate to the directory containing these files.
3.  Execute the script using the following command:

    ```bash
    python3 .\regtoDfa.py
    ```

##   Output

The script will process the regular expressions and test strings provided in the JSON file. For each test case, it will print:

* The name of the test case.
* For each test string:
    * `word Corect` if the generated DFA correctly accepts or rejects the word, matching the expected outcome in the JSON file.
    * `word Incorect` if the generated DFA's result does not match the expected outcome.

In essence, the script verifies the correctness of the DFA conversion by comparing the DFA's behavior on test strings with the expected results defined in the JSON file.
