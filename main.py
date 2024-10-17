import argparse
from pprint import pprint
from apriori import APriori
import data_exploration
from naive import Naive
import time

def prog_usage(name=None):                                                            
    return (
'''%(prog)s [ARGS] [SUBCOMMAND] [SUBCOMMAND ARGS]

ARGS:
    --md                  Output the results of th subcommand in a  markdown table
    --dataset DATASETPATH Set the dataset path the subcommand should use

SUBCOMMAND:
    data-expl Perform the data explorations
    naive     Perform the naive algorithm on the dataset
    apriori   Perform the apriori algorithm on the dataset

SUCOMMAND ARGS:
    data-expl:
        --explorations=[DATA_EXPLS] Choose one or more data explorations to perform on the dataset.
        --output-ppa                Output `papers_per_auhtor` technique to a csv file
    naive:
        --k Which maximal author set you would like to calculate
    apriori:
        --k int        Till which maximal author set you would like to calculate (this also outputs intermediate results)
        --treshold int Set the treshold for the apriori algorithm

DATA_EXPLS:
    You can define multiple data_explorations seperated by a comma
    all // does all the explorations
    amt_publications, average_amt_authors, unique_authors, papers_per_author, average_paper_per_author, 
    count_marc_dirk, most_papers_published_by_one_author, median_amt_authors
''')


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
    parser = argparse.ArgumentParser(description="BDA Project frequent itemsets and apriori", usage=prog_usage(),epilog=None)

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

    expl_parser.add_argument(
        "--output-ppa",
        help="Output `papers_per_auhtor` technique to a csv file",
        action="store_const",
        const=True
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
        results = explorer.perform(args.explorations)
        if args.md:
            print(explorer.create_markdown_table(results, args.output_ppa))
        else:
            pprint(results)

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
        apriori = APriori(args.dataset, args.treshold) # default treshold is 5
        generator = apriori.run(args.k) # default k = 20
        cummulative_time = 0
        results = []
        while True:
            try:
                # Get next authorset and time how long that takes
                start_time = time.perf_counter() 
                (k, result) = next(generator)  
                end_time = time.perf_counter()  
                elapsed_time = end_time - start_time
                cummulative_time += elapsed_time
                if result is not None:
                    (author_set, support) = result
                    results.append((k, author_set, support, elapsed_time))
                print(f"Result of k={k}: {result}; elapsed in: {elapsed_time}")
            except StopIteration:
                # Break the loop when the generator is exhausted
                break
        if args.md:
            print(apriori.create_markdown_table(results))
        print(f"Calculating till {k} elapsed in: {cummulative_time}")

if __name__ == "__main__":
    main()
