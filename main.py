
from src import LasVegasMAX3SAT, Max3SAT, SATBenchFactory


if __name__ == "__main__":

    benchset: dict[str, Max3SAT] = SATBenchFactory.from_dir(r'./cnf_bench', ext='.cnf')
    print(f'[i] Loaded {len(benchset)} problem instances from benchmark directory.')

    for i, instance in enumerate(benchset.values()):
        bc, _ = LasVegasMAX3SAT.run(instance, maxit=1000)
        print(f'[i] Instance {i}: Best clause count = {bc} [proportion = {bc / instance.formula.size():.4f}]')

