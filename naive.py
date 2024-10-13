from collections import defaultdict
import itertools
import os
import polars as pl
import operator

class Naive():

    # frozenset is set of authers
    counter: defaultdict[frozenset[str], int] = defaultdict()
    df: pl.DataFrame
    def __init__(self, dataset_path: str) -> None:
        self.df = (
            pl.read_csv(dataset_path,
                has_header=False,
                new_columns=["names"],
                separator="\n",
                n_threads=os.cpu_count()
            )
            .with_columns(
                pl.col("names").str.split(",").alias("names")
            )
        )

    def run(self, k: int):
        """
        Entry point of naive implemenation

        It returns the maximal author set of size `k` using a very naive implementation
        """
        self.counter = defaultdict()

        # we can filter anything below k because it isnt requested
        for (authors,) in self.df.filter(pl.col("names").list.len() >= k).iter_rows():
            for combination in itertools.combinations(authors, k):
                key = frozenset(combination)
                self.counter[key] = self.counter.get(key, 0) + 1
        if (self.counter):
            return (k, max(self.counter.items(), key=operator.itemgetter(1)))
        else:
            (k, None)

    def create_markdown_table(self, data: list[tuple[int, frozenset[str], int, float]]) -> str:
        """
        Creates a Markdown table for the results given by running the naive implemenation on multiple `k`'s
        
        The format of the table is:

        | k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
        """
        markdown = "| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |\n"
        markdown +="|---|------------|---------|------------------|---------------------|\n"
        cumulative_time = 0
        for (k, subset, support, time_elapsed) in data:
            cumulative_time += time_elapsed
            subset_str = ", ".join(subset)
            markdown += f"| {k} | {subset_str} | {support} | {time_elapsed:.6f} | {cumulative_time:.6f} |\n"
        return markdown