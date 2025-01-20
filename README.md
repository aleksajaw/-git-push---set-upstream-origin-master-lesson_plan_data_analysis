
## Python version
The Python version used to create the project is 3.12.7.

<br>

## Commands
At first, navigate to the folder named `py_version`. Open a terminal and run one of the following commands:

* #### Setup
For setup only.
```bash
python main.py --setup
```

* #### Setup & start
For setup and start the program after it.
```bash
python main.py --setup --start
```

* #### Start
After installing the virtual environment (which happens with `--setup` or `--setup --start`),<br>
you will be able to simply use one of these commands to quickly start the program:
```bash
python main.py --start
```
or
```bash
python main.py
```

* #### Force
The program could not start correctly due to the accidental deletion of one of the virtual environment files<br>
or an interruption during setup, which prevented it from finishing as expected.<br>
The following commands force the program to reinstall the entire environment,<br>
if any of these errors occur:
```bash
python main.py --setup --force
```

<br>

Also, the main purpose of the following command is to ensure the program starts correctly,<br>
even if any errors occur:
```bash
python main.py --start --force
```

<br>

*...and the rest is history.*

<br>
<br>

> Ignore .old entries.