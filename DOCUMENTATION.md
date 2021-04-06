# Documentation

## (global)

### Print {NOUN}

```text
Syntax: "print {NOUN}".
Type: Sentence.
Description: Print the value specified by {NOUN}.
Arguments:
    {NOUN}: A noun.
```

### Input {NOUN}

```text
Syntax: "input {NOUN}".
Type: Sentence.
Description: ask for a input and assign it to a value.
Arguments:
    {NOUN}: A noun representing a variable.
Returns: The input result.
```

### Create A New Constant Called {NOUN} And Initialize It As {NOUN2}

```text
Syntax: "create a new constant called {NOUN} and initialize it as {NOUN2}".
Alias(es): create a new constant called {NOUN} initialized as {NOUN2}.
Type: Sentence.
Description: Create a new constant.
Arguments:
    {NOUN}: A literal string representing the identifier for the constant.
    {NOUN2}: A noun that represents the value to assign to {NOUN}.
Returns: the value of {NOUN} after the initialization.
```

### Create A New {NOUN} Called {NOUN2} And Initialize It As {NOUN3}

```text
Syntax: "create a new {NOUN} called {NOUN2} and initialize it as {NOUN3}".
Alias(es): create a new {NOUN} called {NOUN2} initialized as {NOUN3}.
Type: Sentence.
Description: Create a new variable with initialization.
Arguments:
    {NOUN}: A noun that represents the type of variable.
    {NOUN2}: A literal string representing the identifier for the variable.
    {NOUN3}: A noun that represents the value to assign to {NOUN2}.
Returns: the value of {NOUN2} after the initialization.
```

### Create A New Constant Called {NOUN} Initialized As {NOUN2}

```text
Syntax: "create a new constant called {NOUN} initialized as {NOUN2}".
Type: Sentence.
Description: Create a new constant.
Arguments:
    {NOUN}: A literal string representing the identifier for the constant.
    {NOUN2}: A noun that represents the value to assign to {NOUN}.
Returns: the value of {NOUN} after the initialization.
```

### Create A New {NOUN} Called {NOUN2} Initialized As {NOUN3}

```text
Syntax: "create a new {NOUN} called {NOUN2} initialized as {NOUN3}".
Type: Sentence.
Description: Create a new variable with initialization.
Arguments:
    {NOUN}: A noun that represents the type of variable.
    {NOUN2}: A literal string representing the identifier for the variable.
    {NOUN3}: A noun that represents the value to assign to {NOUN2}.
Returns: the value of {NOUN2} after the initialization.
```

### Create A New {NOUN} Called {NOUN2}

```text
Syntax: "create a new {NOUN} called {NOUN2}".
Type: Sentence.
Description: Create a new variable.
Arguments:
    {NOUN}: A noun that represents the type of variable.
    {NOUN2}: A literal string representing the identifier for the variable.
Returns: the value of {NOUN2} after the initialization.
```

### Set {NOUN} To {NOUN2}

```text
Syntax: "set {NOUN} to {NOUN2}".
Type: Sentence.
Description: Assign a value to a variable.
Arguments:
    {NOUN}: A variable(noun) to be asssigned to.
    {NOUN2}: A noun that represents the value to assign to {NOUN}.
Returns: the value of {NOUN} after the assignment.
```

### Increase {NOUN} By {NOUN2}

```text
Syntax: "increase {NOUN} by {NOUN2}".
Type: Sentence.
Description: Increase the value of a variable by another value.
Arguments:
    {NOUN}: A variable(noun) which the value has "+" defined for {NOUN2}.
    {NOUN2}: A noun that represents the value to increase to {NOUN}.
Returns: the value of {NOUN} after the assignment.
```

### Decrease {NOUN} By {NOUN2}

```text
Syntax: "decrease {NOUN} by {NOUN2}".
Type: Sentence.
Description: Decrease the value of a variable by another value.
Arguments:
    {NOUN}: A variable(noun) which the value has "-" defined for {NOUN2}.
    {NOUN2}: A noun that represents the value to decrease to {NOUN}.
Returns: the value of {NOUN} after the assignment.
```

### Variable

```text
Syntax: "variable".
Type: Noun.
Description: A phrase that returns variable.
Returns: <class 'variables.IngScr_Variable'>.
```

### Integer

```text
Syntax: "integer".
Type: Noun.
Description: A phrase that returns integer.
Returns: <class 'int'>.
```

### Real Number

```text
Syntax: "real number".
Type: Noun.
Description: A phrase that returns real number.
Returns: <class 'float'>.
```

### Decimal Number

```text
Syntax: "decimal number".
Type: Noun.
Description: A phrase that returns decimal number.
Returns: <class 'float'>.
```

### Number

```text
Syntax: "number".
Type: Noun.
Description: A phrase that returns number.
Returns: <class 'numbers.Number'>.
```

### String

```text
Syntax: "string".
Type: Noun.
Description: A phrase that returns string.
Returns: <class 'str'>.
```

### List

```text
Syntax: "list".
Type: Noun.
Description: A phrase that returns list.
Returns: <class 'list'>.
```

### {NOUN} Convert Into A/An {NOUN2}

```text
Syntax: "{NOUN} convert into a/an {NOUN2}".
Type: Noun.
Description: A phrase that returns {NOUN} convert into a/an {NOUN2}.
Arguments:
    {NOUN}: A noun.
    {NOUN2}: A noun.
```

### The List Of Ascii/Unicode

```text
Syntax: "the list of ASCII/Unicode".
Alias(es): the ASCII/Unicode list.
Type: Noun.
Description: Returns a "list" of Unicode characters that can be accessed with a key.
Returns: A list of Unicode characters.
```

### The Ascii/Unicode List

```text
Syntax: "the ASCII/Unicode list".
Type: Noun.
Description: Returns a "list" of Unicode characters that can be accessed with a key.
Returns: A list of Unicode characters.
```

### The Number Representing {NOUN} In Ascii/Unicode

```text
Syntax: "the number representing {NOUN} in ASCII/Unicode".
Type: Noun.
Description: A phrase that returns the number representing {NOUN} in ASCII/Unicode.
Arguments:
    {NOUN}: A noun.
```

### The Remainder Of {NOUN} Divided By {NOUN2}

```text
Syntax: "the remainder of {NOUN} divided by {NOUN2}".
Type: Noun.
Description: Modulo of two values.
Arguments:
    {NOUN}: A noun that has "%" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: the value of the remainder of {NOUN} divided by {NOUN2}.
```

### The Quotient Of {NOUN} Divided By {NOUN2}

```text
Syntax: "the quotient of {NOUN} divided by {NOUN2}".
Type: Noun.
Description: Integer division of two values.
Arguments:
    {NOUN}: A noun that has "//" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: the value of the quotient of {NOUN} divided by {NOUN2}.
```

### The Value Of {LIST} At Index {KEY}

```text
Syntax: "the value of {LIST} at index {KEY}".
Type: Noun.
Description: Access an item with key.
Arguments:
    {LIST}: A noun.
    {KEY}: A noun.
Returns: the value of {LIST} at index {KEY}.
```

### The Action {NOUN}

```text
Syntax: "the action {NOUN}".
Type: Noun.
Description: Parses a string into an IngScript code.
Arguments:
    {NOUN}: A string noun that represents the IngScript code to parse.
```

### {NOUN} Plus {NOUN2}

```text
Syntax: "{NOUN} plus {NOUN2}".
Type: Noun.
Description: Adds two values.
Arguments:
    {NOUN}: A noun that has "+" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: the value of {NOUN} plus {NOUN2}.
```

### {NOUN} Minus {NOUN2}

```text
Syntax: "{NOUN} minus {NOUN2}".
Type: Noun.
Description: Subtracts two values.
Arguments:
    {NOUN}: A noun that has "-" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: the value of {NOUN} minus {NOUN2}.
```

### {NOUN} Times {NOUN2}

```text
Syntax: "{NOUN} times {NOUN2}".
Type: Noun.
Description: Multiplies two values.
Arguments:
    {NOUN}: A noun that has "*" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: the value of {NOUN} times {NOUN2}.
```

### {NOUN} Divided By {NOUN2}

```text
Syntax: "{NOUN} divided by {NOUN2}".
Type: Noun.
Description: Divides two values.
Arguments:
    {NOUN}: A noun that has "/" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: the value of {NOUN} divided by {NOUN2}.
```

### {NOUN} To The Power Of {NOUN2}

```text
Syntax: "{NOUN} to the power of {NOUN2}".
Type: Noun.
Description: Exponent of two values.
Arguments:
    {NOUN}: A noun that has "**" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: the value of {NOUN} to the power of {NOUN2}.
```

### Negative {NOUN}

```text
Syntax: "negative {NOUN}".
Type: Noun.
Description: Arithmetically invert a value.
Arguments:
    {NOUN}: A noun that has "-"(unary) defined for {1}.
Returns: the value of negative {NOUN}.
```

### {NOUN} - {NOUN2}

```text
Syntax: "{NOUN} - {NOUN2}".
Type: Noun.
Description: Represent a two digit number between 21~99. For example, twenty-one, thirty-six.
Arguments:
    {NOUN}: A noun that is a number word that ends with -ty.
    {NOUN2}: A noun that is a number word for 0~9.
Returns: the value of {NOUN} + {NOUN2}.
```

### - {NOUN}

```text
Syntax: "- {NOUN}".
Type: Noun.
Description: Get the negative of a number.
Arguments:
    {NOUN}: A number.
Returns: the value of - {NOUN}.
```

### Zero

```text
Syntax: "zero".
Type: Noun.
Description: A phrase that returns zero.
Returns: 0.
```

### One

```text
Syntax: "one".
Type: Noun.
Description: A phrase that returns one.
Returns: 1.
```

### Two

```text
Syntax: "two".
Type: Noun.
Description: A phrase that returns two.
Returns: 2.
```

### Three

```text
Syntax: "three".
Type: Noun.
Description: A phrase that returns three.
Returns: 3.
```

### Four

```text
Syntax: "four".
Type: Noun.
Description: A phrase that returns four.
Returns: 4.
```

### Five

```text
Syntax: "five".
Type: Noun.
Description: A phrase that returns five.
Returns: 5.
```

### Six

```text
Syntax: "six".
Type: Noun.
Description: A phrase that returns six.
Returns: 6.
```

### Seven

```text
Syntax: "seven".
Type: Noun.
Description: A phrase that returns seven.
Returns: 7.
```

### Eight

```text
Syntax: "eight".
Type: Noun.
Description: A phrase that returns eight.
Returns: 8.
```

### Nine

```text
Syntax: "nine".
Type: Noun.
Description: A phrase that returns nine.
Returns: 9.
```

### Ten

```text
Syntax: "ten".
Type: Noun.
Description: A phrase that returns ten.
Returns: 10.
```

### Eleven

```text
Syntax: "eleven".
Type: Noun.
Description: A phrase that returns eleven.
Returns: 11.
```

### Twelve

```text
Syntax: "twelve".
Type: Noun.
Description: A phrase that returns twelve.
Returns: 12.
```

### Thirteen

```text
Syntax: "thirteen".
Type: Noun.
Description: A phrase that returns thirteen.
Returns: 13.
```

### Fourteen

```text
Syntax: "fourteen".
Type: Noun.
Description: A phrase that returns fourteen.
Returns: 14.
```

### Fifteen

```text
Syntax: "fifteen".
Type: Noun.
Description: A phrase that returns fifteen.
Returns: 15.
```

### Sixteen

```text
Syntax: "sixteen".
Type: Noun.
Description: A phrase that returns sixteen.
Returns: 16.
```

### Seventeen

```text
Syntax: "seventeen".
Type: Noun.
Description: A phrase that returns seventeen.
Returns: 17.
```

### Eighteen

```text
Syntax: "eighteen".
Type: Noun.
Description: A phrase that returns eighteen.
Returns: 18.
```

### Nineteen

```text
Syntax: "nineteen".
Type: Noun.
Description: A phrase that returns nineteen.
Returns: 19.
```

### Twenty

```text
Syntax: "twenty".
Type: Noun.
Description: A phrase that returns twenty.
Returns: 20.
```

### Thirty

```text
Syntax: "thirty".
Type: Noun.
Description: A phrase that returns thirty.
Returns: 30.
```

### Forty

```text
Syntax: "forty".
Type: Noun.
Description: A phrase that returns forty.
Returns: 40.
```

### Fifty

```text
Syntax: "fifty".
Type: Noun.
Description: A phrase that returns fifty.
Returns: 50.
```

### Sixty

```text
Syntax: "sixty".
Type: Noun.
Description: A phrase that returns sixty.
Returns: 60.
```

### Seventy

```text
Syntax: "seventy".
Type: Noun.
Description: A phrase that returns seventy.
Returns: 70.
```

### Eighty

```text
Syntax: "eighty".
Type: Noun.
Description: A phrase that returns eighty.
Returns: 80.
```

### Ninety

```text
Syntax: "ninety".
Type: Noun.
Description: A phrase that returns ninety.
Returns: 90.
```

### {NOUN} Hundred

```text
Syntax: "{NOUN} hundred".
Type: Noun.
Description: Multiplies a number by a hundred.
Arguments:
    {NOUN}: A noun that represents a number.
Returns: the value of {NOUN} times a hundred.
```

### {NOUN} Thousand

```text
Syntax: "{NOUN} thousand".
Type: Noun.
Description: Multiplies a number by a thousand.
Arguments:
    {NOUN}: A noun that represents a number.
Returns: the value of {NOUN} times a thousand.
```

### {NOUN} Million

```text
Syntax: "{NOUN} million".
Type: Noun.
Description: Multiplies a number by a million.
Arguments:
    {NOUN}: A noun that represents a number.
Returns: the value of {NOUN} times a million.
```

### True

```text
Syntax: "true".
Type: Sentence.
Description: A phrase that does true.
Returns: True.
```

### True

```text
Syntax: "true".
Type: Noun.
Description: A phrase that returns true.
Returns: True.
```

### False

```text
Syntax: "false".
Type: Sentence.
Description: A phrase that does false.
Returns: False.
```

### False

```text
Syntax: "false".
Type: Noun.
Description: A phrase that returns false.
Returns: False.
```

### Whether {SENTENCE}

```text
Syntax: "whether {SENTENCE}".
Type: Noun.
Description: A phrase that returns whether {SENTENCE}.
Arguments:
    {SENTENCE}: A sentence.
```

### {NOUN} Is Greater/Larger Than Or Equal To {NOUN2}

```text
Syntax: "{NOUN} is greater/larger than or equal to {NOUN2}".
Type: Sentence.
Description: Compare two values's size.
Arguments:
    {NOUN}: A noun that has ">=" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: whether {NOUN} is greater/larger than or equal to {NOUN2}.
```

### {NOUN} Is Less/Smaller Than Or Equal To {NOUN2}

```text
Syntax: "{NOUN} is less/smaller than or equal to {NOUN2}".
Type: Sentence.
Description: Compare two values's size.
Arguments:
    {NOUN}: A noun that has "<=" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: whether {NOUN} is less/smaller than or equal to {NOUN2}.
```

### {NOUN} Is Greater/Larger Than {NOUN2}

```text
Syntax: "{NOUN} is greater/larger than {NOUN2}".
Type: Sentence.
Description: Compare two values's size.
Arguments:
    {NOUN}: A noun that has ">" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: whether {NOUN} is greater/larger than {NOUN2}.
```

### {NOUN} Is Less/Smaller Than {NOUN2}

```text
Syntax: "{NOUN} is less/smaller than {NOUN2}".
Type: Sentence.
Description: Compare two values's size.
Arguments:
    {NOUN}: A noun that has "<" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: whether {NOUN} is less/smaller than {NOUN2}.
```

### {NOUN} Is Not The Same As {NOUN2}

```text
Syntax: "{NOUN} is not the same as {NOUN2}".
Type: Sentence.
Description: Compare two values's identity.
Arguments:
    {NOUN}: A noun.
    {NOUN2}: A noun.
Returns: whether {NOUN} is not the same as {NOUN2}.
```

### {NOUN} Is Not Equal To {NOUN2}

```text
Syntax: "{NOUN} is not equal to {NOUN2}".
Alias(es): {NOUN} does not equal {NOUN2}.
Type: Sentence.
Description: Compare two values's equality.
Arguments:
    {NOUN}: A noun that has "==" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: whether {NOUN} is not equal to {NOUN2}.
```

### {NOUN} Is The Same As {NOUN2}

```text
Syntax: "{NOUN} is the same as {NOUN2}".
Type: Sentence.
Description: Compare two values's identity.
Arguments:
    {NOUN}: A noun.
    {NOUN2}: A noun.
Returns: whether {NOUN} is the same as {NOUN2}.
```

### {NOUN} Is Equal To {NOUN2}

```text
Syntax: "{NOUN} is equal to {NOUN2}".
Alias(es): {NOUN} equals {NOUN2}.
Type: Sentence.
Description: Compare two values's equality.
Arguments:
    {NOUN}: A noun that has "==" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: whether {NOUN} is equal to {NOUN2}.
```

### {ITEM} Is In {ITERABLE}

```text
Syntax: "{ITEM} is in {ITERABLE}".
Type: Sentence.
Description: Check whether something is in an iterable.
Arguments:
    {ITEM}: A noun.
    {ITERABLE}: A noun.
Returns: Whether {ITEM} is in {ITERABLE}.
```

### {NOUN} Equals {NOUN2}

```text
Syntax: "{NOUN} equals {NOUN2}".
Type: Sentence.
Description: Compare two values's equality.
Arguments:
    {NOUN}: A noun that has "==" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: whether {NOUN} equals {NOUN2}.
```

### {NOUN} Does Not Equal {NOUN2}

```text
Syntax: "{NOUN} does not equal {NOUN2}".
Type: Sentence.
Description: Compare two values's equality.
Arguments:
    {NOUN}: A noun that has "==" defined for {NOUN2}.
    {NOUN2}: A noun.
Returns: whether {NOUN} does not equal {NOUN2}.
```

### If {CONDITION} , {TRUE_ACTION} ; Otherwise/Else , {FALSE_ACTION}

```text
Syntax: "if {CONDITION} , {TRUE_ACTION} ; otherwise/else , {FALSE_ACTION}".
Type: Sentence.
Description: Do something if a condition is true, and do another action if the condition is false.
Arguments:
    {CONDITION}: A sentence that returns a boolean.
    {TRUE_ACTION}: A sentence that will be executed when {CONDITION} is true.
    {FALSE_ACTION}: A sentence that will be executed when {CONDITION} is false.
```

### If {CONDITION} , {TRUE_ACTION}

```text
Syntax: "if {CONDITION} , {TRUE_ACTION}".
Type: Sentence.
Description: Do something if a condition is true.
Arguments:
    {CONDITION}: A sentence that returns a boolean.
    {TRUE_ACTION}: A sentence that will be executed when {CONDITION} is true.
```

### While {CONDITION} , {ACTION}

```text
Syntax: "while {CONDITION} , {ACTION}".
Type: Sentence.
Description: Repeating something when the condition is true.
Arguments:
    {CONDITION}: A sentence that returns a boolean.
    {ACTION}: A sentence that will be executed when {CONDITION} is true.
```

### A New Line

```text
Syntax: "a new line".
Type: Noun.
Description: A phrase that returns a new line.
Returns: "
".
```

### A List With A Size Of {NOUN}

```text
Syntax: "a list with a size of {NOUN}".
Type: Noun.
Description: A phrase that returns a list with a size of {NOUN}.
Arguments:
    {NOUN}: A noun.
```

### New Line

```text
Syntax: "new line".
Alias(es): a new line.
Type: Noun.
Description: A phrase that returns new line.
Returns: "
".
```

### {NOUN} , {NOUN2}

```text
Syntax: "{NOUN} , {NOUN2}".
Type: Noun.
Description: A phrase that returns {NOUN} , {NOUN2}.
Arguments:
    {NOUN}: A noun.
    {NOUN2}: A noun.
```

### {SENTENCE} , {SENTENCE2}

```text
Syntax: "{SENTENCE} , {SENTENCE2}".
Type: Sentence.
Description: A phrase that does {SENTENCE} , {SENTENCE2}.
Arguments:
    {SENTENCE}: A sentence.
    {SENTENCE2}: A sentence.
```

### Execute {ACTION}

```text
Syntax: "execute {ACTION}".
Type: Sentence.
Description: Executes an action.
Arguments:
    {ACTION}: A noun representing an action.
```

### Do Nothing

```text
Syntax: "do nothing".
Type: Sentence.
Description: A placeholder for when a sentence is needed, but nothing should run.
```

### None

```text
Syntax: "none".
Alias(es): null, nil.
Type: Noun.
Description: A phrase that returns none.
Returns: None.
```

### Null

```text
Syntax: "null".
Type: Noun.
Description: A phrase that returns null.
Returns: None.
```

### Nil

```text
Syntax: "nil".
Type: Noun.
Description: A phrase that returns nil.
Returns: None.
```

### Step {LABEL} , {ACTION}

```text
Syntax: "step {LABEL} , {ACTION}".
Type: Sentence.
Description: Label a step as a constant.
Arguments:
    {LABEL}: A constant noun representing the identifier of the label.
    {ACTION}: A sentence associated with the label.
```

### Go To Step {LABEL}

```text
Syntax: "go to step {LABEL}".
Type: Sentence.
Description: Jump to a label. Some say it's a sh!t practice, but haters are going to hate, and there's nothing I can do about it. How else am I supposed to make it "Turing complete" with the time given?.
Arguments:
    {LABEL}: A constant noun representing the identifier of the label.
```


