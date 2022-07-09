iota_counter = 0

def com(prog):
    with open(sys.argv[1], "w") as f:
        for op in prog:
            if op[0] == PRINT:
                f.write(f"print({op[1]})")
            elif op[0] == EXIT:
                f.write("exit()")
            elif op[0] == DEFINE:
                f.write("def {op[1]}:")

        
