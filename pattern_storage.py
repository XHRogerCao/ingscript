from grammar import *
from tree import *
from constants import *
from traceback import format_exc
from copy import copy
# A dictionary that stores various patterns in it.
# Dictionaries is a dictionary of PatternDictionary, with the key indicates the scope of the things
# "" indicates the global scope
# Scopes are spearated with "/"
class PatternDictionary:
    # Number of dictionaries already created. Used to autogenerate scope names.
    numOfPatternDict = 0
    # A list of existing dictionary
    dictionaries = {}
    # The current scope. Matters when creating new scopes.
    currentScope = ""
    # Whenever a new dictionary should be created, it look for whether there exists a dictionary with
    # the same scope. If yes, then return that dictionary; otherwise, create a new ictionary.
    # ParentScope can be a string representing a scope or a patterndictionary.
    # If scopeName is None, autogenerate a scope name(guarenteed to be unique unless you use numeric scope name before)
    def __new__(cls, dictionary = None, parentScope = None, scopeName = None):
        scope = ""
        if isinstance(parentScope, str):
            parentScope = cls.dictionaries[parentScope]
        if parentScope != None:
            scope = parentScope.scope + "/" + (str(PatternDictionary.numOfPatternDict) if scopeName == None else scopeName)
        #print(scope)
        cls.currentScope = scope
        if not scope in PatternDictionary.dictionaries:
            return super(PatternDictionary, cls).__new__(cls)
        else:
            super(PatternDictionary, cls).__new__(cls)
            return PatternDictionary.dictionaries[scope]
    def __init__(self, dictionary = None, parentScope = None, scopeName = None):
        # A dictionary of patterns to look for. It is stored as a dictionary of lists, where the key is
        # the first non-cast word and the value is a list of possible phrases associated with that key
        self.dictionary = dictionary or {}
        # The scope of the dictionary.
        # It is store as a string, separated by "/"
        self.scope = ""
        # Doesn't do anything right now, but I don't want to remove it.
        self.sentenceMarked = {}
        if isinstance(parentScope, str):
            parentScope = PatternDictionary.dictionaries[parentScope]
        if parentScope != None:
            self.scope = parentScope.scope + "/" + (str(PatternDictionary.numOfPatternDict) if scopeName == None else scopeName)
        if not self.scope in PatternDictionary.dictionaries:
            PatternDictionary.dictionaries[self.scope] = self
        else:
            PatternDictionary.dictionaries[self.scope].dictionary.update(self.dictionary)
        PatternDictionary.numOfPatternDict += 1
    # Add an entry to the dictionary. With a key and a value.
    # Create a new list if no list exists at the key; otherwise, append to the list and sort it.
    def addEntryToDictionary(self, key, value):
        if key in self.dictionary:
            self.dictionary[key].append(value)
            self.dictionary[key].sort(reverse = True)

        else:
            self.dictionary[key] = [value]
    # Add a sentencepiece to the dictionaries.
    # Automatically get what key should be used(First non-cast item)
    def addEntry(self, newEntry):
        #self.addEntryToDictionary(newEntry.identifier, newEntry)
        splitPattern = newEntry.identifier.split(" ")
        for word in splitPattern:
            if not (isCastStr(word)):
                self.addEntryToDictionary(word, newEntry)
                break
        if "alias" in newEntry.doc:
            if isinstance(newEntry.doc["alias"],str):
                self.addEntry(AliasPiece(newEntry.doc["alias"], newEntry))
            else:
                for alias in newEntry.doc["alias"]:
                    self.addEntry(AliasPiece(alias, newEntry))
        return self
    # Add multiple entries to the dictionaries.
    def addEntries(self, *entries):
        for entry in entries:
            self.addEntry(entry)
        return self
    # Add a label to a sentence.
    def labelSentence(self, sentence, label):
        assert label != None
        self.sentenceMarked[label] = sentence
    def getSentenceByLabel(self, label):
        for scope in reversed(self.parentScopes):
            tempDict = PatternDictionary.dictionaries[i]
            if label in tempDict.sentenceMarked:
                return tempDict.sentenceMarked[label]
        return None
    # Get a list of ancestor scopes associated with this scope, including self for the purpose of iterating.
    @property
    def parentScopes(self):
        scopeNames = self.scope.split("/")
        parentScopes = []
        for i in scopeNames:
            if len(parentScopes) > 0:
                parentScopes.append(parentScopes[-1] + "/" + i)
            else:
                parentScopes.append(i)
        return parentScopes
    # Collect all possible sentence pieces associated with an identifier.
    # First look for those in self, then look for those in parent, and so on.
    def collectPossiblePieces(self, identifier):
        possiblePieces = []
        parentScopes = self.parentScopes
        #print(parentScopes)
        for i in reversed(parentScopes):
            #print(possiblePieces)
            if identifier in PatternDictionary.dictionaries[i].dictionary:
                possiblePieces += PatternDictionary.dictionaries[i].dictionary[identifier]
        if identifier != removeTitleCase(identifier):
            for i in reversed(parentScopes):
                #print(possiblePieces)
                if removeTitleCase(identifier) in PatternDictionary.dictionaries[i].dictionary:
                    possiblePieces += PatternDictionary.dictionaries[i].dictionary[removeTitleCase(identifier)]
        #print(possiblePieces)
        return possiblePieces
    # Interpret tokens into one sentence, starting from pos.
    # If verbose is set to true, print debug information
    def interpretTokens(self, tokens, pos = 0, verbose = False):
        #stacks = []
        # A list of possible casts
        possibilities = []
        # The position that starts a possibility. Used to fall back position if a possibility is exhausted.
        # Should have the same length as possibilities
        startPos = []
        # Literally does nothing
        # checkPointer = 0
        
        # Any loose ends for certain phrases that needs to be added.
        endingStack = []
        # A list of potential errors with the code.
        potentialErrors = []
        #results = []
        #tempResult = None
        
        # Print the current amount of tokens parsed
        def generateCurrentPossibilityStr():
            strList = []
            for i in possibilities:
                if len(i) > 0:
                    strList.append(str(i[0]))
            return "[" + ", ".join(strList) + "]"

        # Add all that's possible for something.
        # Return True if at least 1 possibility, false otherwise.
        def addPossibilities():
            nonlocal possibilities, startPos#,results
            if pos >= len(tokens):
                return False
            token = tokens[pos]
            startPos.append(pos)
            if token.tokenType == TokenType.WORD or token.tokenType == TokenType.PUNCTUATION or token.tokenType == TokenType.NUMBER:
                possibilities.append([])
                for piece in self.collectPossiblePieces(token.value):
                    theCopy = copy(piece)
                    possibilities[-1].append(theCopy)
                    possibilities[-1][-1].rowNums, possibilities[-1][-1].columnNums = \
                        token.rowNums, token.columnNums
                    possibilities[-1][-1].scope = self
                if token.tokenType == TokenType.NUMBER:
                    possibilities[-1].append(NumberPhrase(token.value))
                    possibilities[-1][-1].rowNums, possibilities[-1][-1].columnNums = \
                        token.rowNums, token.columnNums
                    possibilities[-1][-1].scope = self
                
            elif token.tokenType == TokenType.LITERAL:
                possibilities.append([LiteralPhrase(token.value)])
                possibilities[-1][-1].rowNums, possibilities[-1][-1].columnNums = \
                    token.rowNums, token.columnNums
                possibilities[-1][-1].scope = self
            else:
                possibilities.append([])
            if len(endingStack) > 0:
                possibilities[-1].append(endingStack[-1])
                if possibilities[-1][0] == endingStack[-1]:
                    endingStack.pop()
            else:
                possibilities[-1].append(StaticPhrase('.',GMSTR_SPECIAL, priority=PRIORITY_LOWEST))
                possibilities[-1][-1].rowNums, possibilities[-1][-1].columnNums = \
                    token.rowNums, token.columnNums
                possibilities[-1][-1].scope = self
            if len(possibilities[-1]) > 0:
                return True
            else:
                potentialErrors.append((
                    100,
                    "({0},{1}): No identifier matches \"{2}\"\n    Parsed Values: {3}".format(token.rowNums, token.columnNums, token.value, generateCurrentPossibilityStr())
                ))
                return False
            #results.append(ParsedResult(possibilities[0]))
            #results.append([])
        # Check if the current pattern matches the tokens.
        # Returns True if completely matches, "addPhrase" if only matches until a cast(in which case
        # adds a new possibility to endingStack), False if pattern does not match.
        def checkPatternMatch():
            nonlocal pos
            initPos = pos
            if isinstance(possibilities[-1][0], LiteralPhrase):
                returnval = tokens[pos].tokenType == TokenType.LITERAL and tokens[pos].value == possibilities[-1][0].identifier
                if returnval:
                    pos += 1
                return returnval
            if tokens[pos].tokenType == TokenType.LITERAL:
                return False
            checkPattern = possibilities[-1][0].splitPatterns()
            hasNonCast = False
            for i in range(len(checkPattern)):
                if isinstance(checkPattern[i], Cast):
                    #endingStack.append(possibilities[-1][0].getNextTracker())
                    if hasNonCast:
                        return "addPhrase"

                else:
                    hasNonCast = True
                    patternToCheck = checkPattern[i]
                    if patternToCheck != "/" and "/" in patternToCheck:
                        patternToCheck = patternToCheck.split("/")
                    else:
                        patternToCheck = [patternToCheck]
                    succeedPatternCheck = False
                    for j in patternToCheck:
                        if j == tokens[pos].value or j == removeTitleCase(tokens[pos].value) or (j == "" and tokens[pos].value == "/"):
                            succeedPatternCheck = True
                            break
                    if not succeedPatternCheck:
                        pos = initPos
                        return False
                    pos += 1
            return True
        # Moves on to the next possibility,
        # Returns false if there are no more possibilities
        def popPossibility():
            nonlocal pos
            while len(possibilities) > 0 and len(possibilities[-1]) == 0:
                possibilities.pop()
                startPos.pop()
            if len(possibilities) == 0:
                return False
            
            temp = possibilities[-1].pop(0)
            if len(endingStack) > 0 and temp.parentPhrase == endingStack[-1].parentPhrase and temp != endingStack[-1]:
                endingStack.pop()
            if isinstance(temp, PhraseTracker):
                endingStack.append(temp)
            if len(possibilities[-1]) <= 0:
                if pos < len(tokens):
                    potentialErrors.append((
                        0,
                        "({0},{1}): Invalid pattern \"{2}\"...\n    Parsed Values: {3}".format(tokens[pos].rowNums, tokens[pos].columnNums, tokens[pos].value, generateCurrentPossibilityStr())
                ))
                possibilities.pop()
                startPos.pop()
                if len(startPos) > 0:
                    pos = startPos[-1]
                return popPossibility()
            else:
                if len(endingStack) > 0 and possibilities[-1][0] == endingStack[-1]:
                    endingStack.pop()
            return True
        # Build a grammar tree from start to end. Both an index to the array "possibilities".
        # The index are inclusive
        # If successful, returns the grammar tree built; otherwise, throw an error.
        def buildGrammarTree(start, end, prevTree = None):
            result = buildGrammarTreeWithStart(start, end, prevTree)
            if result[1] > end:
                return result[0]
            else:
                return buildGrammarTree(result[1], end, result[0])
        # Build a grammar tree based from start. Will return a grammar tree and a end point if successful
        # the end point indicates the index that the code should check first, so 1+the index included in the
        # grammar tree.
        # The index is for possibilities.
        def buildGrammarTreeWithStart(start, end = None, prevTree = None):
            if isinstance(possibilities[start][0], DynamicPhrase):
                returnVal = GrammarTreeNode(possibilities[start][0])
                if prevTree != None:
                    assert \
                        len(possibilities[start][0].splitPatterns()) > 0 \
                        and isinstance(possibilities[start][0].splitPatterns()[0], Cast), \
                        "The first item in the pattern is not a cast, but prevTree is not None"
                        
                    returnVal.addChild(prevTree)
                else:
                    assert \
                        len(possibilities[start][0].splitPatterns()) == 0 \
                        or not isinstance(possibilities[start][0].splitPatterns()[0], Cast), \
                        "The first item in the pattern is a cast, but prevTree is None"
                start += 1
                end = start
                while len(returnVal.children) < returnVal.value.totalCasts:
                    if isinstance(possibilities[end][0], PhraseTracker) and possibilities[end][0].parentPhrase == returnVal.value:
                        returnVal.addChild(buildGrammarTree(start, end - 1))
                        start = end + 1
                    end += 1
                childI = 0
                for i in returnVal.value.splitPatterns():
                    if isinstance(i, Cast):
                        assert i.canCast(returnVal.children[childI]), "invalid cast"
                        childI += 1
                if verbose: print("Grammar tree:",returnVal)
                return returnVal, end
            else:
                returnVal = GrammarTreeNode(possibilities[start][0])
                if verbose: print("Grammar tree:",returnVal)
                return returnVal, start + 1
        # Same as buildGrammarTree, but will return None if failed instead of throwing an error.
        def tryBuildGrammarTree(start, end, prevTree = None):
            try:
                return buildGrammarTree(start, end, prevTree)
            except Exception as e:
                if verbose: print(e)
                if verbose: print(format_exc())
                potentialErrors.append((
                    1000,
                    "Trouble when parsing grammar tree: \"{0}\"...\n    Parsed Values: {1}".format(e, generateCurrentPossibilityStr())
                ))
                return None
        addPossibilities()
        # continue to parse until you have no item in endingStack and you find a period or there are
        # no tokens left. Then, convert what has been parsed into a grammar tree, and validate whether 
        # the grammar tree has the correct structure. If all is successful, returns the grammar tree and
        # the end position, representing a sentence. If possibilities are exhausted before building a 
        # successful sentence, return None and potential errors.
        while True:
            while (pos < len(tokens)):
                if verbose: print("Tokens Left: {}".format(tokens[pos:]))
                checkResult = checkPatternMatch()
                if checkResult == "addPhrase":
                    if verbose: print("new phrase added")
                    endingStack.append(possibilities[-1][0].getNextTracker())
                if checkResult:
                    if verbose: print("succeed check possibility")
                    if possibilities[-1][0].identifier == "." and possibilities[-1][0].structureType == GMSTR_SPECIAL:
                        if verbose: print("successfully parsed")
                        endResult = tryBuildGrammarTree(0,len(possibilities) - 2)
                        if verbose: print(endResult)
                        if endResult and endResult.value.structureType == GMSTR_SENTENCE:
                            endResult.assignSentenceLabelToValue()
                            return endResult, pos
                        else:
                            if verbose: print("incorrect grammar, rollback structure")
                            popResult = popPossibility()
                            if not popResult:
                                if verbose: print("Fail to interpret tokens")
                                return None, potentialErrors
                    else:
                        addPossibilities()
                else:
                    if verbose: print("fail possibility")
                    popResult = popPossibility()
                    if not popResult:
                        if verbose: print("Fail to interpret tokens")
                        return None, potentialErrors
            while len(endingStack) > 0 and len(endingStack[-1].splitPatterns()) == 0:
                possibilities.append([endingStack.pop()])
            if len(endingStack) == 0:
                if verbose: print("successfully parsed")
                endResult = tryBuildGrammarTree(0,len(possibilities) - 1)
                if verbose: print(endResult)
                if endResult and endResult.value.structureType == GMSTR_SENTENCE:
                    endResult.assignSentenceLabelToValue()
                    return endResult, pos
                else:
                    if verbose: print("incorrect grammar, rollback structure")
                    popResult = popPossibility()
                    if not popResult:
                        if verbose: print("Fail to interpret tokens")
                        return None, potentialErrors
                #return tryBuildGrammarTree(startPos[0], pos - 1)
            else:
                popResult = popPossibility()
                if not popResult:
                    if verbose: print("Fail to interpret tokens")
                    return None, potentialErrors
    # It's like interpretTokens, but interpret all tokens. This means that there can be multiple sentences.
    # Returns an actionblock if succeed, otherwise, print error and return None
    def interpretAllTokens(self, tokens, pos = 0, verbose = False):
        returnVal = []#ActionBlock()
        while pos < len(tokens):
            result = self.interpretTokens(tokens, pos, verbose)
            if result and result[0]:
                result[0].onHookup()
                pos = result[1]
                returnVal.append(result[0])
            else:
                result[1].sort(reverse = True)
                errorStrings = []
                for i in result[1]:
                    errorStrings.append(i[1])
                print("Fail to compile.\nPotential Errors:")
                print(*errorStrings,sep='\n')
                return None
        try:
            rVal = ActionBlock(returnVal)
            rVal.scope = self
            return rVal
        except Exception as e:
            print("Fail to compile:", e)
            return None
    # Interprets a string, but also parse it first into tokens.
    def interpretString(self, string, verbose = False):
        tokens = ParsedTokens(string)
        return self.interpretAllTokens(tokens.tokens, verbose=verbose)
    # Create a new scope and parse the string into tokens in that scope.
    @classmethod
    def parseActionBlock(cls, string, verbose = False):
        # print("currentscope: ", cls.currentScope)
        # print("another scope: ", PatternDictionary.currentScope)
        oldScope = cls.currentScope
        newScope = PatternDictionary(None, oldScope)
        returnVal = newScope.interpretString(string, verbose=verbose)
        cls.currentScope = oldScope
        return returnVal

    # Get entry by its identifier.
    def getEntryByIdentifier(self, identifier):
        pattern = identifier.split(" ")
        firstString = pattern[0]
        for i in pattern:
            if not isCastStr(i):
                firstString = i
                break
        possiblePieces = self.collectPossiblePieces(firstString)
        for i in possiblePieces:
            if i.identifier == identifier:
                return i
        return None
    # Add an alias to an existing entry
    def addAlias(self, original, newAliases):
        entry = self.getEntryByIdentifier(original)
        for i in newAliases:
            self.addEntry(
                AliasPiece(i,entry)
            )
    # Update a scope to self.
    # The reason i need this is because it prevents circular import.
    def updateScopeToSelf(self):
        self.__class__.currentScope = self.scope

def updateScope(scope):
    PatternDictionary.currentScope = scope
# Execute a string as an IngScript script.
def executeString(stringToExecute):
    action = PatternDictionary.parseActionBlock(stringToExecute)
    action()
if __name__ == "__main__":
    # "print the result of two plus x."
    # read print
    # lookup print
    # static verb, succeed.
    baseDict = PatternDictionary().addEntries(
        # Right now verb is too hard. It is therefore discontinued
        #StaticPhrase('print',GMSTR_VERB),
        DynamicPhrase(
            'print {0}',
            GMSTR_SENTENCE,
            [Cast(GMSTR_NOUN)],
            lambda self, a: print(a())
        ),
        DynamicPhrase(
            'the result of {0}',
            GMSTR_NOUN,
            [Cast(GMSTR_NOUN)],
            childValueFn
        ),
        DynamicPhrase(
            '{0} plus {1}',
            GMSTR_NOUN,
            [Cast(GMSTR_NOUN),Cast(GMSTR_NOUN)],
            lambda self, a,b: a() + b()    
        ),
        VariablePhrase(
            'x',
            IngScr_Variable(8, int)
        ),
        DynamicPhrase(
            'the {0}',
            GMSTR_NOUN,
            [Cast(GMSTR_NOUN)],
            childValueFn
        ),
        StaticPhrase(
            'two',
            GMSTR_NOUN,
            lambda self: 2
        ),
        StaticPhrase(
            'four',
            GMSTR_NOUN,
            lambda self: 4
        ),
        DynamicPhrase(
            'the answer to {0}',
            GMSTR_NOUN,
            [GMSTR_NOUN],
            childValueFn
        ),
        StaticPhrase(
            'result',
            GMSTR_NOUN,
            lambda self: "result"
        ),
    )
    tokens = ParsedTokens(r"""
    Print the result of two plus x plus 7. """)
    print(tokens.tokens)
    result = baseDict.interpretTokens(tokens.tokens)
    print("Result:")
    print(result)


    #result()
    #print(baseDict.dictionary)