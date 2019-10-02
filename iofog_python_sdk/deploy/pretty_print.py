from colorama import init

#
# Pretty Print is a rather simple helper utility that exposes some helper methods to make printing logging
# information more colorful and easier to understand.
#
# Initialize colorama
init(autoreset=True)

# These are the colors that we'll use in our output
NO_FORMAT = '\033[0m'
C_SKYBLUE1 = '\033[38;5;117m'
C_DEEPSKYBLUE4 = '\033[48;5;25m'
RED = '\033[38;5;1m'
GREEN = '\033[38;5;28m'


#
# Display a nice title line for any output. You can optionally populate it with a string
#
# Usage: pretty_title("Bootstrapping ioFog")
#
def pretty_title(title):
    print_info("## " + title + " ####################################################")


#
# Display a nice header for any command line script. You can optionally populate it with a string
#
# Usage: pretty_header("Bootstrapping ioFog")
#
def pretty_header(title):
    print_info("## " + title + " ####################################################")
    print_info("## Copyright (C) 2019, Edgeworx, Inc.\n")


# Basic subtle output
def print_info(message):
    print(C_SKYBLUE1 + message + NO_FORMAT)


# Highlighted output with a background
def print_notify(message):
    print(C_DEEPSKYBLUE4 + message + NO_FORMAT)


# Hurrah!
def print_success(message):
    print(GREEN + message + NO_FORMAT)


# Houston, we have a problem!
def print_error(message):
    print(RED + str(message) + NO_FORMAT)
