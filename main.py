import argparse
from apriori import APriori
import data_exploration
from naive import Naive
import time

def initialize_args_parser() -> argparse.ArgumentParser:


    parser = argparse.ArgumentParser(description="BDA Project frequent itemsets and apriori")


    parser.add_argument(
        "--dataset",
        help="Path to dataset file",
        metavar="DATASET_PATH",
        required=True,
    )


    subparsers = parser.add_subparsers(dest="command", required=True)


    expl_parser = subparsers.add_parser("data-expl", help="Perform data exploration")
    expl_parser.add_argument(
        "--explorations",
        nargs="*",
        choices=data_exploration.DataExplorer.choices,
        help="Choose one or more data explorations to perform on the dataset.",
    )


    subparsers.add_parser("naive", help="Run naive implementation")


    apriori_parser = subparsers.add_parser("apriori", help="Run apriori implementation")
    apriori_parser.add_argument(
        "--treshold",
        help="Set threshold for apriori algorithm",
        type=int,
        default=5,
    )

    apriori_parser.add_argument(
        "--k",
        help="Untill which size of maximal author set you want to calculate",
        type=int,
        default=20
    )

    return parser

def main():
    parser = initialize_args_parser()
    args = parser.parse_args()

    if args.command == "data-expl":
        explorer = data_exploration.DataExplorer(args.dataset)
        print(explorer.perform(args.data_expl))

    elif args.command == "naive":
        naive = Naive(args.dataset)
        for k in range(1, 20):
            # run fully_df
            start_time = time.perf_counter()
            naive.run(k)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"Calculating k={k} Elapsed in: {elapsed_time}\n")

    elif args.command == "apriori":
        apriori = APriori(args.dataset, args.treshold)
        generator = apriori.run(args.k)
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
        print(f"Calculating till {k} elapsed in: {end_total_time - start_total_time}")

if __name__ == "__main__":
    main()
