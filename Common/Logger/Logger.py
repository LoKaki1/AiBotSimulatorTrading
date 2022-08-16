import termcolor


def error(text):
    termcolor.cprint(text, 'red')

def info(text):
    termcolor.cprint(text, 'cyan')