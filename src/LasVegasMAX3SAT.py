

import random
from typing import Optional, List, Tuple, Dict, Set, Union


assignment_t = Union[Dict[int, bool], Dict['Literal', bool]]


class Literal:

    """A class representing a literal in a 3-SAT formula (can be negated)."""

    def __init__(self, id: int, negative: bool = False) -> None:

        """Initialize a Literal with a variable number and a negation flag."""

        self._id: int = id
        self._negative: bool = negative

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def negative(self) -> bool:
        return self._negative

    def evaluate(self, assignment: assignment_t) -> Optional[bool]:

        """
        Evaluate the literal based on its assigned value. \n
        Raises a `ValueError` if the literal has no assigned value.
        """

        if self._id not in assignment:
            raise ValueError(f"[e] Literal x_{self._id} has no assigned value.")

        value: bool = assignment[self._id]
        return not value if self._negative else value
    
    def __repr__(self) -> str:
        return f"{'-' if self._negative else ''}x_{self._id}"

    def __hash__(self) -> int:
        return hash((self._id, self._negative))

class Clause:

    """A class representing a clause in a 3-SAT formula (contains up to 3 literals)."""

    def __init__(self, literals: List[Literal]) -> None:

        """Initialize a Clause with a list of up to 3 Literals."""
        self._literals: List[Literal] = literals

    @property
    def literals(self) -> Tuple[Literal, ...]:
        """Return the literals in the clause as a tuple."""
        return tuple(self._literals)

    def size(self) -> int:
        """Return the number of literals in the clause."""
        return len(self._literals)

    def __repr__(self) -> str:
        return " v ".join([str(l) for l in self._literals])
    
    def is_satisfied(self, assignment: assignment_t) -> bool:

        """Check if the clause is satisfied based on the evaluation of its literals."""

        # for each literal in the clause, if there is a True, since its a disjunction, return True
        # if all literals are False, return False

        for l in self._literals:
            if l.evaluate(assignment):
                return True

        if all(not l.evaluate(assignment) for l in self._literals):
            return False

        # not suppoed to reach here, since unassigned literals should raise an error        
        raise ValueError("[e] Clause was likely empty or literals were unassigned.")

class Formula:

    """A class representing a SAT formula (a conjunction of clauses)."""

    def __init__(self, clauses: List[Clause]) -> None:
        """Initialize a Formula with a list of Clauses."""
        self._clauses: List[Clause] = clauses

    @property
    def clauses(self) -> Tuple[Clause, ...]:
        """Return the clauses in the formula as a tuple."""
        return tuple(self._clauses)

    def size(self) -> int:
        """Return the number of clauses in the formula."""
        return len(self._clauses)

    def __repr__(self) -> str:
        return " ^ ".join([f"({str(c)})" for c in self._clauses])
    
    def is_satisfied(self, assignment: assignment_t) -> bool:

        """Check if the formula is satisfied based on the evaluation of its clauses."""

        # for each clause in the formula, if there is a False, since its a conjunction, return False
        # if all clauses are True, return True

        for c in self._clauses:
            if not c.is_satisfied(assignment):
                return False
        
        if all(c.is_satisfied(assignment) for c in self._clauses):
            return True
        
        # not suppoed to reach here, since unassigned clauses should raise an error
        raise ValueError("[e] Formula was likely empty or clauses were unassigned.")

class Max3SAT:

    """A class representing the MAX 3-SAT problem."""

    def __init__(self, formula: Formula) -> None:
        """Initialize a Max3SAT instance with a given formula."""
        assert all(clause.size() <= 3 for clause in formula.clauses), "[w] All clauses must have at most 3 literals."
        self._formula: Formula = formula

    @property
    def formula(self) -> Formula:
        """Return the formula associated with this Max3SAT instance."""
        return self._formula
    
    def all_literals(self) -> Set[Literal]:

        """Return a set of all literals in the formula."""

        literals_set: Set[Literal] = set()

        for clause in self._formula.clauses:
            for literal in clause.literals:
                literals_set.add(literal)

        return literals_set
    
    def count_satisfied_clauses(self, assignment: assignment_t) -> int:
        """Count the number of satisfied clauses in the formula."""
        return sum(1 for clause in self._formula.clauses if clause.is_satisfied(assignment))
    
    def __repr__(self) -> str:
        return str(self._formula)
    

class LasVegasMAX3SAT:

    """A class implementing the Las Vegas algorithm for the MAX 3-SAT problem."""

    @staticmethod
    def random_assignment(literals: List[Literal]) -> assignment_t:

        """Generate a random assignment for the given literals."""

        assignment: Dict[Literal, bool] = dict()
        for l in literals:
            value: bool = random.choice([True, False])
            assignment[l.id] = value
        return assignment

    @staticmethod
    def run(max3sat: Max3SAT) -> Tuple[int, assignment_t]:

        """
        Run the Las Vegas algorithm to find an assignment that maximizes at least 7/8 of the clauses and
        yield the number of satisfied clauses along with the corresponding assignment.
        """

        literals: List[Literal] = list(max3sat.all_literals())
        
        # repeat until a satisfactory assignment is found
        while True:
            
            assignment: assignment_t = LasVegasMAX3SAT.random_assignment(literals)
            satisfied_clauses: int = max3sat.count_satisfied_clauses(assignment)

            # uses the karloff-zwick bound of 7/8
            if satisfied_clauses >= (7 / 8) * max3sat.formula.size():
                return satisfied_clauses, assignment
        

