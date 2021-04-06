from enum import Enum
import constants
#from grammar import GrammarStructure
#
class TokenType(Enum):
    # A word. The default, normal token type
    WORD = 0
    # A punctuation that is in a list of punctuation defined in constants.py
    PUNCTUATION = 1
    # A literal token. representing a string value
    LITERAL = 2
    # A number token. representing a number value.
    NUMBER = 3
    # Illegal tokens. Literally doesn't exist but is included anyway
    ILLEGAL = 4
# A token
class Token:
    def __init__(self, value, rowNums = 0, columnNums = 0, parsedTokens = None, tokenType = None, isLiteral = False, comment_layers = 0):
        # The literal string of the token
        self.value = value
        # The type of the token, is a tokentype
        self.tokenType = tokenType
        # The row number of where the token is
        self.rowNums = rowNums
        # The column number of where the token is
        self.columnNums = columnNums
        # The ParsedToken object associated with this token. Not sure why that's here.
        self.parsedTokens = parsedTokens
        # The value of the token. will be a number if it is a number, otherwise it's the same as value.
        self.tokenValue = self.value
        if isLiteral:
            self.tokenType = TokenType.LITERAL
        if self.tokenType == None:
            self.autoAssignType()
        # How many comment layer there is.
        self.comment_layers = comment_layers
    def __repr__(self):
        return "{0}({1} token at {2},{3})".format(self.value, self.tokenType.name if self.tokenType != None else "Undefined", self.rowNums, self.columnNums) + ("(ignored)" if self.comment_layers > 0 else "")
    # Whether this is ignored.
    def ignored(self, comment_layers = 0):
        return self.comment_layers > comment_layers
    # @property
    # def structureType(self):
    #     return GrammarStructure.NOUN
    # Auto assign a type to this token.
    def autoAssignType(self):
        self.tokenType = None
        if self.tokenType == None:
            try:
                val = constants.toNumber(self.value)
                self.tokenValue = val
                self.tokenType = TokenType.NUMBER
            except:
                pass
        if self.tokenType == None and self.value in constants.punctuations:
            self.tokenValue = self.value
            self.tokenType = TokenType.PUNCTUATION
        if self.tokenType == None:
            self.tokenValue = self.value
            self.tokenType = TokenType.WORD
# A bunch of parsed tokens. Using parser logic.
# The logic of parser:
# Whitespace are ignored except when they are used to separate tokens.
# Punctuations are always single character.
# Literal string is parsed specially. Literal strings are surrounded by double quotes, and everything
# between them is counted toward the token, including whitespaces.
# Everything else is one word, separated by whitespace or other tokens
# Words and punctuations are separate, except . when used as decimal numbers.
# Then, if that "word" happens to be a number, it's a number.
class ParsedTokens:
    def __init__(self, string_to_tokenize, index = 0, ignore_comments = True, rowNums = None, columnNums = None):
        tokens = []
        tokenString = ""
        isonlynum = True
        decimalPointUsed = False
        leftBrackets = 0
        if rowNums == None:
            rowNums = 1
        if columnNums == None:
            columnNums = 1
        def addStringToTokens(string, doEndProcess = True):
            nonlocal tokenString, isonlynum, decimalPointUsed
            if string != "" and (not ignore_comments or leftBrackets == 0):
                if len(string) > 1 and string[-1] == ".":
                    tokens.append(Token(string[:-1], rowNums, columnNums - len(string), comment_layers = leftBrackets))
                    tokens.append(Token(string[-1], rowNums, columnNums - len(string), comment_layers = leftBrackets))
                else:
                    tokens.append(Token(string, rowNums, columnNums - len(string), comment_layers = leftBrackets))
            tokenString = ""
            isonlynum = True
            decimalPointUsed = False
        def incrementIndex(character):
            nonlocal index, rowNums, columnNums
            index += 1
            if character == "\n":
                rowNums += 1
                columnNums = 1
            else:
                columnNums += 1
        while index < len(string_to_tokenize):
            doAutoIncrement = True
            nextChar = string_to_tokenize[index]
            #print(nextChar)
            if nextChar.isspace():
                if tokenString != "":

                    addStringToTokens(tokenString)
                    # if len(tokenString) > 1 and tokenString[-1] == ".":
                    #     if not ignore_comments or leftBrackets == 0:
                    #         addStringToTokens(tokenString[:-1])
                    #         addStringToTokens(tokenString[-1])
                    #         # tokens.append(Token(tokenString[:-1], comment_layers = leftBrackets))
                    #         # tokens.append(Token(tokenString[-1], comment_layers = leftBrackets))
                    # else:
                    #     if not ignore_comments or leftBrackets == 0:
                    #         addStringToTokens(tokenString)
                    #         tokens.append(Token(tokenString, comment_layers = leftBrackets))
            elif nextChar == "\"":
                tokenResult = tokenizeLiteral(string_to_tokenize, index, rowNums, columnNums)
                if tokenResult == None:
                    raise "Invalid token starting at index {}.".format(index)
                if not ignore_comments or leftBrackets == 0:
                    tokenResult[0].comment_layers += leftBrackets
                    tokenResult[0].rowNums = rowNums
                    tokenResult[0].columnNums = columnNums
                    tokens.append(tokenResult[0])
                index = tokenResult[1]
                rowNums = tokenResult[2]
                columnNums = tokenResult[3]
                doAutoIncrement = False
            elif nextChar == "(":
                
                if tokenString != "":
                    addStringToTokens(tokenString)
                    # if len(tokenString) > 1 and tokenString[-1] == ".":
                    #     if not ignore_comments or leftBrackets == 0:
                    #         tokens.append(Token(tokenString[:-1], comment_layers = leftBrackets))
                    #         tokens.append(Token(tokenString[-1], comment_layers = leftBrackets))
                    # else:
                    #     if not ignore_comments or leftBrackets == 0:
                    #         tokens.append(Token(tokenString, comment_layers = leftBrackets))
                leftBrackets += 1
                addStringToTokens('(')
            elif nextChar == ")" and leftBrackets > 0:
                if tokenString != "":
                    addStringToTokens(tokenString)
                    # if len(tokenString) > 1 and tokenString[-1] == ".":
                    #     if not ignore_comments or leftBrackets == 0:
                    #         tokens.append(Token(tokenString[:-1], comment_layers = leftBrackets))
                    #         tokens.append(Token(tokenString[-1], comment_layers = leftBrackets))
                    # else:
                    #     if not ignore_comments or leftBrackets == 0:
                    #         tokens.append(Token(tokenString, comment_layers = leftBrackets))
                addStringToTokens(')')
                leftBrackets -= 1
                
            elif nextChar in constants.punctuations:
                if isonlynum and nextChar == "." and not decimalPointUsed:
                    tokenString += nextChar
                    decimalPointUsed = True
                else:#if len(tokenString) > 0 and not tokenString[-1] in constants.punctuations:
                    addStringToTokens(tokenString)
                    # if tokenString != "" and (not ignore_comments or leftBrackets == 0):
                    #     tokens.append(Token(tokenString, comment_layers = leftBrackets))
                    tokenString = nextChar
                    isonlynum = False
                # else:
                #     tokenString += nextChar
                #     isonlynum = False
            else:
                if nextChar.isdigit() and isonlynum:
                    tokenString += nextChar
                elif len(tokenString) > 0 and tokenString[-1] in constants.punctuations:
                    addStringToTokens(tokenString)
                    # if len(tokenString) > 1 and tokenString[-1] == ".":
                    #     if not ignore_comments or leftBrackets == 0:
                    #         tokens.append(Token(tokenString[:-1], comment_layers = leftBrackets))
                    #         tokens.append(Token(tokenString[-1], comment_layers = leftBrackets))
                    # else:
                    #     if not ignore_comments or leftBrackets == 0:
                    #         tokens.append(Token(tokenString, comment_layers = leftBrackets))
                    tokenString = nextChar
                    isonlynum = nextChar.isdigit()
                else:
                    tokenString += nextChar
                    isonlynum = False
            if doAutoIncrement:
                incrementIndex(nextChar)
        if tokenString != "":
            addStringToTokens(tokenString)
            # if len(tokenString) > 1 and tokenString[-1] == ".":
            #     if not ignore_comments or leftBrackets == 0:
            #         tokens.append(Token(tokenString[:-1], comment_layers = leftBrackets))
            #         tokens.append(Token(tokenString[-1], comment_layers = leftBrackets))
            # else:
            #     if not ignore_comments or leftBrackets == 0:
            #         tokens.append(Token(tokenString))
        self.tokens = tokens
    def __repr__(self):
        returnStr = ""
        for i in self.tokens:
            if returnStr == "":
                returnStr += str(i)
            else:
                returnStr += ", " + str(i)
        return returnStr
# Get a number token
# Accepts normal decimal number, 8-base(0...), 2-base(00...), 16-base(0x...), decimal(works with all bases)
# Scientific notation(...e...), the two numbers are actually seperate.
# Returns a token and a index if succesfully generated a token, otherwise returns none
# def getNumberToken(string_to_tokenize, index = 0, override_base = None, allow_non_int = True):
#     number = 0
#     base = 10 if override_base == None else override_base
#     if override_base == None and string_to_tokenize[index] == "0" and index + 1 < len(string_to_tokenize):
#         # Binary
#         if string_to_tokenize[index + 1] == "0":
#             base = 2
#             index = index + 2
#         # Hexadecimal
#         elif string_to_tokenize[index + 1] == "x":
#             base = 16
#             index = index + 2
#         # Special cases, ignore
#         elif string_to_tokenize[index + 1] == "e" or string_to_tokenize[index + 1] == ".":
#             pass
#         # Octal
#         else:
#             base = 8
#             index = index + 1
#     while index < len(string_to_tokenize):
#         nextChar = string_to_tokenize[index]
#         if nextChar.isdigit():
#             value = int(nextChar)
#             if value >= base: return None
#             number = number * base + value
#         elif nextChar >= "A" and nextChar <= "F":
#             value = ord(nextChar) - ord("A") + 10
#             if value >= base: return None
#             number = number * base + value
#         elif nextChar >= "a" and nextChar <= "f":
#             value = ord(nextChar) - ord("a") + 10
#             if value >= base: return None
#             number = number * base + value
#         # illegal characters
#         elif not nextChar in constants.punctuations and not nextChar.isspace() and not nextChar.lower() == "e":
#             return None
#         else:
#             break
#         index += 1
#     #print(index)
#     # if index + 1 < len(string_to_tokenize) and string_to_tokenize[index] == "." and string_to_tokenize[index + 1] in constants.allowedHexadecimals:
#     #     index += 1
#     #     decimalNums = 0
#     #     while index < len(string_to_tokenize):
#     #         nextChar = string_to_tokenize[index]
#     #         if nextChar.isdigit():
#     #             value = int(nextChar)
#     #             number = number * base + value
#     #             decimalNums += 1
#     #         elif nextChar >= "A" and nextChar <= "F":
#     #             value = ord(nextChar) - ord("A") + 10
#     #             number = number * base + value
#     #             decimalNums += 1
#     #         elif nextChar >= "a" and nextChar <= "f":
#     #             value = ord(nextChar) - ord("a") + 10
#     #             number = number * base + value
#     #             decimalNums += 1
#     #         else:
#     #             break
#     #         index += 1
#     #     number = number / (base ** decimalNums)
#     print(number)
#     return Token(number, TokenType.NUMBER)
#     input()
# Logic to tokenize literal strings.
def tokenizeLiteral(string_to_tokenize, index = 0, rowNums = None, columnNums = None):
    if string_to_tokenize[index] != "\"":
        return None
    if rowNums == None:
        rowNums = 1
    if columnNums == None:
        columnNums = 1
    literalString = ""
    lineString = "\""
    def incrementIndex(character = None):
        nonlocal index, rowNums, columnNums
        index += 1
        if character == "\n":
            rowNums += 1
            columnNums = 1
        else:
            columnNums += 1
    incrementIndex()
    
    while index < len(string_to_tokenize):
        #print(index)
        doAutoIncrement = True
        nextChar = string_to_tokenize[index]
        #print(nextChar)
        if index + 1 < len(string_to_tokenize) and nextChar == "\\" and string_to_tokenize[index + 1] in constants.escape_map:
            literalString += constants.escape_map[string_to_tokenize[index + 1]]
            incrementIndex(constants.escape_map[string_to_tokenize[index + 1]])
        elif nextChar == "\n":
            if lineString.isspace():
                literalString += lineString
            lineString = ""
            literalString += "\n"
        elif nextChar == "\"":
            if (lineString.isspace() or lineString == ""):
                lineString = "\""
            else:
                incrementIndex(nextChar)
                break
        elif nextChar.isspace() and (lineString.isspace() or lineString == ""):
            lineString += nextChar
        else:
            if (lineString.isspace() or lineString == ""):
                literalString += lineString
                lineString = nextChar
                literalString += nextChar
            else:
                literalString += nextChar
        if doAutoIncrement:
            incrementIndex(nextChar)
    return Token(literalString, isLiteral = True), index, rowNums, columnNums
if __name__ == "__main__":
    tokens = ParsedTokens(r"""
    Ingsoc:
    "War is peace
    "freedom is slavery
    "ignorance is strength".
    """, ignore_comments = False)
    for i in tokens.tokens:
        print(i)