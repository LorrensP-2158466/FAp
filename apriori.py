from collections import Counter, defaultdict
import itertools
import polars as pl
import functools
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
    singleton_map: defaultdict[frozenset, int] = defaultdict(int)
    pairs_map: defaultdict[frozenset, int] = defaultdict(int)

    prev_map: defaultdict[frozenset, int] = defaultdict(int)
    curr_map: defaultdict[frozenset, int] = defaultdict(int)


    def __init__(self, dataset_path: str, treshold = 5):
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
        self.produce_frequent_singletons()
        yield (1, max(self.singleton_map.items(), key=operator.itemgetter(1)))

        self.produce_frequent_pairs()
        self.prev_map = self.pairs_map
        yield (2, max(self.prev_map.items(), key=operator.itemgetter(1)))

        for pass_nr in range(3,k+1):
            self.count(pass_nr)
            self.filter()

            self.prev_map = self.curr_map
            self.curr_map = defaultdict(int)
            if len(self.prev_map) > 0:
                yield (pass_nr, max(self.prev_map.items(), key=operator.itemgetter(1)))
            else:
                return



    # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    # frequent : {1, 2, 3, 4, 5}
    # frequent pairs : {1, 2}, {2, 3}, {3, 4}, and {4, 5} => l_k_prev
    # find frequent triples
    # basket =  {2, 3, 4, 5}
    # possible triples: {2, 3, 4}, {2, 3, 5}, {2, 4, 5}, {3, 4, 5}
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
        prev_frequents = frozenset(itertools.chain.from_iterable(self.prev_map))
        self.df = self.df.filter(pl.col("names").list.len() >= k)
        for (basket, ) in self.df.iter_rows():
            # only take authors that where frequent in the previous iteration
            pruned_basket = prev_frequents.intersection(basket)

            # create L_{k-1} from those authors
            possible_candidates = itertools.combinations(pruned_basket, k-1)

            # elements that, when combined into k combinations
            # will result in a candidate
            c_k = functools.reduce(
                frozenset.union, 
                filter(
                    lambda pc: pc in self.prev_map, 
                    map(frozenset, possible_candidates)
                ),
                frozenset()
                )

            # create the candidates and count them up
            for candidate in map(frozenset,itertools.combinations(c_k, k)):
                self.curr_map[candidate] +=  1


    # filter candidates based on treshold
    def filter(self):
        self.curr_map = defaultdict(
            int,
            filter(lambda item: item[1] > self.treshold, self.curr_map.items())
        )


    def produce_frequent_singletons(self):
        df = (self.df
            .explode("names")
            .group_by("names")
            .agg(pl.count())
            .filter(pl.col("count") > self.treshold)
        )
        self.singleton_map = defaultdict(int, map(lambda row: (frozenset((row[0],)), row[1]), df.iter_rows()))

    def produce_frequent_pairs_(self):
        prev_frequents = frozenset(itertools.chain.from_iterable(self.singleton_map))
        print(prev_frequents)
        
        # Use Counter for efficient counting
        pair_counter = Counter()
        
        for pruned_basket in map(
                lambda b: prev_frequents.intersection(b[0]), 
                self.df.filter(pl.col("names").list.len() >= 2).iter_rows()):
            print(pruned_basket)
            
            pair_counter.update(map(frozenset, itertools.combinations(pruned_basket, 2)))
        

        self.pairs_map.update(pair_counter)
        self.filter_pairs()
    
    def produce_frequent_pairs(self):
        prev_frequents = frozenset(itertools.chain.from_iterable(self.singleton_map))
        df = self.df.filter(pl.col("names").list.len() >= 2)
        for (basket, ) in df.iter_rows():
            pruned_basket = prev_frequents.intersection(basket)

            # create the candidates and count them up
            for candidate in map(frozenset,itertools.combinations(pruned_basket, 2)):
                self.pairs_map[candidate] += 1
        
        self.filter_pairs()

    # not this
    def produce_frequent_pairs_v2(self):
        df = self.df.filter(pl.col("names").list.len() >= 2)
        for pruned_basket in  map(
                lambda row: filter(
                    lambda x: x in self.singleton_map, row[0]),
                     df.iter_rows()
                ):

            # create the candidates and count them up
            for candidate in map(frozenset,itertools.combinations(pruned_basket, 2)):
                self.pairs_map[candidate] += 1
        
        self.filter_pairs()


    def filter_pairs(self):
        self.pairs_map = defaultdict(
            int,
            filter(lambda item: item[1] > self.treshold, self.pairs_map.items())
        )
