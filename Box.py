class Box:

    def __init__(self, id_box: int, degree: int):
        self._id_box = None
        self._item = 2
        self._next = None
        self._degree = None # 0 -> first_line AND 1 -> second_line

        self.set_id_box(id_box)
        self.set_degree(degree)

    # Getters and Setters
    def get_id_box(self) -> int:
        return self._id_box
    
    def get_item(self) -> int:
        return self._item
    
    def get_next(self):
        return self._next
    
    def get_degree(self) -> int:
        return self._degree
    
    def set_id_box(self, id_box: int):
        self._id_box = id_box

    def set_item(self, item: int):
        self._item = item

    def set_next(self, next_box):
        self._next = next_box

    def set_degree(self, degree: int):
        self._degree = degree