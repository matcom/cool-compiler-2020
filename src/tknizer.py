import re
from typing import List, Tuple, Union
from grammar.symbols import EOF
from lexer.tokens import Token
from grammar.grammar import Terminal

RegexTypes = Tuple[Union[str, Terminal], str]


class Tokenizer:
    def __init__(self, regex_table: List[RegexTypes], eof: EOF):
        self.regexs = self._build_regexs(regex_table)
        self.eof = eof
        self.line = 1
        self.column = 1

    def _build_regexs(self, regex_table):
        regexs = regex_table
        fixed_line_token = "\n"
        fixed_space_token = " "

        regexs.append(("Line", fixed_line_token))
        regexs.append(("Space", fixed_space_token))
        return regexs

    def _walk(self, string: str):
        matched_suffix = ""
        tt = None

        for token_type, regex in self.regexs:
            match = re.match(regex, string)
            if match is not None:
                msuffix = match.group()
                if len(msuffix) > len(matched_suffix):
                    matched_suffix = msuffix
                    tt = token_type

        return matched_suffix, tt

    def _tokenize(self, text):
        while text:
            string = text
            suffix, token_type = self._walk(string)
            if token_type is None:
                next_token = string.split()[0]
                raise SyntaxError(
                    f"({self.line},{self.column}) - LexicographicError: Unexpected Token %s"
                    % next_token
                )
            elif token_type in ("StringError", "StringEOF"):
                newlines = re.split(r"\\\n|\n", suffix.strip())
                if len(newlines) > 1:
                    self.line += len(newlines) - 1
                    self.column = len(newlines[-1]) + 1
                else:
                    self.column += len(newlines[0])
                raise SyntaxError(
                    f"({self.line},{self.column}) - LexicographicError: {token_type} {suffix}"
                )
            elif token_type == "Line":
                self.column = 1
                self.line += 1
            elif token_type == "Space":
                self.column += 1
            elif isinstance(token_type, Terminal) and token_type.Name in (
                "quoted_string_const",
                "tilde_string_const",
            ):
                if "\0" in suffix:
                    newlines = re.split(r"\\\n", suffix)
                    for line in newlines:
                        if "\0" in line:
                            self.column = line.index("\0") + 1
                            raise SyntaxError(
                                f"({self.line},{self.column}) - LexicographicError: String contains null character"
                            )
                        newlines += 1
                # Strings may have some troubles with rows and columns
                newlines = re.split(r"\\\n", suffix)
                # Now we have a list with every line of the string
                # we need to sum every line to the lines and make
                # columns equal to the length of the last line.
                # Note that in case no scaped newline is found in
                # string, then splits return a single element list
                # with the full list, so next code should do
                # the work.
                self.line += len(newlines) - 1
                self.column = len(newlines[-1])
            else:
                self.column += len(suffix)
            yield suffix, token_type
            text = text[len(suffix) :]
        yield "$", self.eof

    def __call__(self, text):
        tokens = []
        for lex, token_type in self._tokenize(text):
            if token_type not in ("Line", "Space"):
                tokens.append(Token(lex, token_type, self.column, self.line))
        return tokens
