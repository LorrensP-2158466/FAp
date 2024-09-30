from typing import Callable, Self
import polars as pl
import os



type ExplorerResult = tuple[str, int]

class DataExplorer():
    '''
    Can perform different types of data explorations on a given dataset
    '''
    # when adding a function 
    # add that name to this list:
    choices = ["all", "default", "amt_publications", "average_amt_authors", "unique_authors","papers_per_author", "average_paper_per_author"]

    dataset_path: str
    def __init__(self, dataset_path: str) -> None:
        self.dataset_path = dataset_path


    def perform_all(self) -> list[ExplorerResult]:
        pass

    def perform_default(self) -> list[ExplorerResult]:
        pass


    def amt_publications(self, df: pl.DataFrame) -> int:
        return df.height
    
    def unique_authors(self, df: pl.DataFrame) -> int:
        return (
            df
            .select(pl.col("names").explode().alias("all_names"))
            .unique("all_names")
            .height
        )

    def average_amt_authors(self, df: pl.DataFrame) -> int:
        df = df.with_columns(
                pl.col("names").list.len().alias("len_names") 
            )
        return df["len_names"].mean()


    def median_amt_authors(self) -> int:
        pass


    def papers_per_author(self, df: pl.DataFrame) -> int:
        result = (df
            .select(pl.col("names").explode().alias("names"))
            .group_by("names")
            .agg(pl.count().alias("count")))
        print(result)
        return 0
    
    def average_paper_per_author(self, df: pl.DataFrame) -> int:
        unique_authors = self.unique_authors(df)
        return df.height / unique_authors if unique_authors > 0 else 0
    

    def perform(self, functions: list[str]) -> list[ExplorerResult]:
        if "all" in functions:
            return self.perform_all()
        if "default" in functions:
            return self.perform_default()
                # Use read_csv to read the file
        df = (
            pl.read_csv(self.dataset_path, 
                        has_header=False,  # No header in the file
                        new_columns=["names"],
                        separator=";",
                        n_threads=os.cpu_count()
                        )
            .with_columns(
                pl.col("names").str.split(",").alias("names")
            )
        )
        results: list[ExplorerResult] = []

        for func in functions:
            match func:
                case "all" | "default": ()
                case "amt_publications":
                    results.append((func, self.amt_publications(df)))
                case "average_amt_authors": 
                    results.append((func, self.average_amt_authors(df)))
                case "unique_authors":
                    results.append((func, self.unique_authors(df)))
                case "papers_per_author":
                    results.append((func, self.papers_per_author(df)))
                case "average_paper_per_author":
                    results.append((func, self.average_paper_per_author(df)))
                case _:
                    print(f"Unknown data exploration method: {func}")
        return results
        

    # TODO: implement different types of explorations
    '''
    Amt of publications: Lorrens | done
    Unique authors: Lorrens | done
    Average amount of papers per author: Lorrens
    average amount of authors: Ivan
    median amount of authors: Ivan
    number of papers per author: Lorrens/Ivan | done
    '''
