from typing import List, Tuple
import os
import subprocess

Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]


def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    # self explanatory.
    print(len(clauses))
    fstring = f"p cnf {nb_vars} {len(clauses)}"
    for clause in clauses:
        fstring += "\n"
        for litteral in clause:
            fstring += f" {litteral} 0" # litteral => string
    return fstring + " " # espace pour le parsing nul de gophersat -1 char


def write_dimacs_file(dimacs: str, filename: str):
    filename = os.path.join(os.getcwd(), filename)
    print(filename)

    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    
    filename = os.path.join(os.getcwd(), filename)
    print(filename)
    
    result = subprocess.run(
        [cmd, filename], encoding=encoding,
        capture_output=True, check=True, shell=True
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]


def main():
    clauses = [[1], [2]]

    dimacs = clauses_to_dimacs(clauses, 2)

    write_dimacs_file(dimacs, "dimacs.cnf")
    ret = exec_gophersat("dimacs.cnf")
    print(ret)

if __name__ == "__main__":
    main()