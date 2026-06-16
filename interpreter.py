import sys
import re

class NV2GameEngine:
    def __init__(self):
        self.variables = {}
        self.entities = {}  # Tracks spawned objects: {"hero": {"type": "player", "x": 0, "y": 0, "health": 100}}
        self.world_settings = {"name": "Default", "gravity": 0.0, "timescale": 1.0}
        self.skip_block = False

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"):
            return

        if line == "}":
            self.skip_block = False
            return

        if self.skip_block and not line.startswith(("-else", "-check")):
            return

        # 1. World Management (-create world, -set gravity, etc.)
        if line.startswith("-create world"):
            match = re.match(r'-create world\("(.*?)"\);', line)
            if match:
                self.world_settings["name"] = match.group(1)
                print(f"[WORLD] Created game world: '{self.world_settings['name']}'")
            return

        if line.startswith("-set gravity"):
            match = re.match(r'-set gravity\((.*?)\);', line)
            if match:
                self.world_settings["gravity"] = float(match.group(1))
                print(f"[PHYSICS] Gravity configured to: {self.world_settings['gravity']} m/s²")
            return

        # 2. Entity Spawning (-spawn player, -spawn enemy, -spawn object)
        if line.startswith("-spawn"):
            match = re.match(r'-spawn\s+(\w+)\("(.*?)"\s*,\s*(-?\d+)\s*,\s*(-?\d+)\);', line)
            if match:
                ent_type = match.group(1)
                ent_name = match.group(2)
                x = int(match.group(3))
                y = int(match.group(4))
                
                self.entities[ent_name] = {"type": ent_type, "x": x, "y": y, "health": 100}
                print(f"[ENGINE] Spawned {ent_type.upper()} '{ent_name}' at coordinates ({x}, {y})")
            return

        # 3. Entity Manipulation & Variables (-set position, -set health, -set variable)
        if line.startswith("-set position"):
            match = re.match(r'-set position\((.*?)\s*,\s*(.*?)\s*,\s*(.*?)\);', line)
            if match:
                name, x, y = match.group(1), match.group(2), match.group(3)
                if name in self.entities:
                    print(f"[ENGINE] Moved '{name}' to vector position ({x}, {y})")
            return

        if line.startswith("-set"):
            # Checking regular variables
            match = re.match(r'-set\s+(\w+)\s*=\s*(.*?);', line)
            if match:
                var_name = match.group(1)
                var_val = match.group(2).strip('"\'')
                try:
                    self.variables[var_name] = int(var_val)
                except ValueError:
                    self.variables[var_name] = var_val
                print(f"[VARIABLES] Global {var_name} set to: {var_val}")
            return

        # 4. Input Engine Handling (-run input, -check input)
        if line.startswith("-check input"):
            match = re.match(r'-check input\("(.*?)"\)\s*\{', line)
            if match:
                key = match.group(1)
                print(f"[INPUT] Processing controller check for keypress: [{key}]")
            return

        # 5. Core Engine Log System (-log)
        if line.startswith("-log"):
            match = re.match(r'-log\((.*?)\);', line)
            if match:
                content = match.group(1).strip('"\'')
                print(f"[LOG] {content}")
            return

        # 6. Global Run Commands (-run camera, -run ui, -run damage)
        if line.startswith("-run"):
            match = re.match(r'-run\s+(.*?)\((.*?)\);', line)
            if match:
                system_call = match.group(1)
                args = match.group(2).strip('"\'')
                print(f"[SYSTEM CALL] {system_call.upper()} executed with payload: ({args})")
            return

        # Fallback for unrecognized commands
        if not line.startswith(("-if", "-loop")):
            print(f"[PARSE ERROR] Unknown N v2 command sequence: {line}")

    def start_terminal(self):
        print("====================================================")
        print("    -N- LANGUAGE v2 INTERACTIVE ENGINE TERMINAL     ")
        print("    Simulating Worlds, Entities, and Physics API    ")
        print("    Type 'exit' to terminate engine.                ")
        print("====================================================")
        while True:
            try:
                user_input = input("-N v2 > ")
                if user_input.strip().lower() in ("exit", "quit"):
                    print("[ENGINE] System shutdown sequence complete.")
                    break
                self.parse_line(user_input)
            except Exception as e:
                print(f"[ENGINE ERROR] Malformed logic stack: {e}")

if __name__ == "__main__":
    engine = NV2GameEngine()
    engine.start_terminal()
