from collections import defaultdict
import itertools
import os
import polars as pl
from pprint import pprint
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

    def run(self, k: int) -> None:
        self.counter = defaultdict()

        # we can filter anything below k because it isnt requested
        for (authors,) in self.df.filter(pl.col("names").list.len() >= k).iter_rows():
            for combination in itertools.combinations(authors, k):
                key = frozenset(combination)
                self.counter[key] = self.counter.get(key, 0) + 1
        if (self.counter):
            print(max(self.counter.items(), key=operator.itemgetter(1)))
        else:
            print(f"Maximal author set of size {k} doesnt exist")
        #print(max(self.counter.items(), key=lambda x: x[1]))
