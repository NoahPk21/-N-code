import sys
import re

class NV2GameEngine:
    def __init__(self):
        self.variables = {}
        self.entities = {}
        self.world_settings = {"name": "Default", "gravity": 0.0, "timescale": 1.0}

    # NEW: Visual map rendering method
    def render_map(self):
        # Create a clean 15x5 grid of empty ground '.'
        grid = [["." for _ in range(15)] for _ in range(5)]
        
        # Place entities onto our grid map
        for name, data in self.entities.items():
            x, y = data["x"], data["y"]
            # Keep positions safely inside our 15x5 visual grid boundaries
            grid_x = max(0, min(14, x))
            grid_y = max(0, min(4, y))
            
            # Use 'P' for players and 'E' for enemies
            grid[grid_y][grid_x] = "P" if data["type"] == "player" else "E"
            
        print("\n--- VISUAL WORLD MAP ---")
        for row in grid:
            print(" ".join(row))
        print("------------------------\n")

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return

        if line.startswith("-create world"):
            match = re.match(r'-create world\("(.*?)"\);', line)
            if match: print(f"[WORLD] Created game world: '{match.group(1)}'")
            return

        if line.startswith("-set gravity"):
            return

        if line.startswith("-spawn"):
            match = re.match(r'-spawn\s+(\w+)\("(.*?)"\s*,\s*(-?\d+)\s*,\s*(-?\d+)\);', line)
            if match:
                ent_type = match.group(1)
                ent_name = match.group(2)
                self.entities[ent_name] = {"type": ent_type, "x": int(match.group(3)), "y": int(match.group(4))}
                print(f"[ENGINE] Spawned {ent_type.upper()} '{ent_name}' at ({match.group(3)}, {match.group(4)})")
                # Render screen automatically when things spawn
                self.render_map()
            return

        if line.startswith("-set position"):
            match = re.match(r'-set position\((.*?)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\);', line)
            if match:
                name = match.group(1)
                if name in self.entities:
                    self.entities[name]["x"] = int(match.group(2))
                    self.entities[name]["y"] = int(match.group(3))
                    print(f"[ENGINE] Moved '{name}'")
                    self.render_map()
            return

    def start_terminal(self):
        print("====================================================")
        print("    -N- LANGUAGE v3 VISUAL MAP ENGINE TERMINAL       ")
        print("====================================================")
        while True:
            try:
                user_input = input("-N v3 > ")
                if user_input.strip().lower() == "exit": break
                self.parse_line(user_input)
            except Exception as e:
                print(f"[ENGINE ERROR] Stack error: {e}")

if __name__ == "__main__":
    engine = NV2GameEngine()
    engine.start_terminal()
