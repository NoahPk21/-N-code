import sys
import re

class NInterpreter:
    def __init__(self):
        self.variables = {}

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"):
            return

        # 1. Handle LOG command
        if line.startswith("-log"):
            match = re.match(r'-log\((.*?)\);', line)
            if match:
                content = match.group(1).strip('"\'')
                print(content)
            return

        # 2. Handle SET command
        if line.startswith("-set"):
            match = re.match(r'-set\s+(\w+)\s*=\s*(.*?);', line)
            if match:
                var_name = match.group(1)
                var_val = match.group(2).strip('"\'')
                # Try to convert to integer if possible
                try:
                    self.variables[var_name] = int(var_val)
                except ValueError:
                    self.variables[var_name] = var_val
            return

        # 3. Handle RUN command
        if line.startswith("-run"):
            match = re.match(r'-run\s+(\w+)\((.*?)\);', line)
            if match:
                func_name = match.group(1)
                args = [arg.strip().strip('"\'') for arg in match.group(2).split(',')]
                self.execute_function(func_name, args)
            return

    def execute_function(self, func, args):
        if func == "add":
            var_name, val = args[0], int(args[1])
            if var_name in self.variables:
                self.variables[var_name] += val
                print(f"[SYSTEM] Added {val} to {var_name}. New value: {self.variables[var_name]}")
        elif func == "sub":
            var_name, val = args[0], int(args[1])
            if var_name in self.variables:
                self.variables[var_name] -= val
        elif func == "theme":
            print(f"[UI] Changing window theme to: {args[0].upper()}")
        elif func == "title":
            print(f"[UI] Setting window title to: {args[0]}")
        elif func == "user":
            # Resolve variable name if passed instead of raw string
            username = self.variables.get(args[0], args[0])
            print(f"[USER] Logged in as: {username}")
        else:
            print(f"[WARNING] Function '{func}' not yet implemented.")

    def run_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                self.parse_line(line)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <filename.n>")
    else:
        interpreter = NInterpreter()
        interpreter.run_file(sys.argv[1])
