import argparse
from apriori import APriori
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
        action="store_const",
        const=True,
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
            naive.run(k)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"Calculating k={k} Elapsed in: {elapsed_time}\n")

    if args.apriori:
        apriori = APriori(args.dataset, 25)
        generator = apriori.run(19)
        start_total_time = time.perf_counter()

        while True:
            try:
                start_time = time.perf_counter()  # Start timing
                (k, result) = next(generator)  # Get the next item from the generator
                end_time = time.perf_counter()  # End timing

                # Output the result and the time taken
                print(result)
                elapsed_time = end_time - start_time
                print(f"Calculating k={k} elapsed in: {elapsed_time}")

            except StopIteration:
                # Break the loop when the generator is exhausted
                break
        end_total_time = time.perf_counter()
        print(f"Calculating till 18 elapsed in: {end_total_time - start_total_time}")
    elif args.apriori:
        for k in range(1, 19):
            apriori = APriori(args.dataset, 25)
            start_time = time.perf_counter()
            apriori.run(k)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"Calculating k={k} Elapsed in: {elapsed_time}\n")



if __name__ == "__main__":
    main()
