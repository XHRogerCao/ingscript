from pattern_storage import *

# Documentation usage:
# "desc": The description of the expression.
# "argument": A list, each item describes the argument
# "argName": The name of the argument
# "return": The description of the return value
# "alias": Aliases associated with this identifier. A list
# "aliasOf": What this alias is an alias of

# Generate a string for documentation. This is in markdown, btw.
def generateDocString(scopeName = ""):
    returnStr = []
    for scope in PatternDictionary.dictionaries:
        if len(scope) >= len(scopeName) and scope[:len(scopeName)] == scopeName:
            currentStr = ""
            currentStr += "## {}\n\n".format(scope if scope != "" else "(global)")
            currentDict =  PatternDictionary.dictionaries[scope]
            for key in currentDict.dictionary:
                for entry in currentDict.dictionary[key]:
                    currentStr += "### " + entry.processDocString(entry.identifier.title()) + "\n\n```text\n"
                    currentStr += entry.generateDocumentation()
                    currentStr += "```\n\n"
            returnStr.append((scope, currentStr))
    returnStr.sort()
    actualReturnString = "# Documentation\n\n"
    for i in returnStr:
        actualReturnString += i[1] + "\n"
    return actualReturnString
def generateDocFile(scopeName = "", filename = "DOCUMENTATION"):
    f = open(filename + ".md","w")
    f.write(generateDocString(scopeName))
    f.close()