# A list of punctuations recognized by the tokenizer. Characters in this string is treated as a punctuation,
# And characters outside of this list is treated as a normal character
punctuations = "!#$%&'(-)*+,./:;<=>?@[\]^`{|}~"
# A list of characters that belong in a hexadecimal.
allowedHexadecimals = "0123456789abcdefABCDEF"
# A mapping for escape characters and what they represents.
escape_map = {
    "n": "\n",
    "t": "\t",
    "\\": "\\",
    "\"": "\"",
}

childValueFn = lambda self, a: a.getRawValue()

PRIORITY_LOWEST = -999999

numberConst = ['zero','one','two','three','four','five','six','seven','eight','nine']
numberConstTeens = ['ten','eleven','twelve','thirteen','fourteen','fifteen',
'sixteen','seventeen','eighteen','nineteen']
numberConstTens = [None, None, 'twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']

# Check if two string is equivalent in english.
# First letter is not case sensitive, while the rest are.
# That's probably because the capitalization rule at the beginning of the sentence, and i don't intend to
# remove this rule.
def equalInEnglish(str1, str2):
    if len(str1) > 1 and len(str2) > 1:
        return str1[0].lower() == str2[0].lower() and str1[1:] == str2[1:]
    return str1 == str2
# Check if something is a tuple or a list.
def isAList(obj):
    return isinstance(obj,(tuple, list))
def removeTitleCase(str1):
    if len(str1) >= 2:
        return str1[0].lower() + str1[1:]

    return str1.lower()
def isCastStr(identifierString):
    return len(identifierString) >= 3 and identifierString[0] == "{" and identifierString[-1] == "}" and identifierString[1:-1].isdigit()
def isVowel(char):
    return char.lower() in "aeiou"
def toNumber(num):
    try:
        return int(num)
    except:
        try:
            return float(num)
        except:
            raise ValueError("Fail to cast as number: " + str(num))
def getDefaultValueForType(typeVal):
    if typeVal == int:
        return 0
    return None
class UnicodeList:
    def __init__(self, lowerBound = None, upperBound = None):
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        if isinstance(self.lowerBound, str):
            self.lowerBound = ord(self.lowerBound)
        if isinstance(self.upperBound, str):
            self.upperBound = ord(self.upperBound)
        if self.lowerBound == None:
            self.lowerBound = 0
        if self.upperBound == None:
            self.upperBound = 0x10ffff
        self.reversed = False
        assert self.lowerBound <= self.upperBound
    def __getitem__(self, key):
        return chr(key)
    @classmethod
    def universal(cls):
        if not hasattr(cls,"_UnicodeList__universal"):
            cls.__universal = UnicodeList()
        return cls.__universal
    def __len__(self):
        return self.upperBound - self.lowerBound + 1
    def __contains__(self, item):
        return ord(item) >= self.lowerBound and ord(item) <= self.upperBound
    def __reverse__(self):
        self.reversed = not self.reversed
    def __iter__(self):
        if self.reversed:
            self.iterIndex = self.upperBound
        else:
            self.iterIndex = self.lowerBound
        return self
    def __next__(self):
        iterIndex = self.iterIndex
        if iterIndex < self.lowerBound or iterIndex > self.upperBound:
            raise StopIteration
        if self.reversed:
            self.iterIndex -= 1
        else:
            self.iterIndex += 1
        return chr(self.iterIndex)
if __name__ == "__main__":
    test = UnicodeList.universal()
    test2 = UnicodeList.universal()
    print(test, test2)