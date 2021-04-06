# IngScript

```ingscript
     ,a8a,                                 ,gg,
     ,8" "8,                               i8""8i                                           I8
     d8   8b                               `8,,8'                                           I8
     88   88                                `88'                          gg             88888888
     88   88                                dP"8,                         ""                I8
     Y8   8P  ,ggg,,ggg,     ,gggg,gg      dP' `8a    ,gggg,   ,gggggg,   gg   gg,gggg,     I8
     `8, ,8' ,8" "8P" "8,   dP"  "Y8I     dP'   `Yb  dP"  "Yb  dP""""8I   88   I8P"  "Yb    I8
8888  "8,8"  I8   8I   8I  i8'    ,8I _ ,dP'     I8 i8'       ,8'    8I   88   I8'    ,8i  ,I8,  
`8b,  ,d8b, ,dP   8I   Yb,,d8,   ,d8I "888,,____,dP,d8,_    _,dP     Y8,_,88,_,I8 _  ,d8' ,d88b,
  "Y88P" "Y88P'   8I   `Y8P"Y8888P"888a8P"Y88888P" P""Y8888PP8P      `Y88P""Y8PI8 YY88888P8P""Y8s
                                 ,d8I'                                         I8
                               ,dP'8I                                          I8
                              ,8"  8I                                          I8
                              I8   8I                                          I8
                              `8, ,8I                                          I8
                               `Y8P"                                           I8


```

## About

**IngScript** is a scripting language that uses English as the basis of its script. The name **IngScript** is a combination of the words *English* and *Script*. **IngScript** has a long history. The first appearance of **IngScript** can be found as early as 5th century, although the form is quite different from **IngScript** today. You can look up on Wikipedia and see that it is complete [redacted], but it's okay because it is technically correct, the best kind of correct.

**IngScript** is intended to be readable and useable by anyone who can speak English. It is so English-like that it makes python and more importantly, smalltalk, look like they are spoken by someone who are [redacted]. For example:

```smalltalk
x > 0 ifTrue: [ "Do something" ] ifFalse: [ "Do other things" ]
```

What the [redacted] is this? Who the [redacted] speaks like that?

In **IngScript**, you don't need to do anything like that. Here is a statement that does exactly that:

```ingscript
If x is greater than 0, do something. Otherwise, do other things.
```

See how it is easier to read? Anyone that could speak English can program this. "It is 'pedagogically' the easiest language to learn." quoth I.

All valid **IngScript** code are valid English. This means that you can't use brackets to group things together like other languages. Brackets are for comments in **IngScript**. What happens when you need brackets to group things together? You don't. It is entirely your fault that your script is so unclear that you need brackets to group things together. You should use multiple lines, like how your English teacher tells you to do.

To ease the programming experience, **IngScript** allows users to add spaces and newlines however they want. White spaces are merely separators between tokens. Each statement ends with a period (.) anyway, so there is no need to properly format everything like in Python. However, it is recommended that the user properly format their code to make it more readable.

As in English, **IngScript** is not case sensitive unless in some specific cases. Special nouns specifically declared are case sensitive(For example, all characters in "ASCII" are case sensitive), but in a normal sentence, everything is not case sensitive.

## How to use this interpreter

Open `main.py` and run it. You can also run it through a console and give it many arguments. When you run the script, enter `help` for a list of commands you can do.

Alternatively, you can open `main.bat`, presuming you have `python` command installed. You can open an **IngScript** file with the batch file to directly run it.

## Syntax

### Comments

```ingscript
(This is a comment)
```

In **IngScript** comments are declared using brackets. Anything inside brackets are ignored by the intepreter. This is a multiline comment. [redacted] single line comments. You can add multiple brackets in comments, as long as the brackets have a one to one pairing with each other. `(a comment(things explaining this comment))` is allowed as a comment.

### String literals

```ingscript
"This is a string literal"
```

In **IngScript** string literals are declared using double quotes. Anything between the double quotes are intepreted as literal strings by the intepreter. You can use some escape characters, like "\n", just so it's not too obnoxious.

String literals can span across multiple lines. For each line that a string literal spans, a free double quote can be added at the beginning of the line to indicates that a string is part of a literal. Newlines and tabs are included. For example:

```ingscript
Output
"War is peace
"Freedom is slavery
"Ignorance is strength".
```

or

```ingscript
Output
"War is peace
Freedom is slavery
Ignorance is strength".
```

### Numbers

In **IngScript**, only numbers represented with the decimal notation are supported. That means `4`, `12`, `3.1415926` are supported, while numbers such as `0x77ff` are not supported because that's not English. You can do `-23`, but that's technically two tokens(I think).

Since the compiler is written in Python, there are no size limits to integers.

### Sentence

```ingscript
Do some action.
```

In **IngScript**, sentences ends with ".", just like in real English. A sentence is a type of phrase that usually has no return value or boolean return value, and usually modifies the state of the program somehow. Examples of a sentence phrase are `Set ... to ...` and `... is equal to ...`

### Noun

In **IngScript**, a noun is a type of phrase that usually has a return value. It's used as a parameter for other phrases. For example, you can't just say `twelve`, you have to use it in another phrase such as `Set x to twelve.` or something like that.

### Labels and go to statements

For this language to be turing complete, it has to either have a way to do a while loop, or have go to statements. This language has both! See `go to {LABEL}` and `while {CONDITION} , {ACTION}` for looping and goto statements.

### Code blocks

Right now, just use `execute the action {ACTION_STRING}` for a code block, because that's easier for me to do right now.
