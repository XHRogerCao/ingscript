from inspect import isclass
class IngScr_Variable:
    def __init__(self, value = None, vartype = None, getterFn = None, setterFn = None):
        super().__init__()
        self.varType = vartype
        self.getterFn = getterFn
        self.setterFn = setterFn
        if setterFn == None:
            self.value = value
        
        #print(self.__dict__)
    @property
    def value(self):
        if callable(self.getterFn):
            return self.getterFn(self)
        else:
            return self.__value
    @value.setter
    def value(self, val):
        if isclass(self.varType) and self.varType != IngScr_Variable and val != None:
            val = self.varType(val)
        assert self.validateValue(val), "Invalid value to assign"
        if callable(self.setterFn):
            self.setterFn(self, val)
        else:
            self.__value = val
    def validateValue(self, value):
        if self.varType == None or self.varType == IngScr_Variable:
            return True
        if isclass(self.varType):
            return value == None or isinstance(value, self.varType)
        return False