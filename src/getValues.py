import numpy as np

def Eval(cmd, T=None):

    fResult = True
    value = None

    try:
        value = eval(cmd)
    except NameError:
        print('Name Error: %s' % cmd)
        fResult = False
    except SyntaxError:
        print('Syntax Error: %s' % cmd)
        fResult = False
    except TypeError:
        print('Type Error: %s' % cmd)
        fResult = False

    return fResult, value

def Evals(cmds, num):

    fResult = True
    values = []

    for i in range(num):

        fResult, value = Eval(cmds[i])

        if fResult:
            values.append(value)
        else:
            break

    return fResult, values
