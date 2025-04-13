class Pagelink:
    def __init__(self,pl_from: int, pl_to: int) -> None:
        self.pl_from = pl_from
        self.pl_to = pl_to

    def getData(self):
        print(self.pl_from,"has link to:",self.pl_to)
        
