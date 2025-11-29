
from src import LasVegasMAX3SAT, Max3SAT, SATBenchFactory
from typing import Dict
import argparse


class Main:

    """Main class to handle command-line interface for Las Vegas MAX-3SAT."""

    @staticmethod
    def parse_args() -> argparse.Namespace:

        """
        Parse command-line arguments.
        Use --file to specify a single .cnf file or --dir to specify a directory of .cnf files.
        """

        parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Run Las Vegas MAX-3SAT on a single .cnf file or on all .cnf files in a directory.")
        
        # either --file or --dir must be provided, but not both + verbose flag
        group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--file", type=str, help="Path to a single .cnf file.")
        group.add_argument("--dir", type=str, help="Path to a directory containing .cnf files.")
        parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')

        return parser.parse_args()

    @staticmethod
    def single(fp: str, verbose: bool) -> None:

        """
        Run Las Vegas MAX-3SAT on a single .cnf file.
        """

        instance: Max3SAT = SATBenchFactory.from_benchmark_file(fp)
        
        if verbose:
            print(f'[i] Loaded instance from {fp} with {instance.formula.size()} clauses.')

        c, a, i = LasVegasMAX3SAT.run(instance)

        print(f'[r] [{i} it] Maximal clause count = {c} [proportion = {c / instance.formula.size():.4f}]')
        if verbose:
            print(f'[r] Best assignment found:')
            # sort variables for consistent output
            for var in sorted(a.keys()):
                val = a[var]
                print(f'>> [x_{var}] {val}')
        
    @staticmethod
    def batch(dir_path: str, verbose: bool) -> None:

        """
        Run Las Vegas MAX-3SAT on all .cnf files in a directory.
        """

        factory: SATBenchFactory = SATBenchFactory()
        instances: Dict[str, Max3SAT] = factory.from_dir(dir_path)

        for name, instance in instances.items():
            if verbose:
                print(f'[i] Loaded instance {name} with {instance.formula.size()} clauses.')

            c, a, i = LasVegasMAX3SAT.run(instance)

            print(f'[r] [{i} it] Instance: {name} | Maximal clause count = {c} [proportion = {c / instance.formula.size():.4f}]')
            if verbose:
                print(f'[r] Best assignment found:')
                # sort variables for consistent output
                for var in sorted(a.keys()):
                    val = a[var]
                    print(f'>> [x_{var}] {val}')


if __name__ == "__main__":

    # Alternatively, you could import src by yourself and call
    # e.g., LasVegasMAX3SAT.run(...) directly, on a Max3SAT instance you create.
    # Here, we provide a command-line interface for convenience.

    args: argparse.Namespace = Main.parse_args()

    if args.file:
        Main.single(fp=args.file, verbose=args.verbose)
    elif args.dir:
        Main.batch(dir_path=args.dir, verbose=args.verbose)
