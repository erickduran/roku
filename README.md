# roku-compiler
This repository stores the implementation of the compiler for the __roku__ programming language.

## Getting started

### What is it?
A compiler for a simple "domestic" programming language inspired by _Avatar: The Last Airbender_.

### What it isn't?
* An official compiler.
* A compiler for a day-to-day use programming language.

### Status
The current status of this project is __DONE__. This includes:
* Lexical analyser
* Syntax analyser
* Semantic analyser
* Middle code tuples

### Version
This repository stores v1.0 of the  __roku__ compiler.

### Prerequisites
This compiler was implemented using __Python 3__ (3.7.0) and it is designed for it. You will need to have this installed prior to usage, along with the __click__ library. To install this, use the following command:

```bash
pip install click
```

### Usage
To compile using the __roku__ compiler, use the following command:

```bash
python roku.py [OPTIONS] SOURCE_FILE
```
Options can be used to track each of the steps of the compiling process. For example, use:

```bash
python roku.py --ast ../tests/test_source.fang
```
This will compile the input source file and print the corresponding generated abstract syntax tree.

### What everything means

__Terminals__ | __Actual meaning__
------------- | -------------
zhuli  		| data type for integers
appa    	| data type for floating (get it?) point value
koi			| data type for boolean values
tui, la 	| true, false (yin and yang, push and pull)
scroll  	| data type for strings of characters
wan			| data type for individual characters
sokka 		| null value
bend		| for function declarations
agni, kai 	| if, else
avatar 		| for loop (cycle)
raava		| while loop (bigger cycle)
cabbage		| loop breaking
yipyip		| return
energy		| reserved word for the main block


## Authors
Developed by _The Boomeraangs_. Copyright © 2018, Alfa Venegas, Daniel Ortega and Erick Durán. CETYS Universidad.

## License
Released under the GNU GENERAL PUBLIC LICENSE.
