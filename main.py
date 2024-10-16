import argparse
from apriori import APriori
import data_exploration
from naive import Naive
import time

def initialize_args_parser() -> argparse.ArgumentParser:
    """
    Creates the argument parser for the program

    There are 2 arguments:
        - dataset | give the dataset to perform the different subcommands on
        - md | create markdown tables from results

    It has 3 subcommands:
        - data-expl | perform data exploration
        - naive
        - apriori

    Naive has 1 extra argument:
        - k | till which k (size of maximal authorset) we want to calculate

    Apriori has 2 extra arguments:
        - treshold | specify the treshold the algorithm should use
        - k | till which k (size of maximal authorset) we want to caluclate
    """
    parser = argparse.ArgumentParser(description="BDA Project frequent itemsets and apriori")

    parser.add_argument(
        "--dataset",
        help="Path to dataset file",
        metavar="DATASET_PATH",
        required=True,
    )

    parser.add_argument(
        "--md",
        help="Create MarkDown Table from results",
        action="store_const",
        const=True
    )


    subparsers = parser.add_subparsers(dest="command", required=True)

    expl_parser = subparsers.add_parser("data-expl", help="Perform data exploration")
    expl_parser.add_argument(
        "--explorations",
        nargs="*",
        choices=data_exploration.DataExplorer.choices,
        help="Choose one or more data explorations to perform on the dataset.",
    )


    naive_parser = subparsers.add_parser("naive", help="Run naive implementation")
    naive_parser.add_argument(
        "--k",
        help="Untill which size of maximal author set you want to calculate",
        type=int,
        default=20
    )

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
        results = []
        for k in range(1, args.k + 1): # default k = 20
            # run fully_df
            start_time = time.perf_counter()
            result = naive.run(k)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            if result is not None:
                (k, (author_set, support)) = result
                results.append((k, author_set, support, elapsed_time))
            print(result)
            print(f"Calculating k={k} Elapsed in: {elapsed_time}\n")
        if args.md:
            print("\nMARKDOWN TABLE:")
            print(naive.create_markdown_table(results))

    elif args.command == "apriori":
        # apriori = APriori(args.dataset, args.treshold) # default treshold is 5
        # generator = apriori.generate(args.k) # default k = 20
        # cummulative_time = 0
        # results = []
        # while True:
        #     try:
        #         start_time = time.perf_counter() 
        #         (k, result) = next(generator)  
        #         end_time = time.perf_counter()  
        #         elapsed_time = end_time - start_time
        #         cummulative_time += elapsed_time
        #         if result is not None:
        #             (author_set, support) = result
        #             results.append((k, author_set, support, elapsed_time))
        #         print(f"Result of k={k}: {result}; elapsed in: {elapsed_time}")
        #     except StopIteration:
        #         # Break the loop when the generator is exhausted
        #         break
        # if args.md:
        #     print(apriori.create_markdown_table(results))
        # print(f"Calculating till {k} elapsed in: {cummulative_time}")
        apriori = APriori(args.dataset, args.treshold)
        start = time.perf_counter()
        apriori.calculate_maximal_authorset(20)
        end = time.perf_counter()
        print(f"Calculating maximal author set of k=20 elapsed in: {end-start}")

if __name__ == "__main__":
    main()
