import sys
import lexer
import subprocess
import pickle
import base64


code = subprocess.check_output(("m4", "-I", "stdlib"), stdin=sys.stdin)
tokens = lexer.lex(code.decode("UTF-8"))
for token in tokens:
    print("{} {}".format(
        token.type,
        base64.b64encode(str(token.value).encode("UTF-8")).decode("ASCII"),
    ))
