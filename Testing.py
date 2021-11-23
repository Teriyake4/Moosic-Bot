def dislplayArguments(argument1, *argument2, **argument3):

    # displaying predetermined argument
    print(argument1)

    # displaying non keyword arguments
    for arg in argument2:
        print(arg)

    # displaying non keyword arguments
    for arg in argument3.items():
        print(arg)

arg1 = "Welcome"
arg3 = "Geeks"

# function call
dislplayArguments(arg1, "to", arg3, agr4 = 4,
                  arg5 ="Geeks !")
