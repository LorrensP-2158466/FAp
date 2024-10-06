import argparse
import data_exploration
from naive import Naive
import time

def initialize_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BDA Project frequent itemsets and apriori")
    group = parser.add_mutually_exclusive_group(required=True)

    # try to make this shit a list like so:
    # main.py --data-expl=[...] 
    # with ... a list of data explorations we like to perform
    #
    # can also be:
    # all = just do it all
    # default = defined in assigment
    group.add_argument(
        "--data-expl",
        nargs="*",
        choices=data_exploration.DataExplorer.choices,
        help="Choose one or more data explorations to perform on the dataset.",
    )

    parser.add_argument(
        "--dataset",
        help="Path to dataset file",
        metavar="DATASET_PATH",
        required=True,
    )


    group.add_argument(
        "--naive",
        help="Run naive impl",
        action="store_const",
        const=True,
        default=False,
    )

    group.add_argument(
        "--apriori",
        help="run apriori impl",
        metavar="",
        default=False
    )

    return parser

def main():
    parser = initialize_args_parser()
    args = parser.parse_args()

    if args.data_expl:
        explorer = data_exploration.DataExplorer(args.dataset)
        print(explorer.perform(args.data_expl))
    if args.naive:
        naive = Naive(args.dataset)
        for k in range(1, 20):
            # run fully_df
            start_time = time.perf_counter()
            naive.run_fully_df(k)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"Calculating k={k} Elapsed in: {elapsed_time}\n")



    


if __name__ == "__main__":
    main()