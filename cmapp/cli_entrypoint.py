"""Usage: cmapp
        cmapp add (-n <name> -m <mobile>)
        cmapp (-i | --interactive)

Options:
    -s, --start  Interactive Mode
    -h, --help  Show this screen and exit.
"""


import sys
import os
import cmd
from docopt import docopt, DocoptExit
from crudoperations import CrudOperations




# compares the arguments to determine if all have been entered in correct
# manner
def parser(func):

    def fn(self, arg):
        try:
            # tries to compare entered commands against the doc
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The entered arguments don't match

            print('Sorry,you entered an invalid command')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

"""Class overrides method parser so as to validate input.The input arguments
    are mapped to respective methods
"""
class CMapp(cmd.Cmd):
    
    prompt = '(cmapp) '
    file = None

    @parser
    def do_add(self, arg):
        
        """Usage: cmapp add (-n <name> -m <mobile>)"""
        addcontact(arg)

    def do_quit(self, arg):

    	"""Exit application."""

    	print('Exited!')
        exit()

opt = docopt(__doc__, sys.argv[1:])


"""Creates a new contact
"""


def addcontact(docopt_args):
    if docopt_args["-n <name>"] and docopt_args["-m <mobile>"]:
        name = docopt_args["<name>"]
        mobilenum = docopt_args["<mobile>"]
        contacts = CrudOperations()
        contacts.save(contactname=name, contactnumber=mobilenum)
    

if opt['--start']:

    CMapp().cmdloop()  # creates the REPL

print(opt) 
# opt = docopt(__doc__, sys.argv[1:])

# if opt['--start']:
#     try:
#         CMapp().cmdloop()
#     except SystemExit:
#         pass
#     except KeyboardInterrupt:
#         pass
# if __name__ == '__main__':
#     CMapp().cmdloop()

