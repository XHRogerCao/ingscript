# Ignore this. This is deprecated.


from tokenizer import *
import constants
from constants import equalInEnglish
# Result of a parsing of tokens.
class Result:
    def __init__(self, value, tokenPos):
        self.value = value
        self.tokenPos = tokenPos
    def __repr__(self):
        return "Result({},{})".format(self.value, self.tokenPos)
# An abstract parser class
class Parser:
    # The result of the parsing when this parser is called.
    # If successfully parsed, return a result. Otherwise, return None
    def __call__(self, tokens, pos = 0):
        if pos >= len(tokens):
            return None
    # Parser shortcut:
    # You can use "+" on two or more parsers to automatically use a ConcatParser
    # Easier for writing stuff.
    def __add__(self, other):
        finalList = []
        if isinstance(self, ConcatParser):
            finalList += self.parsers
        else:
            finalList.append(self)
        if isinstance(other, ConcatParser):
            finalList += other.parsers
        else:
            finalList.append(other)
        print(finalList)
        return ConcatParser(*finalList)
    # Parser shortcut:
    # You can use "|" on two or more parsers to automatically use a AlternateParser
    # Easier for writing stuff.
    def __or__(self, other):
        finalList = []
        if isinstance(self, AlternateParser):
            finalList += self.parsers
        else:
            finalList.append(self)
        if isinstance(other, AlternateParser):
            finalList += other.parsers
        else:
            finalList.append(other)
        print(finalList)
        return AlternateParser(*finalList)
    # Parser shortcut:
    # You can use "~" on a parser to indicate that this parser is optional.
    def __invert__(self):
        return OptParser(self)
    # Parser shortcut:
    # You can use "*" on two or more parsers to automatically use a RepeatParser
    def __mul__(self, other):
        return RepeatParser(self, other if isinstance(other, Parser) else None)
    def __xor__(self, other):
        return ProcessParser(self, other)
    def setFields(self, **fields):
        for key in fields:
            self.__dict__[key] = fields[key]
# A parser that only looks for a constant list of tokens.
# Does not allow literals.
class ConstParser(Parser):
    def __init__(self, string):
        if isinstance(string, str):
            self.values = string.split(" ")
        else:
            self.values = string
    def __call__(self, tokens, pos = 0):
        if pos >= len(tokens):
            return None
        initPos = pos
        for i in self.values:
            if pos >= len(tokens):
                return None
            if not equalInEnglish(i, tokens[pos].value) or tokens[pos].tokenType == TokenType.LITERAL:
                return None
            pos += 1
        if len(self.values) == 1:
            return Result(tokens[initPos], pos)
        return Result(tokens[initPos:pos], pos)
# A parser that looks for a token of a certain type, with a specified condition.
# Either token type and condition can be None.
# If token type is none, then any token type can fit this parser
# If condition is none, then no additional conditions will be checked.
# If both are none, this eats any token.
class TypeParser(Parser):
    def __init__(self, tokenType = None, condition = None):
        self.tokenType = tokenType
        self.condition = condition
    def __call__(self, tokens, pos=0):
        if pos >= len(tokens):
            return None
        if self.tokenType and self.tokenType != tokens[pos].tokenType:
            return None
        if self.condition and not self.condition(tokens[pos]):
            return None
        return Result(tokens[pos], pos + 1)
# A parser that when parsed, all parsers contain must successfully parse as well.
# For example, NUMBER + "+" + NUMBER require the parsing of a number, the plus sign, and another number
# To succeed the parsing.
class ConcatParser(Parser):
    def __init__(self, *parsers):
        self.parsers = parsers
    def __call__(self, tokens, pos=0):
        results = []
        for parser in self.parsers:
            oneResult = parser(tokens, pos)
            if not oneResult:
                return None
            results.append(oneResult)
            pos = oneResult.tokenPos
        return Result(results, pos)
# A parser that can succeed when any parser succeed.
# If one parser successfully parsed the tokens, all other parsers are ignored.
# For example, "one" | "two" | "three" requires the tokens to be either one, two three(word, not literal)
class AlternateParser(Parser):
    def __init__(self, *parsers):
        self.parsers = parsers
    def __call__(self, tokens, pos=0):
        for parser in self.parsers:
            oneResult = parser(tokens, pos)
            if oneResult:
                return oneResult
        return None
# An optional parser that doesn't fail when parsed.
class OptParser(Parser):
    def __init__(self, parser):
        self.parser = parser
    def __call__(self, tokens, pos=0):
        result = self.parser(tokens, pos)
        if result: return result
        return Result(None, pos)
# A parser that takes a parser and an optional separator.
# The parser repeats until it can't no more.
class RepeatParser(Parser):
    def __init__(self, parser, separator = None, allowLingeringSeparator = False):
        self.parser = parser
        self.separator = separator
        self.allowLingeringSeparator = allowLingeringSeparator
    def __call__(self, tokens, pos=0):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result)
            pos = result.tokenPos
            if self.separator:
                separatorResult = self.separator(tokens, pos)
                if not separatorResult:
                    return Result(results, pos)
                pos = separatorResult.tokenPos
            result = self.parser(tokens, pos)
        if len(results) == 0:
            return None
        if self.allowLingeringSeparator:
            return Result(results, pos)
        else:
            return Result(results, results[-1].tokenPos)
# A parser that process a result with process_fn
class ProcessParser(Parser):
    def __init__(self, parser, process_fn):
        self.parser = parser
        self.process_fn = process_fn
    def __call__(self, tokens, pos=0):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.process_fn(result.value)
            return result
        return None
# A parser that is a custom function.
class LazyParser(Parser):
    def __init__(self, parser_fn):
        self.parser = None
        self.parser_fn = parser_fn
    def __call__(self, tokens, pos=0):
        if not self.parser:
            self.parser = self.parser_fn()
        return self.parser(tokens, pos)
class CompleteParser(Parser):
    def __init__(self, parser):
        self.parser = parser
    def __call__(self, tokens, pos=0):
        result = self.parser(tokens, pos)
        if result and result.tokenPos == len(tokens):
            return result
        return None
if __name__ == "__main__":
    testParser = TypeParser(TokenType.NUMBER) * ConstParser(",")
    rawString = "1,4,5,9,"
    parsedTokens = ParsedTokens(rawString)
    print(parsedTokens)
    print(testParser(parsedTokens.tokens))