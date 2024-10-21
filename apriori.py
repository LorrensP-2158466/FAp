from collections import defaultdict
import itertools
import polars as pl
import os
import operator

# using list/set comprehension seems to be faster than
# using map()/filter()/reduce()

class APriori():
    """
    Class to configure and run apriori algorithm on a given dataset

    The main entry point is the "run" method
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
                n_threads=os.cpu_count() # we tested with 1 and we got the same results
            )
            .with_columns(
                pl.col("names").str.split(",").alias("names")
            )
        )


    def run(self, k: int):
        """
        Main entry point of the Apriori implementation
        
        It calculates till the k'th maximal authorset and yields all intermidiate maximal
        author sets
        """
        self.produce_frequent_singletons()
        yield (1, len(self.singleton_map), max(self.singleton_map.items(), key=operator.itemgetter(1)))
        if k == 1:
            return

        self.produce_frequent_pairs()
        self.prev_map = self.pairs_map
        yield (2, len(self.prev_map), max(self.prev_map.items(), key=operator.itemgetter(1)))

        if k == 2:
            return
        for pass_nr in range(3,k+1):
            self.count(pass_nr)
            self.filter()

            self.prev_map = self.curr_map
            self.curr_map = defaultdict(int)
            if len(self.prev_map) > 0:
                yield (pass_nr, len(self.prev_map), max(self.prev_map.items(), key=operator.itemgetter(1)))
            else:
                yield (pass_nr, 0, None) # ofcourse 0 and None
                return 
        return


    def count(self, k: int):
        """
        The count step of the apriori algorithm

        Given a `k` it counts all authorsets of size `k`
        """
        prev_frequents = frozenset(itertools.chain.from_iterable(self.prev_map))
        self.df = self.df.filter(pl.col("names").list.len() >= k)
        
        for (basket, ) in self.df.iter_rows():
            # only take authors that where frequent in the previous iteration
            pruned_basket = prev_frequents.intersection(basket)

            if len(pruned_basket) < k:
                continue
            
            # create L_{k-1} from those authors
            # we are essentialy creating the sets of size k-1
            # that are frequent and consist of elements in this basket.
            # in other words: these are the frequent sets in prev_map (of size k-1)
            # that can be made from elements in this basket
            possible_candidates = {
                pc for pc in itertools.combinations(pruned_basket, k-1)
                if frozenset(pc) in self.prev_map
            }

            # flatten set
            c_k = frozenset().union(*possible_candidates)

            # the frequent sets of size k can only consist of the 
            # elements in c_k => create sets and count them
            for candidate in itertools.combinations(c_k, k):
                self.curr_map[frozenset(candidate)] +=  1


    
    def filter(self):
        """
        Filter the current counter map of author sets so only 
        the frequent ones remain
        """
        self.curr_map = self.filter_(self.curr_map)


    def produce_frequent_singletons(self):
        """
        Optimized implementation for producing all frequent singletons
        """

        # use dataframe and "sql" like methods to count the singletons
        df = (self.df
            .explode("names")
            .group_by("names")
            .agg(pl.count())
            .filter(pl.col("count") > self.treshold)
        )

        self.singleton_map = {
            frozenset([row[0]]): row[1] for row in df.iter_rows()
        }


    def produce_frequent_pairs(self):
        """
        Optimized implemantion for producing all frequent pairs 

        This is a variation of the `count` method but it leaves out the L_{k-1} step because we have easier access
        to the frequent singletons.
        """
        # create set of singleton map to create the pruned basket
        prev_frequents = frozenset(itertools.chain.from_iterable(self.singleton_map))
        df =  self.df.filter(pl.col("names").list.len() >= 2)
        for (basket, ) in df.iter_rows():
            # only take authors that where frequent in the previous iteration
            pruned_basket = prev_frequents.intersection(basket)

            # create the candidates and count them up
            if len(pruned_basket) >= 2:
                for candidate in itertools.combinations(pruned_basket, 2):
                    self.pairs_map[frozenset(candidate)] += 1
        self.filter_pairs()


    def filter_pairs(self):
        """
        Filter step for the candidate pairs
        """
        self.pairs_map = self.filter_(self.pairs_map)


    def filter_(self, map) -> dict:
        return {
            key: value for key, value in map.items() if value > self.treshold
        }

    def create_markdown_table(self, data: list[tuple[int, int, frozenset[str], int, float]]) -> str:
        """
        Creates a Markdown table for the results given by running the apriori implemenation
        
        The format of the table is:

        | k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
        """

        markdown = "| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |\n"
        markdown +="|---|------------|---------|---------------------|------------------|---------------------|\n"
        cumulative_time = 0
        for (k, count_maximals, subset, support, time_elapsed) in data:
            cumulative_time += time_elapsed
            subset_str = ", ".join(subset)
            markdown += f"| {k} | {subset_str} | {support} | {count_maximals} | {time_elapsed:.6f} | {cumulative_time:.6f} |\n"
        return markdown
