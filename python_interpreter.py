import code
import os
import sys
import traceback


def run(source, filename):
    # os and sys stay importless: scripts ran in this launcher's own namespace
    # before, and some came to rely on it.
    namespace = {"__name__": "__main__", "__file__": filename, "os": os, "sys": sys}
    try:
        exec(compile(source, filename, "exec"), namespace)
    except SystemExit:
        raise
    except BaseException as e:
        # Drop this launcher's frame so the trace starts in the user's script.
        traceback.print_exception(e.with_traceback(e.__traceback__.tb_next))
        sys.exit(1)


def interact():
    print("Python " + sys.version)
    print("Type 'exit()' or 'quit()' to exit the interpreter.")
    code.interact(local={"__name__": "__main__"})


if __name__ == "__main__":
    args = sys.argv[1:]
    # A frozen executable ignores -u, so honour it here: without line buffering
    # a piped stdout reaches the runner only when the script ends. The runner
    # reads UTF-8, while a piped stdout on Windows defaults to the ANSI codepage
    # and raises on the first character outside it.
    unbuffered = bool(args) and args[0] == "-u"
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", line_buffering=unbuffered or None)
    if unbuffered:
        args = args[1:]

    if not args:
        interact()
    elif args[0] == "-c":
        if len(args) < 2:
            print("Error: '-c' flag provided but no code given", file=sys.stderr)
            sys.exit(1)
        sys.argv = ["-c", *args[2:]]
        run(args[1], "<string>")
    elif os.path.isfile(args[0]):
        sys.argv = args
        # Bytes, so compile() decodes them as CPython would: UTF-8 unless a
        # coding cookie says otherwise, with a BOM allowed.
        with open(args[0], "rb") as f:
            run(f.read(), args[0])
    else:
        sys.argv = ["-c", *args[1:]]
        run(args[0], "<string>")
