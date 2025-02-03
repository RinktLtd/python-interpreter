import sys
import code
import os

def execute_command(cmd):
    try:
        exec(cmd)
    except Exception as e:
        print(f"Error executing the command: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Check if the first argument is "-c"
        if sys.argv[1] == "-c":
            # Ensure there is a code argument after "-c"
            if len(sys.argv) > 2:
                code_to_run = sys.argv[2]
                execute_command(code_to_run)
            else:
                print("Error: '-c' flag provided but no code given", file=sys.stderr)
                sys.exit(1)
        else:
            arg = sys.argv[1]
            if os.path.isfile(arg):
                try:
                    # If a script file is provided as an argument, execute it
                    exec(open(arg).read())
                except Exception as e:
                    print(f"Error executing the script: {e}", file=sys.stderr)
                    sys.exit(1)
            else:
                # If the argument is not a file, treat it as a Python command
                execute_command(arg)
    else:
        # No arguments provided, start an interactive interpreter
        print("Python " + sys.version)
        print("Type 'exit()' or 'quit()' to exit the interpreter.")
        code.interact(local=locals())
