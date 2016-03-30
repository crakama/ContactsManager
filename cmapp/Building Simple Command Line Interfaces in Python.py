Building Simple Command Line Interfaces in Python
BY RANDALL DEGGES - NOVEMBER 2 2015
skele-cli

Building command line programs has been a long time passion of mine. There’s something magical about making a simple, intuitive, and composable CLI. There’s also nothing more beautiful than chaining together a series of CLI programs to solve a complex problem quickly.

Here at Stormpath, we’ve built our entire product CLI in Python to create / manage / edit users for your applications, and have been really happy with the result.

Most of this is thanks to the wonderful docopt library, which provides automatic CLI argument parsing and makes building complicated CLIs incredibly simple. And the best part? It works across more than 20 different programming languages! This means that even if you’re building a new CLI app in Go, Rust, or something in between, chances are you can use docopt, too!

If you want to know how to structure your next CLI-based app to minimize complexity and maximize awesomeness, keep reading.
An Overview of CLI Tools

For the purposes of this article, we’re going to be building a really simple CLI called skele that works via subcommands.

There are typically two types of CLI tools that people build: single and multi-command. A good example of a single command CLI tool would be the grep command.

This is because the grep tool takes various options, but does only one thing: match text.

For instance, if I wanted to search a file for my name, I might run the following command:

1
$ grep 'Randall' some-file.txt
On the other hand, there are CLI tools that operate via sub-commands, and do many things. These tools are typically harder to build as they have more complexity.

A good example of sub-command driven CLI tool would be the Heroku CLI tool. This tool allows you to create new web applications, deploy them live, and provision resources for these applications — all via sub-commands.

For instance, if I wanted to create a new Heroku application, I might run the following command:

1
$ heroku applications:create my-new-app
In the example above, applications:create is the name of a sub-command.

If I wanted to later remove my application from Heroku, I could then say:

1
$ heroku applications:destroy my-new-app
See how the one CLI tool can perform different actions? Well, that’s what we’ll be building today. A CLI tool that is capable of simply running sub-commands and handling them in a graceful way.

The specific CLI tool I’ve built as reference material for this article is called skele, and can be found on this Github page.

This tool ships with a single sub-command hello, that just prints some text to the console. It also includes a manual page, help information, and version information in a standard UNIX-compliant manner.

So, on with the show!

Structuring a CLI Project in Python

Before we dive into all the specifics regarding how to build good CLI-based applications, let’s first talk about structuring your project properly. If you want to skip ahead and just look at the source code to figure out how things work, here’s a link to the Github page.

There is an infinite number of ways to structure Python projects, but for CLI apps in particular, I like the following approach the best as it is straightforward, and keeps things simple:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
skele-cli
├── MANIFEST.in
├── README.rst
├── setup.cfg
├── setup.py
└── skele
    ├── __init__.py
    ├── cli.py
    └── commands
        ├── __init__.py
        ├── base.py
        └── hello.py

2 directories, 9 files
At the very top-level, you’ve got the project folder, which in this case is called skele-cli. This will be your main code repository.

Python Packaging Files

Inside of the top-level project folder, you’ve got a few Python packaging files that I’ll explain below.

Firstly, you’ve got MANIFEST.in. This tells the Python build tool what files to include when you ship your package to the world.

1
2
3
4
5
6
7
8
9
10
11
12
# MANIFEST.in
exclude .gitignore
exclude .coverage
exclude .travis.yml
include README.rst
include setup.cfg
prune .cache
prune .git
prune build
prune dist
recursive-exclude *.egg-info *
recursive-include tests *
As you’ll notice above, I’m pro-actively removing and excluding a lot of unnecessary files that would otherwise get included in the package.

Whenever you build your Python package, this file will be scanned by the Python build tool, and these rules will be used to remove or add files in your package accordingly.

In particular, I don’t like including private git folders, build folders, coverage reports, etc. in my package builds, as it unnecessarily clutters up a user’s system.

Next up, you’ve got the setup.cfg file. This file just tells the Python build tool that your program should run on all platforms when building the binary. If this isn’t true for your specific project, you can remove this file.

NOTE: For 99.99% of people, you’ll want to leave this file alone =)

1
2
3
# setup.cfg
[bdist_wheel]
universal=1
Finally, you’ve got the setup.py file. This is where you tell Python all about your CLI tool and how it is packaged up.

Now, the next file we’re going to look at is quite large (setup.py), so I won’t copy / paste all the contents here, if you want to view the entire thing, check it out on Github: https://github.com/rdegges/skele-cli/blob/master/setup.py

Here’s the important / cool bits you should know about:

This setup script will automatically use your README.rst file for documentation. This is nice because when you deploy your package to PyPI, it will have legitimate looking documentation:
1
2
3
this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()
This setup script includes testing support via the popular py.test library (and coverage reporting, too!). 
This means that if you run the $ python setup.py test command, your entire package will be tested nicely (assuming you write tests, that is). Here’s the code that makes this possible:
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)
This setup script won’t accidentally install your documentation or tests on the user’s system as actual packages. 
This happens quite frequently, and causes nasty namespace collisions. 
The relevant bit of code that prevents this from happening can be seen below:
1
packages = find_packages(exclude=['docs', 'tests*']),
This setup script can install all development dependencies easily — this means that if you’re cloning this project fresh, and want to work on it for development purposes, you can run the $ pip install -e .[test] command and the entire CLI program as well as all test dependencies will be installed!
1
2
3
extras_require = {
    'test': ['coverage', 'pytest', 'pytest-cov'],
},
Lastly, this script ensures that your CLI program is started correctly when run from the command line. 
If a user installs your CLI program, they’ll be able to run it by simply typing the program name, 
in this case, $ skele in the terminal:
1
2
3
4
5
entry_points = {
    'console_scripts': [
        'skele=skele.cli:main',
    ],
},
The CLI Package

Now that we’ve covered the Python packaging files, let’s talk about the actual CLI package itself! How do we structure our actual Python code?

The first thing we’ll need is a package (a folder in this case) called skele — as this is our application’s name.

Inside of this folder there are two files we need to quickly discuss.

First, the __init__.py file. The only thing this file contains is our program’s version number:

1
2
# __init__.py
__version__ = '1.0.0'
This version number is what you’ll update when you make new releases.

Second, we’ve got our cli.py file — this is where most of the magic happens. This file contains a function named main which is the code that will actually run when a user types $ skele in the command line.

The reason this function is the one that runs is because of the code we setup previously in our setup.py file: https://github.com/rdegges/skele-cli/blob/master/setup.py#L64-L68 (these lines of code tell Python to execute this particular function when our program is run).

So, next up we’ve got our commands module (another folder). This module contains the actual implementation of our CLI commands.

If you take a look in this folder, you’ll see the following files defined:

__init__.py – This contains our import statements.
base.py – A base command class that all other classes will extend.
hello.py – This is an example command implementation.
If I was building a CLI app that could be used by typing:

1
2
$ skele hi
$ skele bye
Then I’d have two new Python files in my commands folder: hi.py and bye.py. This is how I like to structure things to keep them as simple as possible.

So now that we’ve covered the basic layout, let’s talk about the actual implementation.

Using docopt to Build a Simple CLI

docopt

I love the docopt library. It makes defining CLI interfaces incredibly simple.

The way docopt works is pretty magical: instead of writing rules and telling your program what options to look for, you instead just define the manual page for your CLI program, and docopt will automatically parse this string for you, and generate all the option parsing code too!

Here’s how it works in the skele example application I’ve built. This is the cli.py file source code (notice the big docstring at the top of the file):

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
"""
skele

Usage:
  skele hello
  skele -h | --help
  skele --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  skele hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rdegges/skele-cli
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k):
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
That huge docstring at the top of the file is standard CLI documentation, right? It looks like the output you see when you run a CLI program. It lists how to use the program, how it works, and what options are available.

Well, what happens here is that down below, in the main function, I’m using the docopt library to parse that huge docstring and generate a list of options automatically:

1
2
# __doc__ is a special variable that references this file's docstring.
options = docopt(__doc__, version=VERSION)
If you go ahead and print out the options variable, you’ll see something similar to the following (depending on how you run the program):

1
2
3
4
# `$ skele hello` is the command I ran to output these options.
{'--help': False,
 '--version': False,
  'hello': True}
Pretty amazing, right? docopt generated a dictionary of options that have already been parsed and validated automatically.

Notice how the hello variable is set to True? This means that the user typed the $ skele hello command =)

Now, since we know that docopt is already handling the hard stuff:

Parsing our CLI documentation into real options.
Generating a dictionary of options.
All we have to do is call the appropriate code to run, right?

In the above example, we’re running the $ skele hello command on the CLI — so in the next section, we’ll take a look at how to hook that logic into our app.

Defining Commands in the CLI Program

When building a CLI program, most of the time your program is going to do different things based on what sub-commands are being run.

For instance, in our example skele application, I might want to define several sub-commands that a user can run:

1
2
3
$ skele hello   # say hello, world!
$ skele bye     # say bye!
# etc...
In the example above, I’m referring to both hello and bye as sub-commands.

The way I’ve structured the skele sample app is such that you can define a Python file for each sub-command you want to support, and it will get run automatically when the user specifies that command.

Let’s take a look at how a command works. We’ll start by looking at the hello.py file:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
# skele/commands/hello.py
"""The hello command."""


from json import dumps

from .base import Base


class Hello(Base):
    """Say hello, world!"""

    def run(self):
        print 'Hello, world!'
        print 'You supplied the following options:', dumps(self.options, indent=2, sort_keys=True)
The idea is that each command will have a class inside of it that extends from Base. Here’s what base.py looks like:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
# skele/commands/base.py
"""The base command."""


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')
Whenever we construct a new instance of a command class, we’ll pass in the options that were generated using docopt. This way, each sub-command has access to all the user supplied CLI information.

Finally, we’ll define a run method on each command class, and this is what we’ll call to actually do something that the user wants. This is where we’ll put our logic.

In the hello.py example, we’re simply going to say “Hello, world!” and output the options.

Now, going back to the cli.py file, let’s take a look at how we actually use these command classes to get stuff done:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
# skele/cli.py
def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k):
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
What we’re doing here is this:

We parse the CLI options from the user via docopt.
We loop through the CLI options.
If there is a command module whose name matches a CLI option, then we’ll dynamically figure out the name of the command class.
After getting the command class, we’ll create an instance of it, passing along the user supplied options from docopt.
Finally, we’ll call the run method on our class, which will actually make stuff happen.
If we were to say $ skele hello, for instance, here’s what would happen:

We’d loop through the commands module and find that commands.hello is a valid Python module.
We’d then figure out that Hello is the name of the class we’ve defined inside that file.
Finally, we’ll create a new instance of a Hello class, and call the run method.
All together now, this is what makes our CLI program work!

This is pretty cool because it means that adding or changing our CLI interface is as simple as modifying the docstring we’ve defined in skele/cli.py, as well as creating a proper command in our commands directory.

Simple, right?

Building CLIs Made Simple

By utilizing the awesome docopt module, and structuring your project the right way, building simple CLI programs can be really easy!

Be sure to check out skele-cli on Github for reference, and if you’re looking for more information about Python packaging best practices, be sure to check out the official Python packaging guide.

Get Started with Stormpath