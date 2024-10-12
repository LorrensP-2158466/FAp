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
    choices = [
                "all", "default", 
               "amt_publications", "average_amt_authors", "unique_authors", "papers_per_author", "average_paper_per_author", 
               "count_marc_dirk", "most_papers_published_by_one_author", "median_amt_authors"
    ]

    df: pl.DataFrame
    def __init__(self, dataset_path: str) -> None:
        self.df = self.__create_dataframe(dataset_path)


    def __create_dataframe(self, dataset_path: str) -> pl.DataFrame:
        return (
            pl.read_csv(dataset_path,
                        has_header=False,  # No header in the file
                        new_columns=["names"],
                        separator=";",
                        n_threads=os.cpu_count()
                        )
            .with_columns(
                pl.col("names").str.split(",").alias("names")
            )
        )


    def set_dataset_path(self, dataset_path: str):
        self.df = self.__create_dataframe(dataset_path)


    def perform_all(self) -> list[ExplorerResult]:
        return [ result for fun in self.choices if (result := self.hanlde_method(fun)) is not None ]


    def perform_default(self) -> list[ExplorerResult]:
        return []


    def amt_publications(self) -> int:
        return self.df.height


    def unique_authors(self) -> int:
        return (
            self.df
            .select(pl.col("names").explode().alias("all_names"))
            .unique("all_names")
            .height
        )


    def average_amt_authors(self) -> int:
        df = self.df.with_columns(
                pl.col("names").list.len().alias("len_names")
            )
        return df["len_names"].mean()


    def count_marc_dirk(self) -> int:
        marc_dirk_counter = 0
        for (row, ) in self.df.iter_rows():
            if "Marc Gyssens" in row and "Dirk Van Gucht" in row:
                marc_dirk_counter += 1
        return marc_dirk_counter


    def median_amt_authors(self) -> int:
        df = self.df.with_columns(
            pl.col("names").list.len().alias("len_names")
        )
        return df["len_names"].median()


    def papers_per_author(self) -> pl.DataFrame:
        result = (
            self.df
            .select(pl.col("names").explode().alias("names"))
            .group_by("names")
            .agg(pl.count().alias("count"))
            )
        print(result)
        return result

    
    def most_papers_published_by_one_author(self) -> int:
        return self.papers_per_author().max()


    def average_paper_per_author(self) -> float:
        unique_authors = self.unique_authors()
        return self.df.height / unique_authors if unique_authors > 0 else 0


    def hanlde_method(self, fun: str) -> ExplorerResult | None:
        match fun:
            case "all" | "default":
                return None  # or some default action
            case "amt_publications":
                return (fun, self.amt_publications())
            case "average_amt_authors":
                return (fun, self.average_amt_authors())
            case "unique_authors":
                return (fun, self.unique_authors())
            case "papers_per_author":
                return (fun, self.papers_per_author())
            case "average_paper_per_author":
                return (fun, self.average_paper_per_author())
            case "count_marc_dirk":
                return(fun, self.count_marc_dirk())
            case "most_papers_published_by_one_author":
                return(fun, self.count_marc_dirk())
            case "median_amt_authors":
                return(fun, self.median_amt_authors())
            case _:
                print(f"Unknown data exploration method: {fun}")
                return None


    def perform(self, functions: list[str]) -> list[ExplorerResult]:

        if "all" in functions:
            return self.perform_all()
        if "default" in functions:
            return self.perform_default()
                # Use read_csv to read the file
        return [result for fun in functions if (result := self.hanlde_method(fun)) is not None ]
