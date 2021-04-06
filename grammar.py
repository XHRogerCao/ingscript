from enum import Enum
from tokenizer import *
#from pattern_storage import *
from constants import isCastStr, toNumber, isVowel
from tree import *
from variables import *
from copy import copy

class GrammarStructure(Enum):
    # Sentence is a complete statement, with a verb (potentially an object or a subject).
    # Usually a sentence must end with a period(.), but it can also belong in a phrase as well.
    SENTENCE = 0
    # A noun is an object. Like a variable, a datatype.
    NOUN = 1
    # A verb is like a function. Takes in up to 2 noun parameters(subject and object)
    VERB = 2
    # An adjective describes a noun's behavior. It change how the noun behaves.
    ADJECTIVE = 3
    # An adverb describes a verb(can describe another adjective in actual english,
    # but we just describe verb instead). Changes an action's behavior(Like asynchronously)
    ADVERB = 4
    # Probably not going to be used. Describes an adjective, though why the **** would you do that?
    ADJECTIVE_ADVERB = 5
    # Pronoun. Refer to something, but is not the thing, unlike noun.
    PRONOUN = 6
    # A custom phrase that can take arbitrary type of everything. English have rules except when it don't
    PHRASE = 7
    # Special phrases with special meanings. Like the period.
    SPECIAL = 8
# Simplify things by assigning constants.
GMSTR_SENTENCE = GrammarStructure.SENTENCE
GMSTR_NOUN = GrammarStructure.NOUN
GMSTR_VERB = GrammarStructure.VERB
GMSTR_ADJECTIVE = GrammarStructure.ADJECTIVE
GMSTR_ADVERB = GrammarStructure.ADVERB
GMSTR_ADJECTIVE_ADVERB = GrammarStructure.ADJECTIVE_ADVERB
GMSTR_PRONOUN = GrammarStructure.PRONOUN
GMSTR_PHRASE = GrammarStructure.PHRASE
GMSTR_SPECIAL = GrammarStructure.SPECIAL

# A word or a phrase. Has an identifier and a result.
# The result can be anything.
class SentencePiece:
    def __init__(
        self, 
        identifier = "", 
        structureType = GrammarStructure.NOUN, 
        valueFn = None, 
        hookupFn = None, 
        priority = 0,
        subpriority = 0,
        doc = None,
        ):
        super().__init__()
        # The identifier of this sentence
        # It's a string, with each piece separated by a space.
        # Every one piece of identifier is treated as literal, except for specific cases:
        # A string with the format "{n}" is a cast string, which means a cast goes here.
        # Only used in dynamic phrase.
        # A string can have "/" separating two or more other strings, showing that either phrase can go there.
        # A leading "/" plus another string(no space) represents that either "/" or that string can go there.
        self.identifier = identifier
        # What GrammarStructure is this
        self.structureType = structureType
        # Priority of this before sorting. Overrides default priority sorting
        self.priority = priority
        # Subpriority. does not override default sorting
        self.subpriority = subpriority
        # A function that has arguments:(self, *args), where args is the children grammartreenodes.
        # called whenever the value of the function is required.
        self.valueFn = valueFn
        # A function that has arguments:(self, *args), where args is the children grammartreenodes.
        # called whenever this string is initialized.
        self.hookupFn = hookupFn
        # Documentations associated with this piece.
        # It's a dictionary. To see what goes in there, see documentation.py
        self.doc = doc or {}
        # Row number. Only used when tied to a token
        self.rowNums = None
        self.columnNums = None
        self.scope = None
        # Caches the split pattern function return val so it doesn't take too long each time.
        self._splitPatternCache = None
    def __eq__(self, value):
        if isinstance(value, SentencePiece):
            return self.identifier == value.identifier and self.structureType == value.structureType
        return False
    def __lt__(self, value):
        #print("alohes")
        if isinstance(value, PhraseTracker):
            return self < value.parentPhrase
        if isinstance(self, StaticPhrase) and isinstance(value, DynamicPhrase):
            return False
        if isinstance(value, StaticPhrase) and isinstance(self, DynamicPhrase):
            return True
        #print("alohes")
        if isinstance(value, SentencePiece):
            if self.priority != value.priority:
                return self.priority < value.priority
            if len(self.identifier) != len(value.identifier):
                return len(self.identifier) < len(value.identifier)
            if self.subpriority != value.subpriority:
                return self.subpriority < value.subpriority
        return False
    def __repr__(self):
        return "{}({})".format(self.identifier.replace("\n","\\n"), str(self.structureType.name))
    def __hash__(self):
        return hash(self.identifier) ^ (hash(self.structureType))
    #
    # def matchPattern(self, tokens, allowCapitalization = True):
    #     pass
    # Will be overwritten in subclasses
    # Splits identifier into patterns
    def splitPatterns(self):
        pass
    # Get the next phrase tracker.
    def getNextTracker(self):
        if isCastStr(self.identifier.split(" ")[0]):
            return PhraseTracker(self, 2)
        return PhraseTracker(self, 1)
    @property
    def parentPhrase(self):
        return self
    # Format a string so that it's more readable.
    def processDocString(self, stringToProcess):
        returnVal = stringToProcess
        returnVal = returnVal.replace("{IDENTIFIER}", self.identifier)
        if returnVal[-1] == ".":
            return returnVal[:-1]
        return returnVal
    # Autogenerate a description for this function
    def autoDescription(self):
        if self.structureType == GMSTR_NOUN:
            return "A phrase that returns {IDENTIFIER}"
        return "A phrase that does {IDENTIFIER}"
    # Generate a documentation for this.
    def generateDocumentation(self):
        returnVal = ""
        returnVal += "Syntax: \"{}\".\n".format(self.processDocString(self.identifier))
        if "alias" in self.doc:
            returnVal += "Alias(es): "
            if isinstance(self.doc["alias"], str):
                returnVal += self.processDocString(self.doc["alias"])
            else:
                for i in range(len(self.doc["alias"])):
                    if i > 0:
                        returnVal += ", "
                    returnVal += self.processDocString(self.doc["alias"][i])
            returnVal += ".\n"
        returnVal += "Type: {}.\n".format(self.structureType.name.title())
        description = self.doc["desc"] if "desc" in self.doc else self.autoDescription()
        returnVal += "Description: {}.\n".format(self.processDocString(description))
        if isinstance(self, DynamicPhrase) and len(self.requiredCasts) > 0:
            returnVal += "Arguments:\n"
            argumentList = self.doc["argument"] if "argument" in self.doc else []
            for i in range(len(self.requiredCasts)):
                argumentDesc = argumentList[i] if i < len(argumentList) and argumentList[i] else self.requiredCasts[i].autoDescription()
                argumentDesc = "    {" + str(i) + "}: " + argumentDesc
                returnVal += self.processDocString(argumentDesc) + ".\n"
        if "return" in self.doc:
            returnVal += "Returns: {}.\n".format(self.processDocString(self.doc["return"]))
        return returnVal
# A static phrase is a word or a phrase that has doesn't require any parameter.
# For example, "output", "integer", "constant", "fractional number", "positive"
class StaticPhrase(SentencePiece):
    def __init__(
        self,
        identifier = "", 
        structureType = GrammarStructure.NOUN, 
        valueFn = None, 
        hookupFn = None,
        priority=0,
        subpriority = 0,
        doc = None,
        ):
        super().__init__(identifier, structureType, valueFn, hookupFn, priority, subpriority, doc)
    # Check if tokens(a list of Tokens) matches the pattern
    # def matchPattern(self, tokens, allowCapitalization = True):
    #     pattern = self.identifier.split(" ")
    #     if len(pattern) != len(tokens):
    #         return False
    #     for i in range(len(tokens)):
    #         if allowCapitalization and i == 0 and len(pattern[i]) > 0 and len(tokens[i].value) > 0 and pattern[i][0] == tokens[i].value[0].lower():
    #             if len(pattern[i]) == 1 and len(tokens[i].value) == 1:
    #                 continue
    #             elif pattern[i][1:] == tokens[i].value[1:]:
    #                 continue
    #         if pattern[i] != tokens[i].value:
    #             return False
    #     return True
    def splitPatterns(self):
        identifiers = self._splitPatternCache
        if identifiers == None:
            identifiers = self.identifier.split(" ")
            self._splitPatternCache == identifiers
        # for i in range(len(identifiers)):
        #     identifierString = identifiers[i]
        #     if len(identifierString) >= 3 and identifierString[0] == "{" and identifierString[-1] == "}" and identifierString[1:-1].isdigit():
        #         index = int(identifierString[1:-1])
        #         identifiers[i] = self.requiredCasts[index]
        return identifiers
# A phrase associated with a variable.
# Autogenerate valuefn
class VariablePhrase(StaticPhrase):
    def __init__(
        self,
        identifier='',
        variable = None,
        hookupFn=None,
        priority=0,
        subpriority = 0,
        doc = None,
        ):
        self.variable = variable or IngScr_Variable()
        super().__init__(
            identifier=identifier, 
            structureType=GrammarStructure.NOUN,
            valueFn=VariablePhrase.getVariable, 
            hookupFn=hookupFn, 
            priority=priority,
            subpriority = subpriority,
            doc = doc,
            )
    def getVariable(self):
        return self.variable
# A Static phrase that returns a constant.
# autogenerate value fn and "return" doc if there isn't one.
# Sometimes a cast only takes constant phrases.
class ConstantPhrase(StaticPhrase):
    def __init__(
        self, 
        identifier='', 
        structureType=GrammarStructure.NOUN, 
        value = None,
        priority=0, 
        subpriority=0,
        doc = None,
        ):
        self.value = value
        super().__init__(
            identifier=identifier, 
            structureType=structureType, 
            valueFn=self.__class__.getValue, 
            priority=priority, 
            subpriority=subpriority,
            doc = doc
            )
        if not "return" in self.doc:
            self.doc["return"] = str(self.value) if not isinstance(self.value,str) else '"'+ self.value +'"'
    def getValue(self):
        return self.value
# A phrase that returns a number. Autogenerate value if it's literal.
class NumberPhrase(ConstantPhrase):
    def __init__(
        self, 
        identifier='', 
        value = None,
        priority=0,
        subpriority = 0,
        doc = None,
        ):
        super().__init__(
            identifier=identifier, 
            structureType=GMSTR_NOUN, 
            value = value,
            priority=priority,
            subpriority = subpriority,
            doc = doc
        )
        if self.value == None:
            self.value = toNumber(self.identifier)
# A phrase that's a literal string. The value is equal to the identifier.
# Should be treated separately as the rest, because the identiier does not follow normal rules.
class LiteralPhrase(ConstantPhrase):
    def __init__(
        self, 
        identifier='', 
        priority=0, 
        subpriority=0, 
        doc=None
        ):
        super().__init__(
            identifier=identifier, 
            structureType=GMSTR_NOUN, 
            value=identifier, 
            priority=priority, 
            subpriority=subpriority, 
            doc=doc
            )
# A cast object
# Determines what phrases can fill a spot of a dynamic phrase
class Cast:
    def __init__(self, structure, condition = None, tags = None):
        super().__init__()
        # What condition is required
        self.structure = structure
        self.condition = condition
        # Any tags associated with the cast
        # "optional": This cast is optional, and allow Nones.
        self.tags = tags or {}
    def __repr__(self):
        return "Cast for " + self.structure.name
    # Can cast a grammartreenode into this cast.
    def canCast(self, toCheck):
        if self.structure != toCheck.value.structureType:
            return False
        if self.condition and not self.condition(self, toCheck):
            return False
        return "optional" in self.tags or toCheck != None
    def autoDescription(self):
        return ("An " if isVowel(self.structure.name[0]) else "A ") + self.structure.name.lower()
# A dynamic phrase, as opposed to a static phrase, requires 1 or more parameters.
# For example, "Create ... called ..."
class DynamicPhrase(SentencePiece):
    def __init__(
        self, 
        identifier='', 
        structureType=GrammarStructure.NOUN, 
        requiredCasts = [], 
        valueFn = None, 
        hookupFn = None,
        priority=0,
        subpriority = 0,
        doc = None,
        ):
        super().__init__(identifier, structureType, valueFn, hookupFn, priority, subpriority, doc,)
        # Any cast required for the phrase. A list of casts. In the list also accepts GrammarStructure
        # Enums to simplify things a bit.
        # Right now, switching the cast string can break things.
        self.requiredCasts = requiredCasts
        for i in range(len(self.requiredCasts)):
            if isinstance(self.requiredCasts[i], GrammarStructure):
                self.requiredCasts[i] = Cast(self.requiredCasts[i])
    # def matchPattern(self, tokens, allowCapitalization=True):
    #     def isCast(string):
    #         return string[0] == "{" and string[-1] == "}"
    #     components = self.identifier.split(" ")
    #     for word in components:
    #         if isCast(word):
    #             pass
    #         else:
    #             pass
    #     return True
    def splitPatterns(self):
        identifiers = self._splitPatternCache
        if identifiers == None:
            identifiers = self.identifier.split(" ")
            for i in range(len(identifiers)):
                identifierString = identifiers[i]
                if isCastStr(identifierString):
                    index = int(identifierString[1:-1])
                    identifiers[i] = self.requiredCasts[index]
            self._splitPatternCache = identifiers
        return identifiers
    # Number of casts.
    @property
    def totalCasts(self):
        pattern = self.splitPatterns()
        returnVal = 0
        for i in pattern:
            if isinstance(i, Cast):
                returnVal += 1
        return returnVal
    def generateCastStrings(self):
        existingVal = []
        returnVal = []
        if "argName" in self.doc:
            existingVal = self.doc['argName']
        for i in range(len(self.requiredCasts)):
            if i >= len(existingVal) or existingVal[i] == None:
                structureName = self.requiredCasts[i].structure.name
                if not structureName in returnVal:
                    returnVal.append(structureName)
                    continue
                subscript = 2
                while (structureName + str(subscript)) in returnVal:
                    subscript += 1
                returnVal.append((structureName + str(subscript)))
            else:
                returnVal.append(existingVal[i])
        return returnVal
    def processDocString(self, stringToProcess):
        returnVal = super().processDocString(stringToProcess)
        castStrs = self.generateCastStrings()
        for i in range(len(self.requiredCasts)):
            returnVal = returnVal.replace("{" + str(i) + "}", "{" + castStrs[i] + "}")
        return returnVal
# A tracker that tracks what phrase a dynamicphrase is on. Is not a sentence piece, but 
# has methods that are the same as sentence piece.
# has different function for splitpattern, but otherwise same methods.
class PhraseTracker:
    def __init__(self, parentPhrase, phraseNum = 0):
        super().__init__()
        assert(parentPhrase.totalCasts >= phraseNum)
        self.parentPhrase = parentPhrase
        self.phraseNum = phraseNum
        self._splitPatternCache = self.parentPhrase.splitPatterns().copy()
        casters = 0
        while casters < self.phraseNum:
            if isinstance(self._splitPatternCache[0], Cast):
                casters += 1
            self._splitPatternCache.pop(0)
    @property
    def identifier(self): return self.parentPhrase.identifier
    def splitPatterns(self): return self._splitPatternCache
    def getNextTracker(self): 
        try:
            return PhraseTracker(self.parentPhrase, self.phraseNum + 1)
        except:
            return None
    def __repr__(self):
        return "{}({} in)".format(self.parentPhrase, self.phraseNum)
    def __lt__(self, value):
        if isinstance(value, SentencePiece):
            return self.parentPhrase < value
        elif isinstance(value,PhraseTracker):
            return self.parentPhrase < value.parentPhrase
        return False
# class ParsedResult:
#     def __init__(self, base, *params):
#         self.base = base
#         self.params = params
# A GrammarTreeNodes represents a compiled sentence(or sentence piece) that can be called for value.
class GrammarTreeNode(TreeNode):
    def __init__(self, value, children=None, parent=None):
        super().__init__(value, children=children, parent=parent)
        assert value == None or isinstance(value, SentencePiece), "{} is not a SentencePiece".format(self.value)
        for i in self.children:
            assert isinstance(i, GrammarTreeNode), "{} is not a SentencePiece".format(i.value)
    # The structure of self
    @property
    def structureType(self):
        if self.value:
            return self.value.structureType
        return None
    # Get the raw value, which if it is a reference(IngScr_Variable), returns the reference instead of
    # the value.
    def getRawValue(self):
        if self.value and self.value.valueFn:
            return self.value.valueFn(self.value,*self.children)
        return None
    # When called, recursively calls the hookupFn in self and its children.
    def onHookup(self):
        if self.value and callable(self.value.hookupFn):
            self.value.hookupFn(self.value, *self.children)
        for child in self.children:
            child.onHookup()
    # Allow value to reference self
    def assignSentenceLabelToValue(self):
        self.value.sentence = self
        for i in self.children:
            i.assignSentenceLabelToValue()
        return self

    def assignGotoLabel(self, label):
        self.gotoLabel = label
    # Automatically pass by value instead of reference
    # Gets the value of things
    def __call__(self):
        returnval = self.getRawValue()
        if isinstance(returnval, IngScr_Variable):
            returnval = returnval.value
        return returnval
# This just simplify things by creating aliases of existing phrases. Should never been instantiated
class AliasPiece(SentencePiece):
    def __new__(cls, newIdentifier, oldStructure):
        returnVal = copy(oldStructure)
        returnVal.doc = returnVal.doc.copy()
        returnVal.identifier = newIdentifier
        if "alias" in returnVal.doc:
            returnVal.doc.pop("alias")
        returnVal.doc["aliasOf"] = oldStructure
        return returnVal
    def __init__(self, newIdentifier,  oldStructure):
        raise NotImplementedError("cannot instantiate instance of aliaspiece")
# A block of actions. Stores a bunch of actions and execute them
class ActionBlock:
    # The label to jump to.
    gotoThisLabel = None
    def __init__(self, sentences = None):
        self.sentences = sentences or []
        self.gotoLabelDict = {}
        for i in range(len(self.sentences)):
            if hasattr(self.sentences[i], "gotoLabel") and self.sentences[i].gotoLabel != None:
                gotoLabel = self.sentences[i].gotoLabel
                assert not gotoLabel in self.gotoLabelDict
                self.gotoLabelDict[gotoLabel] = i
    # Executes its action one by one, unless interrupted by labels.
    def __call__(self):
        from pattern_storage import PatternDictionary
        oldScope = PatternDictionary.currentScope
        self.scope.updateScopeToSelf()
        self.currentLine = 0
        while self.currentLine < len(self.sentences):
            if ActionBlock.gotoThisLabel != None:
                if ActionBlock.gotoThisLabel in self.gotoLabelDict:
                    self.currentLine = self.gotoLabelDict[ActionBlock.gotoThisLabel]
                    ActionBlock.gotoThisLabel = None
                else:
                    PatternDictionary.currentScope = oldScope
                    return
            self.sentences[self.currentLine]()
            self.currentLine += 1
        PatternDictionary.currentScope = oldScope
    @classmethod
    def goto(cls, label):
        cls.gotoThisLabel = label
if __name__ == "__main__":
    testPattern = DynamicPhrase("{0} plus {1}", requiredCasts=[Cast(GrammarStructure.NOUN), Cast(GrammarStructure.NOUN)])
    testtracker = PhraseTracker(testPattern, 2)
    print(testPattern.splitPatterns())
    print(testtracker.splitPatterns())