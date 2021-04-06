import sys
from language_library import *
from pattern_storage import *
from documentation import generateDocFile
logo = """     ,a8a,                                 ,gg,
     ,8" "8,                               i8""8i                                           I8
     d8   8b                               `8,,8'                                           I8
     88   88                                `88'                          gg             88888888
     88   88                                dP"8,                         ""                I8
     Y8   8P  ,ggg,,ggg,     ,gggg,gg      dP' `8a    ,gggg,   ,gggggg,   gg   gg,gggg,     I8
     `8, ,8' ,8" "8P" "8,   dP"  "Y8I     dP'   `Yb  dP"  "Yb  dP""\""8I   88   I8P"  "Yb    I8
8888  "8,8"  I8   8I   8I  i8'    ,8I _ ,dP'     I8 i8'       ,8'    8I   88   I8'    ,8i  ,I8,  
`8b,  ,d8b, ,dP   8I   Yb,,d8,   ,d8I "888,,____,dP,d8,_    _,dP     Y8,_,88,_,I8 _  ,d8' ,d88b,
  "Y88P" "Y88P'   8I   `Y8P"Y8888P"888a8P"Y88888P" P""Y8888PP8P      `Y88P""Y8PI8 YY88888P8P""Y8s
                                 ,d8I'                                         I8
                               ,dP'8I                                          I8
                              ,8"  8I                                          I8
                              I8   8I                                          I8
                              `8, ,8I                                          I8
                               `Y8P"                                           I8"""
commands = """-----------------------------------------------------
List of available commands:
- documentation: Generate a documentation for the current scope at DOCUMENTATION.md.
- exit: Exit the script.
- help: Print the available commands.
- info: Print the information regarding IngScript and this compiler.
- run <filename>: Execute this IngScript file.
-----------------------------------------------------"""
about = """About IngScript:
IngScript is a scripting language that uses English as the basis of its script. The name IngScript is a combination of the words *English* and *Script*. IngScript has a long history. The first appearance of IngScript can be found as early as 5th century, although the form is quite different from IngScript today. You can look up on Wikipedia and see that it is complete [redacted], but it's okay because it is technically correct, the best kind of correct.

IngScript is intended to be readable and useable by anyone who can speak English. It is so English-like that it makes python and more importantly, smalltalk, look like they are spoken by someone who are [redacted]. For example:

> smalltalk:
> x > 0 ifTrue: [ "Do something" ] ifFalse: [ "Do other things" ]

What the [redacted] is this? Who the [redacted] speaks like that?

In IngScript, you don't need to do anything like that. Here is a statement that does exactly that:

> ingscript:
> If x is greater than 0, do something. Otherwise, do other things.

See how it is easier to read? Anyone that could speak English can program this. "It is 'pedagogically' the easiest language to learn." quoth I.

For more information, read the README.md page, clearly.

For all the available phrases in IngScript, read DOCUMENTATION.md. I thought it should be fairly obvious.

For an up-to-date documentation, enter "documentation" as the command.
"""
# Process a list of arguments
def processArguments(args):
    if len(args) == 0:
        return
    if args[0] == "run":
        if len(args) == 1:
            print("Syntax: run <filename>")
            return
        filename = args[1]
        if filename.split(".")[-1] != "ing":
            filename += ".ing"
        with open(filename, "r") as openedFile:
            text = openedFile.read()
            try:
                executeString(text)
            except Exception as e:
                print("\n\nError on execution:",e)
            else:
                print("\n\nProgram successfully exits with no errors.")
    elif args[0] == "help":
        print(commands)
    elif args[0] == "info":
        print(about)
    elif args[0] == "documentation":
        generateDocFile()
        print("Generated documentation at DOCUMENTATION.md.")
    elif args[0] == "exit":
        exit()
    else:
        print("Unrecognized command. Enter \"help\" for more information.")
if __name__ == "__main__":
    if len(sys.argv) > 1 and not(len(sys.argv) == 2 and sys.argv[1] == "run"):
        # print(sys.argv)
        processArguments(sys.argv[1:])
        input()
    else:
        print(logo)
        print("""Welcome to IngScript! Enter "help" for how to use this script, and "info" for more information regarding IngScript.""")
        while True:
            arguments = input("> ").split(" ")
            processArguments(arguments)