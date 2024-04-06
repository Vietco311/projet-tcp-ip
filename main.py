class Element:
    def __init__(self, occurrence):
        self._occurrence = occurrence

    @property
    def occurrence(self):
        return self._occurrence

    @occurrence.setter
    def occurrence(self, value):
        self._occurrence = value

    def __eq__(self, other):
        return self.occurrence == other.occurrence

    def __lt__(self, other):
        return self.occurrence < other.occurrence

    def __repr__(self):
        return f"Occurrence: {self.occurrence}"


class Feuille(Element):
    def __init__(self, occurrence, character):
        super().__init__(occurrence)
        self.character = character

    def __repr__(self):
        return f"Feuille - Caractère: {self.character}, {super().__repr__()}"


class Noeud(Element):
    def __init__(self, occurrence, left=None, right=None):
        super().__init__(occurrence)
        self.left = left
        self.right = right

    @property
    def left_child(self):
        return self.left

    @property
    def right_child(self):
        return self.right

    def __repr__(self):
        return f"Noeud - {super().__repr__()}"
