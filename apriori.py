from collections import defaultdict
import itertools
import polars as pl
import mmap
import os
import operator

class APriori():
    """
    Class to configure and run apriori algorithm on given dataset
    """

    df: pl.DataFrame
    dataset: str
    # for tiny and medium <=5
    # for larger <= 25
    treshold: int
    singleton_map: dict[frozenset, int] = {}
    pairs_map: dict[frozenset, int] = {}

    prev_map: dict[frozenset, int] = {}
    curr_map: dict[frozenset, int] = {}

    method_treshold = 6

    def __init__(self, dataset_path: str, treshold = 25):
        self.treshold = treshold
        self.dataset = dataset_path
        self.df =(
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
        # self.df = open(dataset_path, "r")

    """
    pass 1: frequent singletons
        count support every singelton
        filter out non-frequent ones
    pass 2: find frequent pairs

    pass 3: find frequent triples
    ...

    pair (i, j):
        if i and j are frequent -> count (i, j)
    """
    def run(self, k: int):
        self.count_singletons()
        self.filter_singletons()
        self.prev_map = self.singleton_map
        for pass_nr in range(2,k+1):
            self.count(pass_nr)
            self.filter(pass_nr)

            self.prev_map = self.curr_map
            self.curr_map = {}

        if len(self.prev_map) > 0:
            print(max(self.prev_map.items(), key=operator.itemgetter(1)))



    # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    # frequent : {1, 2, 3, 4, 5}
    # frequent pairs : {1, 2}, {2, 3}, {3, 4}, and {4, 5} => l_k_prev
    # find frequent triples
    # basket =  {2, 3, 4, 5}
    # possible triples: {2, 3, 4}, {2, 3, 5}, {2, 4, 5}, {3, 4, 5}, {}
    # C_K:
    #   {2, 3, 4}: {2, 3}, {2, 4}, {3, 4} => no
    #   {2, 3, 5}: {2, 3}, {2, 5}, {3, 5} => no
    # L_K: prune C_K based on treshold

    # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    # frequent = {1, 3, 4, 6, 7, 9}
    # example basket: {2, 4, 6, 9}
    # possible pairs: {2, 4}, {2, 6}, {2, 9}, {4, 6}, {4, 9}, {6, 9}
    # {2, 4}? {2}, {4} => no
    # {4, 6}? {4}, {6} => yes, cuz 4 and 6 are in frequent
    def count(self, k: int):
        for (basket, ) in self.df.iter_rows():
            possible_candidates = itertools.combinations(basket, k - 1)

            c_k = set()
            if k < self.method_treshold:
                for pc in possible_candidates:
                    pc = frozenset(pc)
                    if pc in self.prev_map:
                        c_k = c_k.union(pc)

            else:
                for pc in self.prev_map:
                    if pc.issubset(basket):
                        c_k = c_k.union(pc)

            unions = itertools.combinations(c_k, k)
            for candidate in unions:
                key = frozenset(candidate)
                self.curr_map[key] = self.curr_map.get(key, 0) + 1


    def filter(self, k: int):
        self.curr_map = dict(
            filter(lambda item: item[1] > self.treshold, self.curr_map.items())
        )


    def count_singletons(self):
        for (row,) in self.df.iter_rows():
            for el in row:
                key = frozenset([el])
                self.singleton_map[key] = self.singleton_map.get(key, 0) + 1

    def filter_singletons(self):
        self.singleton_map = dict(
            filter(lambda item: item[1] > self.treshold, self.singleton_map.items())
        )

    def count_pairs(self):
        # generate pairs from singleton_map
        for (row, ) in self.df.iter_rows():
            # voor elke item in basket die frequent is -> sla ze op
            # genereer pairs van deze items en tel op
            #
            frequent_singletons = itertools.chain.from_iterable(self.prev_map.keys())
            for candidate in itertools.combinations(filter(lambda item: item in frequent_singletons, row), 2):
                self.pairs_map[candidate] = self.pairs_map.get(candidate, 0) + 1


    def filter_pairs(self):
        self.pairs_map = dict(
            filter(lambda item: item[1] > self.treshold, self.pairs_map.items())
        )
