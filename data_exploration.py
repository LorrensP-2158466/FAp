import polars as pl


class DataExplorer():
    '''
    Can perform different types of data explorations on a given dataset
    '''
    # when adding a function 
    # add that name to this list:
    choices = ["all", "amount_publications", "average_amount_authors"]

    dataset_path: str
    def __init__(self, dataset_path: str) -> None:
        self.dataset_path = dataset_path

    def all(self) -> dict[str, int]:
        pass


    def amount_publications(self) -> int:
        pdf = pl.read_csv(self.dataset_path, has_header=False, separator=',', n_threads=8)
        return pdf.height
    

    def average_amount_authors() -> int:
        pass
    
    # TODO: implement different types of explorations
    '''
    Amount of publications: Lorrens
    Unique authors: Lorrens
    average amount of authors: ?
    median amount of authors: ?
    number of papers per author: Lorrens/Ivan


    '''
