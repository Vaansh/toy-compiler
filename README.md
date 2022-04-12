<h1> COMP 442: Final Project</h1>

[//]: # "META DATA"
[//]: # "Course: 'COMP 442: Compiler Design'"
[//]: # "Semester: 'Winter 2022'"
[//]: # "University: 'Concordia University'"
[//]: # "Submission: 'Final Project'"
[//]: # "Author: 'Vaansh Vikas Lakhwara'"
[//]: # "Date: 'April 05, 2022'"

---

<details>
    <summary>
        <strong>
            Table of Contents
        </strong>
    </summary>

- [Grading](#grading)
- [Usage](#usage)
  - [1. Basic Usage](#1-basic-usage)
  - [2. Directory usage with Shell script](#2-directory-usage-with-shell-script)
  - [3. Usage for tests designed for demo](#3-usage-for-tests-designed-for-demo)
- [Implementation](#implementation)
  - [1. Design Patterns](#1-design-patterns)
  - [2. Tools Used](#2-tools-used)

</details>

---

## Grading

Please refer to the [implemented](https://github.com/Vaansh/compiler/blob/main/results/implemented.md) markdown file to find a list of all implemented points, as per the final grading scheme.

---

## Usage

### 1. Basic Usage

Place the `.src` file in the `source/` directory and run the following command for instructions:

```zsh
python compiler.py -h
```

**Instructions**

```zsh
usage: compiler.py [-h] file

+----------------------------+-------------+-----------------+-----------------------+
|           Course           |   Semester  |    Professor    |         Author        |
+----------------------------+-------------+-----------------+-----------------------+
| COMP 442 - Compiler Design | Winter 2022 | Dr. Joey Paquet | Vaansh Vikas Lakhwara |
+----------------------------+-------------+-----------------+-----------------------+

Moon Compiler.
A moon compiler written for the course COMP 442 at Concordia University.

positional arguments:
  file        input file to be compiled (format: 'source/*.src').

options:
  -h, --help  show this help message and exit
```

**Installation**

```zsh
pip install -r requirements.txt
```

**Example**:

```zsh
python compiler.py source/bubblesort.src
```

**Sample Output**:

```zsh
===============================================================================================================


        ▄████████  ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄███████▄  ▄█   ▄█        ▄█  ███▄▄▄▄      ▄██████▄
        ███    ███ ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███  ███       ███  ███▀▀▀██▄   ███    ███
        ███    █▀  ███    ███ ███   ███   ███   ███    ███ ███▌ ███       ███▌ ███   ███   ███    █▀
        ███        ███    ███ ███   ███   ███   ███    ███ ███▌ ███       ███▌ ███   ███  ▄███
        ███        ███    ███ ███   ███   ███ ▀█████████▀  ███▌ ███       ███▌ ███   ███ ▀▀███ ████▄
        ███    █▄  ███    ███ ███   ███   ███   ███        ███  ███       ███  ███   ███   ███    ███
        ███    ███ ███    ███ ███   ███   ███   ███        ███  ███▌    ▄ ███  ███   ███   ███    ███
        ████████▀   ▀██████▀   ▀█   ███   █▀   ▄████▀      █▀   █████▄▄██ █▀    ▀█   █▀    ████████▀
                                                                  ▀


                    ----------------------------   [X]   ----------------------------
+-------------------------------------------------+----------------------------------------------------------+
|                      STAGE                      |                          OUTPUT                          |
+-------------------------------------------------+----------------------------------------------------------+
|        Compiling for source code file at:       |                  source/bubblesort.src                   |
|      Output tokens generated and stored at:     |   results/7407807722370555507/bubblesort.outlextokens    |
|     Invalid tokens and error logs stored at:    |   results/7407807722370555507/bubblesort.outlexerrors    |
|        Derivation for the file stored at:       |   results/7407807722370555507/bubblesort.outderivation   |
|      Syntax errors for the file stored at:      |  results/7407807722370555507/bubblesort.outsyntaxerrors  |
|         AST Tree for the file stored at:        |      results/7407807722370555507/bubblesort.outast       |
|       Symbol Table for the file stored at:      |  results/7407807722370555507/bubblesort.outsymboltable   |
| Semantic Errors/Warning for the file stored at: | results/7407807722370555507/bubblesort.outsemanticerrors |
|        Moon file for the file stored at:        |       results/7407807722370555507/bubblesort.moon        |
+-------------------------------------------------+----------------------------------------------------------+
```

### 2. Directory usage with Shell script

To save time and run all the files in the `source/` directory,simply run:

```zsh
sh compile.sh
```

To clean up all generated folders in the `results/` directory, run:

```zsh
sh clean.sh
```

### 3. Usage for tests designed for demo

For the demo, run the following command for a closer look at each working component (performs all tests in the `tests/` directory):

```zsh
python final-demo.py
```

---

## Implementation

### 1. Design Patterns

- [Facade pattern](http://www.design-patterns-stories.com/patterns/Facade/)
- [Visitor pattern](https://web.archive.org/web/20151022084246/http://objectmentor.com/resources/articles/visitor.pdf)

### 2. Tools Used

- Python programming language

  - _Used because_: good working knowledge.
  - _link_: https://www.python.org

- Referenced tool while creating grammar

  - _Used for_: gaining clarity while creating grammar.
  - _link_: https://smlweb.cpsc.ucalgary.ca/

- black python formatter

  - _Used for_: code consistency.
  - _link_: https://github.com/psf/black

- Markdown for documentation

  - _Used for_: good, clear and easy documentation.
  - _link_: https://daringfireball.net/projects/markdown/

- PrettyTable

  - _Used for_: output presentation.
  - _link_: https://pypi.org/project/prettytable/

- pipreqs
  - _Used for_: generating `requirements.txt`
  - _link_: https://github.com/bndr/pipreqs
