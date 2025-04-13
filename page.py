class Page:
    def __init__(self,page_id: int, page_title: str) -> None:
        self.page_id = page_id
        self.page_title = page_title

    def getData(self):
        print(self.page_id,"has title:",self.page_title)
        
