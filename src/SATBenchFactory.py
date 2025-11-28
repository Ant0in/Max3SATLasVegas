
import os
from typing import List, Dict

from .LasVegasMAX3SAT import Literal, Clause, Formula, Max3SAT



class SATBenchFactory:

    """A factory class for creating MAX 3-SAT problem instances from benchmark files."""

    @staticmethod
    def _read(fp: str) -> List[str]:

        """Read the contents of a file and return them as a list of lines."""

        with open(fp, 'r') as f:
            lines: List[str] = f.readlines()
        return lines

    @staticmethod
    def _parse(lines: List[str]) -> Max3SAT:

        """Parse the lines of a benchmark file to create a Max3SAT instance."""

        clauses: List[Clause] = []

        for line in lines:

            line: str = line.strip()
            if line.startswith('p') or line.startswith('c') or \
                line.startswith('%') or line.startswith('0') or line == '':
                continue

            literals: List[Literal] = []
            for literal_str in line.split():
                literal_int: int = int(literal_str)
                if literal_int == 0:
                    continue
                variable: int = abs(literal_int) - 1
                is_positive: bool = literal_int > 0
                literals.append(Literal(variable, is_positive))

            clause = Clause(literals)
            clauses.append(clause)

        formula = Formula(clauses)
        max3sat_instance = Max3SAT(formula)
        return max3sat_instance
    
    @classmethod
    def from_benchmark_file(cls, fp: str) -> Max3SAT:

        """Create a Max3SAT instance from a benchmark file."""

        lines: List[str] = cls._read(fp)
        max3sat_instance: Max3SAT = cls._parse(lines)
        return max3sat_instance
    
    @classmethod
    def from_dir(cls, directory: str, ext: str = '.cnf') -> Dict[str, Max3SAT]:
        
        """Create Max3SAT instances from all benchmark files in a directory."""

        instances: Dict[str, Max3SAT] = {}

        for filename in os.listdir(directory):
            if filename.endswith(ext):

                fp: str = os.path.join(directory, filename)
                instance: Max3SAT = cls.from_benchmark_file(fp)
                instances[filename] = instance

        return instances
