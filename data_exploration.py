import polars as pl


class DataExplorer():
    '''
    Can perform different types of data explorations on a given dataset
    '''
    # when adding a function 
    # add that name to this list:
    choices = ["all", "amt_publications", "average_amt_authors"]

    nthreads = 8

    dataset_path: str

    def __init__(self, dataset_path: str) -> None:
        self.dataset_path = dataset_path


    def all(self) -> dict[str, int]:
        pass


    def amount_publications(self) -> int:
        pdf = pl.read_csv(self.dataset_path, has_header=False, separator=',', n_threads=self.nthreads)
        return pdf.height
    

    def average_amt_authors(self) -> int:
        pass


    def median_amt_authors(self) -> int:
        pass


    def papers_per_author(self) -> dict:
        pass

    def perform(self) -> None:
        print("t")

    
    # TODO: implement different types of explorations
    '''
    Amt of publications: Lorrens
    Unique authors: Lorrens
    average amount of authors: Ivan
    median amount of authors: Ivan
    number of papers per author: Lorrens/Ivan
    '''
