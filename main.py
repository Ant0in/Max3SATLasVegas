
from src import LasVegasMAX3SAT, Max3SAT, SATBenchFactory
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
        
        # either --file or --dir must be provided, but not both
        group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--file", type=str, help="Path to a single .cnf file.")
        group.add_argument("--dir", type=str, help="Path to a directory containing .cnf files.")

        # additional parameters
        parser.add_argument("--iteration", type=int, default=1000, help="Maximum iterations for the Las Vegas algorithm.")
        parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')

        return parser.parse_args()

    @staticmethod
    def single(fp: str, maxit: int, verbose: bool) -> None:

        """
        Run Las Vegas MAX-3SAT on a single .cnf file.
        """

        instance: Max3SAT = SATBenchFactory.from_benchmark_file(fp)
        
        if verbose:
            print(f'[i] Loaded instance from {fp} with {instance.formula.size()} clauses.')

        bc, ba = LasVegasMAX3SAT.run(instance, maxit=maxit)

        print(f'[r] Best clause count = {bc} [proportion = {bc / instance.formula.size():.4f}]')
        if verbose:
            print(f'[r] Best assignment found:')
            # sort variables for consistent output
            for var in sorted(ba.keys()):
                val = ba[var]
                print(f'>> [x_{var}] {val}')
        
    @staticmethod
    def batch(dir_path: str, maxit: int, verbose: bool) -> None:

        """
        Run Las Vegas MAX-3SAT on all .cnf files in a directory.
        """

        benchset: dict[str, Max3SAT] = SATBenchFactory.from_dir(dir_path, ext='.cnf')
        
        if verbose:
            print(f'[i] Loaded {len(benchset)} problem instances from {dir_path}.')

        for i, (name, instance) in enumerate(benchset.items()):
            
            if verbose:
                print(f'\n[i] Processing instance {i+1}/{len(benchset)}: {name} with {instance.formula.size()} clauses.')

            bc, ba = LasVegasMAX3SAT.run(instance, maxit=maxit)

            print(f'[r] Instance: {name} | Best clause count = {bc} [proportion = {bc / instance.formula.size():.4f}]')
            if verbose:
                print(f'[r] Best assignment found:')
                # sort variables for consistent output
                for var in sorted(ba.keys()):
                    val = ba[var]
                    print(f'>> [x_{var}] {val}')


if __name__ == "__main__":

    # Alternatively, you could import src by yourself and call
    # e.g., LasVegasMAX3SAT.run(...) directly, on a Max3SAT instance you create.
    # Here, we provide a command-line interface for convenience.

    args: argparse.Namespace = Main.parse_args()

    if args.file:
        Main.single(fp=args.file, maxit=args.iteration, verbose=args.verbose)
    elif args.dir:
        Main.batch(dir_path=args.dir, maxit=args.iteration, verbose=args.verbose)

