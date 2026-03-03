# python-interpreter

Lightweight embedded Python interpreter for workflow scripting within the [Rinkt](https://rinkt.com) automation platform.

Supports executing Python scripts, inline commands (`-c`), and interactive REPL mode. Used by the Rinkt runner to execute Python-based workflow activities.

## Usage

```bash
# Run a script file
python python_interpreter.py script.py

# Execute inline code
python python_interpreter.py -c "print('hello')"

# Interactive mode
python python_interpreter.py
```
