# The core library.
# All the essential phrases are defined here.

import sys
sys.path.append(".")
from pattern_storage import *
from grammar import *
from constants import *
from numbers import Number
from documentation import *

# The global dictionary for all the base stuff.
globalDict = PatternDictionary()
# --------------------------------------------------------------------
# Input/Output
# --------------------------------------------------------------------
def askForInput(self, var):
    result = input()
    var.getRawValue().value = result
    return result
globalDict.addEntries(
    DynamicPhrase(
        "print {0}", 
        GMSTR_SENTENCE, 
        [Cast(GMSTR_NOUN)], 
        lambda self, a: print(a(), end = ""),
        doc = {
            "desc": "Print the value specified by {0}"
        }
    ),
    DynamicPhrase(
        "input {0}",
        GMSTR_SENTENCE,

        [GMSTR_NOUN],
        askForInput,
        doc={
            "desc":"ask for a input and assign it to a value",
            "argument":[
                "A noun representing a variable"
            ],
            "return": "The input result"
        }
    )
    
)
# --------------------------------------------------------------------
# Variable assignment and initialization.
# --------------------------------------------------------------------
def createVariable(self, varType, varIdentifier, initValue = None):
    newVar = IngScr_Variable(initValue, varType)
    newPhrase = VariablePhrase(
        varIdentifier,
        newVar
    )
    if self.scope != None:
        self.scope.addEntry(
            newPhrase
        )
    self.createdVariable = newVar
    return newVar.value
def createConstant(self, varIdentifier, initValue):
    newPhrase = ConstantPhrase(varIdentifier, value = initValue)
    if self.scope != None:
        self.scope.addEntry(
            newPhrase
        )
    return newPhrase.value
def assignInitValue(self, initValue):
    self.createdVariable.value = initValue
    return self.createdVariable.value
def assignVariableValue(self, var, val):
    tempvar = var.getRawValue()
    assert isinstance(tempvar,IngScr_Variable), "not a variable"
    tempvar.value = val
    return tempvar.value
globalDict.addEntries(
    DynamicPhrase(
        'create a new {0} called {1}',
        GMSTR_SENTENCE,
        [
            Cast(GMSTR_NOUN), 
            Cast(GMSTR_NOUN, lambda self, val: isinstance(val.value, ConstantPhrase)),
        ],
        None,
        lambda self, t, n: createVariable(self, t(), n()),
        doc={
            "desc": "Create a new variable",
            "argument": [
                "A noun that represents the type of variable",
                "A literal string representing the identifier for the variable",
            ],
            "return": "the value of {1} after the initialization"
        }
    ),
    DynamicPhrase(
        'create a new {0} called {1} and initialize it as {2}',
        GMSTR_SENTENCE,
        [
            Cast(GMSTR_NOUN), 
            Cast(GMSTR_NOUN, lambda self, val: isinstance(val.value, ConstantPhrase)),
            GMSTR_NOUN,
        ],
        lambda self, t, n, i: assignInitValue(self, i()),
        lambda self, t, n, i: createVariable(self, t(), n()),
        doc={
            "desc": "Create a new variable with initialization",
            "argument": [
                "A noun that represents the type of variable",
                "A literal string representing the identifier for the variable",
                "A noun that represents the value to assign to {1}"
            ],
            "return": "the value of {1} after the initialization",
            "alias":[
                "create a new {0} called {1} initialized as {2}"
            ],
        }
    ),
    DynamicPhrase(
        'create a new constant called {0} and initialize it as {1}',
        GMSTR_SENTENCE,
        [
            Cast(GMSTR_NOUN, lambda self, val: isinstance(val.value, ConstantPhrase)),
            GMSTR_NOUN,
        ],
        None,
        lambda self, n, i: createConstant(self, n(), i()),
        doc={
            "desc": "Create a new constant",
            "argument": [
                "A literal string representing the identifier for the constant",
                "A noun that represents the value to assign to {0}"
            ],
            "return": "the value of {0} after the initialization",
            "alias":[
                "create a new constant called {0} initialized as {1}"
            ],
        }
    ),
    DynamicPhrase(
        'set {0} to {1}',
        GMSTR_SENTENCE,
        [
            GMSTR_NOUN,
            GMSTR_NOUN,
        ],
        lambda self, var, val: assignVariableValue(self, var, val()),
        doc={
            "desc": "Assign a value to a variable",
            "argument": [
                "A variable(noun) to be asssigned to",
                "A noun that represents the value to assign to {0}"
            ],
            "return": "the value of {0} after the assignment"
        }
    ),
    DynamicPhrase(
        'increase {0} by {1}',
        GMSTR_SENTENCE,
        [
            GMSTR_NOUN,
            GMSTR_NOUN,
        ],
        lambda self, var, val: assignVariableValue(self, var, var() + val()),
        doc={
            "desc": "Increase the value of a variable by another value",
            "argument": [
                "A variable(noun) which the value has \"+\" defined for {1}",
                "A noun that represents the value to increase to {0}"
            ],
            "return": "the value of {0} after the assignment"
        }
    ),
    DynamicPhrase(
        'decrease {0} by {1}',
        GMSTR_SENTENCE,
        [
            GMSTR_NOUN,
            GMSTR_NOUN,
        ],
        lambda self, var, val: assignVariableValue(self, var, var() - val()),
        doc={
            "desc": "Decrease the value of a variable by another value",
            "argument": [
                "A variable(noun) which the value has \"-\" defined for {1}",
                "A noun that represents the value to decrease to {0}"
            ],
            "return": "the value of {0} after the assignment"
        }
    ),
)
# --------------------------------------------------------------------
# Variable Types
# --------------------------------------------------------------------
def convertVariableType(self, toConvert, newType):
    return newType()(toConvert())
globalDict.addEntries(
    ConstantPhrase(
        'variable',
        GMSTR_NOUN,
        IngScr_Variable,
    ),
    ConstantPhrase(
        'integer',
        GMSTR_NOUN,
        int,
    ),
    ConstantPhrase(
        'real number',
        GMSTR_NOUN,
        float,
    ),
    ConstantPhrase(
        'decimal number',
        GMSTR_NOUN,
        float,
    ),
    ConstantPhrase(
        'number',
        GMSTR_NOUN,
        Number,
    ),
    ConstantPhrase(
        'string',
        GMSTR_NOUN,
        str,
    ),
    ConstantPhrase(
        'list',
        GMSTR_NOUN,
        list
    ),
    DynamicPhrase(
        '{0} convert into a/an {1}',
        GMSTR_NOUN,
        [GMSTR_NOUN,GMSTR_NOUN],
    ),
    DynamicPhrase(
        'the number representing {0} in ASCII/Unicode',
        GMSTR_NOUN,
        [GMSTR_NOUN],
        lambda self, a: ord(a())
    )
)
# --------------------------------------------------------------------
# Operations
# --------------------------------------------------------------------
globalDict.addEntries(

    DynamicPhrase(
        "{0} plus {1}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN),Cast(GMSTR_NOUN)],
        lambda self, a, b: a() + b(),
        doc={
            "desc": "Adds two values",
            "argument": ["A noun that has \"+\" defined for {1}"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
    
    DynamicPhrase(
        "{0} minus {1}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN),Cast(GMSTR_NOUN)],
        lambda self, a, b: a() - b(),
        doc={
            "desc": "Subtracts two values",
            "argument": ["A noun that has \"-\" defined for {1}"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
    
    DynamicPhrase(
        "{0} times {1}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN),Cast(GMSTR_NOUN)],
        lambda self, a, b: a() * b(),
        doc={
            "desc": "Multiplies two values",
            "argument": ["A noun that has \"*\" defined for {1}"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
    # Syntax: "{NOUN1} divided by {NOUN2}"
    # Argument:
    #   {NOUN1}: A noun which value has "/" defined for {NOUN2}
    #   {NOUN2}: Another noun
    # Result: Returns the value from {NOUN1} divided by {NOUN2}
    DynamicPhrase(
        "{0} divided by {1}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN),Cast(GMSTR_NOUN)],
        lambda self, a, b: a() / b(),
        doc={
            "desc": "Divides two values",
            "argument": ["A noun that has \"/\" defined for {1}"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
    DynamicPhrase(
        "the quotient of {0} divided by {1}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN),Cast(GMSTR_NOUN)],
        lambda self, a, b: a() // b(),
        doc={
            "desc": "Integer division of two values",
            "argument": ["A noun that has \"//\" defined for {1}"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
    DynamicPhrase(
        "the remainder of {0} divided by {1}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN),Cast(GMSTR_NOUN)],
        lambda self, a, b: a() % b(),
        doc={
            "desc": "Modulo of two values",
            "argument": ["A noun that has \"%\" defined for {1}"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
    DynamicPhrase(
        "{0} to the power of {1}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN),Cast(GMSTR_NOUN)],
        lambda self, a, b: a() ** b(),
        doc={
            "desc": "Exponent of two values",
            "argument": ["A noun that has \"**\" defined for {1}"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
    # Syntax: "negative {NOUN}"
    # Argument:
    #   {NOUN}: A noun which value has "-"(unary) defined
    # Result: Returns the value from negative {NOUN}
    DynamicPhrase(
        "negative {0}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN)],
        lambda self, a: -a(),
        doc={
            "desc": "Arithmetically invert a value",
            "argument": ["A noun that has \"-\"(unary) defined for {1}"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
    DynamicPhrase(
        "- {0}",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN,lambda self, val: isinstance(val.value, NumberPhrase))],
        lambda self, a: -a(),
        doc={
            "desc": "Get the negative of a number",
            "argument": ["A number"],
            "return": "the value of {IDENTIFIER}"
        }
    ),
)
# --------------------------------------------------------------------
# Number Constants
# --------------------------------------------------------------------
for i in range(len(numberConst)):
    if numberConst[i]:
        globalDict.addEntry(NumberPhrase(numberConst[i],i))
for i in range(len(numberConstTeens)):
    if numberConstTeens[i]:
        globalDict.addEntry(NumberPhrase(numberConstTeens[i],i + 10))
for i in range(len(numberConstTens)):
    if numberConstTens[i]:
        globalDict.addEntry(NumberPhrase(numberConstTens[i],i * 10))
globalDict.addEntries(

    DynamicPhrase(
        "{0} - {1}", 
        GMSTR_NOUN,
        [
            Cast(GMSTR_NOUN, lambda self, val: isinstance(val.value, NumberPhrase) and (val.value.identifier in numberConstTens)),
            Cast(GMSTR_NOUN, lambda self, val: isinstance(val.value, NumberPhrase) and (val.value.identifier in numberConst))
        ],
        lambda self, a, b: a() + b(),
        doc={
            "desc": "Represent a two digit number between 21~99. For example, twenty-one, thirty-six.",
            "argument": ["A noun that is a number word that ends with -ty", "A noun that is a number word for 0~9"],
            "return": "the value of {0} + {1}"
        }
    ),
    DynamicPhrase(
        "{0} hundred",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN)],
        lambda self, a: a() * 100,
        doc={
            "desc": "Multiplies a number by a hundred",
            "argument": ["A noun that represents a number"],
            "return": "the value of {0} times a hundred"
        }
    ),
    DynamicPhrase(
        "{0} thousand",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN)],
        lambda self, a: a() * 1000,
        doc={
            "desc": "Multiplies a number by a thousand",
            "argument": ["A noun that represents a number"],
            "return": "the value of {0} times a thousand"
        }
    ),
    DynamicPhrase(
        "{0} million",
        GMSTR_NOUN,
        [Cast(GMSTR_NOUN)],
        lambda self, a: a() * 1000000,
        doc={
            "desc": "Multiplies a number by a million",
            "argument": ["A noun that represents a number"],
            "return": "the value of {0} times a million"
        }
    ),
)
# --------------------------------------------------------------------
# Boolean and Conditions
# --------------------------------------------------------------------
def ifStatement(self, condition, trueAction, falseAction = None):
    if condition and condition():
        if trueAction: trueAction()
    else:
        if falseAction: falseAction()
def whileLoop(self, condition, action):
    while condition and condition():
        if action: action()
        if ActionBlock.gotoThisLabel != None:
            return
globalDict.addEntries(
    ConstantPhrase(
        'true',
        GMSTR_SENTENCE,
        True,
    ),
    ConstantPhrase(
        'false',
        GMSTR_SENTENCE,
        False
    ),
    ConstantPhrase(
        'true',
        GMSTR_NOUN,
        True,
    ),
    ConstantPhrase(
        'false',
        GMSTR_NOUN,
        False
    ),
    DynamicPhrase(
        'whether {0}',
        GMSTR_NOUN,
        [GMSTR_SENTENCE],
        childValueFn
    ),
    # Syntax: "{NOUN1} is equal to {NOUN2}"
    # Argument:
    #   {NOUN1}: A noun which value has "==" defined for {NOUN2}
    #   {NOUN2}: Another noun
    # Result: Returns whether {NOUN1} is equal to {NOUN2}
    DynamicPhrase(
        '{0} is equal to {1}',
        GMSTR_SENTENCE,
        [Cast(GMSTR_NOUN), Cast(GMSTR_NOUN)],
        lambda self,a,b: a() == b(),
        doc={
            "desc": "Compare two values's equality",
            "argument": ["A noun that has \"==\" defined for {1}"],
            "return": "whether {IDENTIFIER}",
            "alias":["{0} equals {1}"],
        }
    ),
    # Syntax: "{NOUN1} is not equal to {NOUN2}"
    # Argument:
    #   {NOUN1}: A noun which value has "!=" defined for {NOUN2}
    #   {NOUN2}: Another noun
    # Result: Returns whether {NOUN1} is not equal to {NOUN2}
    DynamicPhrase(
        '{0} is not equal to {1}',
        GMSTR_SENTENCE,
        [Cast(GMSTR_NOUN), Cast(GMSTR_NOUN)],
        lambda self,a,b: not a() == b(),
        doc={
            "desc": "Compare two values's equality",
            "argument": ["A noun that has \"==\" defined for {1}"],
            "return": "whether {IDENTIFIER}",
            "alias":["{0} does not equal {1}"]
        }
    ),
    DynamicPhrase(
        '{0} is the same as {1}',
        GMSTR_SENTENCE,
        [Cast(GMSTR_NOUN), Cast(GMSTR_NOUN)],
        lambda self,a,b: a() is b(),
        doc={
            "desc": "Compare two values's identity",
            "return": "whether {IDENTIFIER}"
        }
    ),
    DynamicPhrase(
        '{0} is not the same as {1}',
        GMSTR_SENTENCE,
        [Cast(GMSTR_NOUN), Cast(GMSTR_NOUN)],
        lambda self,a,b: not a() is b(),
        doc={
            "desc": "Compare two values's identity",
            "return": "whether {IDENTIFIER}"
        }
    ),
    # Syntax: "{NOUN1} is less than {NOUN2}"
    # Argument:
    #   {NOUN1}: A noun which value has "<" defined for {NOUN2}
    #   {NOUN2}: Another noun
    # Result: Returns whether {NOUN1} is less than {NOUN2}
    DynamicPhrase(
        '{0} is less/smaller than {1}',
        GMSTR_SENTENCE,
        [Cast(GMSTR_NOUN), Cast(GMSTR_NOUN)],
        lambda self,a,b: a() < b(),
        doc={
            "desc": "Compare two values's size",
            "argument": ["A noun that has \"<\" defined for {1}"],
            "return": "whether {IDENTIFIER}"
        }
    ),
    # Syntax: "{NOUN1} is greater than {NOUN2}"
    # Argument:
    #   {NOUN1}: A noun which value has ">" defined for {NOUN2}
    #   {NOUN2}: Another noun
    # Result: Returns whether {NOUN1} is greater than {NOUN2}
    DynamicPhrase(
        '{0} is greater/larger than {1}',
        GMSTR_SENTENCE,
        [Cast(GMSTR_NOUN), Cast(GMSTR_NOUN)],
        lambda self,a,b: a() > b(),
        doc={
            "desc": "Compare two values's size",
            "argument": ["A noun that has \">\" defined for {1}"],
            "return": "whether {IDENTIFIER}"
        }
    ),
    DynamicPhrase(
        '{0} is less/smaller than or equal to {1}',
        GMSTR_SENTENCE,
        [Cast(GMSTR_NOUN), Cast(GMSTR_NOUN)],
        lambda self,a,b: a() <= b(),
        doc={
            "desc": "Compare two values's size",
            "argument": ["A noun that has \"<=\" defined for {1}"],
            "return": "whether {IDENTIFIER}"
        }
    ),
    DynamicPhrase(
        '{0} is greater/larger than or equal to {1}',
        GMSTR_SENTENCE,
        [Cast(GMSTR_NOUN), Cast(GMSTR_NOUN)],
        lambda self,a,b: a() >= b(),
        doc={
            "desc": "Compare two values's size",
            "argument": ["A noun that has \">=\" defined for {1}"],
            "return": "whether {IDENTIFIER}"
        }
    ),
    DynamicPhrase(
        'if {0} , {1}',
        GMSTR_SENTENCE,
        [GMSTR_SENTENCE,GMSTR_SENTENCE],
        ifStatement,
        doc={
            "desc": "Do something if a condition is true",
            "argName":["CONDITION","TRUE_ACTION"],
            "argument": [
                "A sentence that returns a boolean",
                "A sentence that will be executed when {0} is true"
            ]
        }
    ),
    DynamicPhrase(
        'if {0} , {1} ; otherwise/else , {2}',
        GMSTR_SENTENCE,
        [GMSTR_SENTENCE,GMSTR_SENTENCE, GMSTR_SENTENCE],
        ifStatement,
        doc={
            "desc": "Do something if a condition is true, and do another action if the condition is false",
            "argName":["CONDITION","TRUE_ACTION", "FALSE_ACTION"],
            "argument": [
                "A sentence that returns a boolean",
                "A sentence that will be executed when {0} is true",
                "A sentence that will be executed when {0} is false",
            ]
        }
    ),
    DynamicPhrase(
        'while {0} , {1}',
        GMSTR_SENTENCE,
        [GMSTR_SENTENCE,GMSTR_SENTENCE],
        whileLoop,
        doc={
            "desc": "Repeating something when the condition is true",
            "argName":["CONDITION","ACTION"],
            "argument": [
                "A sentence that returns a boolean",
                "A sentence that will be executed when {0} is true"
            ]
        }
    ),
)
# --------------------------------------------------------------------
# List & iterable operations
# --------------------------------------------------------------------
def createRefToListItem(self, iterable, n):
    def setterFn(self, val):
        iterable[n] = val
        return iterable[n]
    return IngScr_Variable(
        getterFn = lambda self: iterable[n],
        setterFn = setterFn
    )
globalDict.addEntries(
    DynamicPhrase(
        'a list with a size of {0}',
        GMSTR_NOUN,
        [GMSTR_NOUN],
        lambda self, n: [None] * n()
    ),
    DynamicPhrase(
        'the value of {0} at index {1}',
        GMSTR_NOUN,
        [GMSTR_NOUN,GMSTR_NOUN],
        lambda self, a, n: createRefToListItem(self, a(), n()),
        doc={
            "desc":"Access an item with key",
            "argName":["LIST","KEY"],
            "return":"{IDENTIFIER}"
        }
    ),
    ConstantPhrase(
        'the list of ASCII/Unicode',
        GMSTR_NOUN,
        UnicodeList.universal(),
        doc={
            "desc":"Returns a \"list\" of Unicode characters that can be accessed with a key",
            "alias":["the ASCII/Unicode list"],
            "return":"A list of Unicode characters"
        }
    ),
    DynamicPhrase(
        '{0} is in {1}',
        GMSTR_SENTENCE,
        [GMSTR_NOUN,GMSTR_NOUN],
        lambda self, val, iterable: val() in iterable(),
        doc={
            "desc":"Check whether something is in an iterable",
            "argName":["ITEM","ITERABLE"],
            "return":"Whether {IDENTIFIER}"
        }
    )
)
# --------------------------------------------------------------------
# Strings
# --------------------------------------------------------------------
globalDict.addEntries(
    ConstantPhrase('new line',GMSTR_NOUN,'\n',doc={"alias":["a new line"]})
)
# --------------------------------------------------------------------
# Misc
# --------------------------------------------------------------------
def mergeList(a, b):
    endlist = []
    if isinstance(a, list):
        endlist.extend(a)
    else:
        endlist.append(a)
    if isinstance(b, list):
        endlist.extend(b)
    else:
        endlist.append(b)
    return endlist
def executeAction(self, action):
    result = action()
    if callable(result):
        return result()
    return result
def generateAction(self, actionString):
    if not hasattr(self, "actionCache"):
        self.actionCache = {}
    parsedString = actionString()
    if not parsedString in self.actionCache:
        action = PatternDictionary.parseActionBlock(parsedString)
        self.actionCache[parsedString] = action
        return action
    else:
        return self.actionCache[parsedString]
globalDict.addEntries(
    DynamicPhrase(
        '{0} , {1}',
        GMSTR_NOUN,
        [GMSTR_NOUN,GMSTR_NOUN],
        lambda self,a,b: mergeList(a(),b())
    ),
    DynamicPhrase(
        '{0} , {1}',
        GMSTR_SENTENCE,
        [GMSTR_SENTENCE,GMSTR_SENTENCE],
        lambda self,a,b: mergeList(a(),b())
    ),
    DynamicPhrase(
        'the action {0}',
        GMSTR_NOUN,
        [GMSTR_NOUN],
        generateAction,
        doc={
            "desc":"Parses a string into an IngScript code",
            "argument":["A string noun that represents the IngScript code to parse"]
        }
    ),
    DynamicPhrase(
        'execute {0}',
        GMSTR_SENTENCE,
        [GMSTR_NOUN],
        executeAction,
        doc={
            "desc":"Executes an action",
            "argName":["ACTION"],
            "argument":["A noun representing an action"]
        }
    ),
    StaticPhrase(
        'do nothing',
        GMSTR_SENTENCE,
        doc={
            "desc":"A placeholder for when a sentence is needed, but nothing should run"
        }
    ),
    ConstantPhrase(
        'none',
        GMSTR_NOUN,
        None,
        doc={
            "alias":["null", "nil"]
        }
    ),
    DynamicPhrase(
        'step {0} , {1}',
        GMSTR_SENTENCE,
        [
            Cast(GMSTR_NOUN, lambda self, val: isinstance(val.value, ConstantPhrase)),
            GMSTR_SENTENCE
        ],
        lambda self, label, sentence: sentence.getRawValue(),
        lambda self, label, sentence: self.sentence.assignGotoLabel(label()),
        doc={
            "desc":"Label a step as a constant",
            "argName":["LABEL", "ACTION"],
            "argument":[
                "A constant noun representing the identifier of the label",
                "A sentence associated with the label"
            ]
        }
    ),
    DynamicPhrase(
        'go to step {0}',
        GMSTR_SENTENCE,
        [GMSTR_NOUN],
        lambda self, gotoVal: ActionBlock.goto(gotoVal()),
        doc={
            "desc":"Jump to a label. Some say it's a sh!t practice, " +
            "but haters are going to hate, and there's nothing I can do about it. How else am I supposed " +
            "to make it \"Turing complete\" with the time given?",
            "argName":["LABEL"],
            "argument":[
                "A constant noun representing the identifier of the label"
            ]
        }
    )
)
if __name__ == "__main__":
    # print(globalDict.dictionary)
    # generateDocFile()
    result = PatternDictionary.parseActionBlock(
        r"""
        Create a new variable called "test list" and initialize it as a list with a size of 8.
        Set the value of test list at index 0 to 8.
        Print the value of test list at index 0.
        Print a new line.
        Increase the value of test list at index 0 by 5.
        Print the value of test list at index 0.
        """,False
    )
    result()