import sys

def run_code(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"): 
            continue
        
        # Split command from the rest of the line
        parts = line.split(" ", 1)
        command = parts[0]

        if command == "SAY":
            # Print text after SAY
            print(parts[1])
            
        elif command == "ADD":
            # Split numbers by '+' and print sum
            numbers = parts[1].split("+")
            num1 = int(numbers[0].strip())
            num2 = int(numbers[1].strip())
            print(num1 + num2)
            
        else:
            print(f"Error: Unknown command '{command}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <filename.n>")
    else:
        run_code(sys.argv[1])
