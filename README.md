# WhileProc-language-lexer-parser
A simple lexer and parser for a programming language called WhileProc. This language only supports simple procedures, while loops, conditionals, some operations of floating point numbers and printing. This Lexer and parser includes tokenizer with comment handling and parser with error handling.

The main components of this project are
* `syntax.py` - Defines the AST nodes and interprets them
* `parse.py` - Tokenizes the source code after handling comments and parses the tokens according to the grammer. returns AST nodes.

### WhileProc Programming Language
WhileProc Programming language supports the following statements
* print - prints a number or output of a function
* proc - keyword for function definition
* if - conditional statement
* else - else conditional statement
* while - while loop

Syntax of the WhileProc language follows the following rules in general
* Every line ends with a ';' except the last line
* Each block is enclosed with curly braces
* inline comments `/*...*/`
* single line comments `// ...`
* multiple line comments `/* .. multiple lines .. */`
* Assignment operator is `:=`
* Supports simple floating point operations.

### Usage
To use this lexer and parser, run 
```bash
python run_while_code <filename.while>
```
### Example
Three Examples sources are provided. 
#### Example 1
```bash
python run_while_code example_1.while
```
This code shows basic Functions, Prints and Inline comments

#### Example 2
```bash
python run_while_code example_2.while
```
This Code shows a recursive funtion with all supported comment formats

#### Example 3
```bash
python run_while_code example_3.while
```
This Code shows a sytax error case which returns a syntax error message upon running