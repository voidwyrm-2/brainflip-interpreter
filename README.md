# brainflip-interpreter
my interpreter for [Branflakes](https://en.wikipedia.org/wiki/brainfuck)

I've always wanted to mess with Brainoof, so why use other people's interpreters when I can just make my own?

<!--**please keep in mind multi-line "[]" pairs do not work because of how I coded them**-->

# Usage
this has a terminal specifically for running Branflakes
### commands
* "exit": exits terminal
* "run [code]" runs the given Branflakes code
* "file [path]": runs the code in the file at the given path
* "hw", "helloworld", or "hello world": runs a hardcoded helloworld program

**both the "run" and "file" commands have an optional "--truncate" flag that removes all characters that are not base Branflakes commands and prints it instead of running the code**