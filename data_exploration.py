from typing import Any, Callable, Self
import polars as pl
import os

type ExplorerResult = tuple[str, Any]

class DataExplorer():
    '''
    Can perform different types of data explorations on a given dataset
    '''
    # when adding a function
    # add that name to this list:
    choices = [
                "all", 
               "amt_publications", "average_amt_authors", "unique_authors", "papers_per_author", "average_paper_per_author", 
               "count_marc_dirk", "most_papers_published_by_one_author", "median_amt_authors"
    ]

    df: pl.DataFrame
    def __init__(self, dataset_path: str) -> None:
        self.dataset_path = dataset_path
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
        self.dataset_path = dataset_path
        self.df = self.__create_dataframe(dataset_path)


    def perform_all(self) -> list[ExplorerResult]:
        """
        Performs All the data explorations and returns their results
        """
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
        return result

    
    def most_papers_published_by_one_author(self) -> int:
        return self.papers_per_author().max()


    def average_paper_per_author(self) -> float:
        unique_authors = self.unique_authors()
        return self.df.height / unique_authors if unique_authors > 0 else 0


    def hanlde_method(self, fun: str) -> ExplorerResult | None:
        """
        Handles a exploration method based on the name given and returns it's result
        if there is one.
        """
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
        """
        Entry point of the Data exploration class.
        It Handles all the methods given and returns their results in a list
        """
        if "all" in functions:
            return self.perform_all()
        if "default" in functions:
            return self.perform_default()
                # Use read_csv to read the file
        return [result for fun in functions if (result := self.hanlde_method(fun)) is not None ]

    def create_markdown_table(self, results: list[ExplorerResult], output_ppa: bool = False):
        markdown = "| Technique | Value |\n"
        markdown +="|-----------|-------|\n"
        for (technique, value) in results:
            if technique == "papers_per_author" and output_ppa:
                file_name = self.dataset_path.split(os.sep)[-1].split('.')[0] + "_papers_per_author.csv"
                value.write_csv(file_name, include_header=False, separator=",")
                continue
            markdown += f"| {technique} | {value} |\n"
        return markdown











