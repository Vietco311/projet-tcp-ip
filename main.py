import pickle

class HuffmanCode:
    def __init__(self):
        self.file_content = ""
        self.huffman_tree = []
        self.huffman_code = {}

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.file_content = file.read()
        except FileNotFoundError:
            print("Le fichier spécifié est introuvable.")

    def generate_huffman_list(self):

        for char in self.file_content:
            found = False
            for element in self.huffman_tree:
                if isinstance(element, Feuille) and element.character == char:
                    element.occurrence += 1
                    found = True
                    break
            if not found:
                new_leaf = Feuille(1, char)
                self.huffman_tree.append(new_leaf)

            self.huffman_tree.sort(key=lambda x: x.occurrence, reverse=True)

    def build_huffman_tree(self):
        while len(self.huffman_tree) > 1:
            left_element = self.huffman_tree.pop()
            right_element = self.huffman_tree.pop()
            new_node = Noeud(left_element.occurrence + right_element.occurrence, left_element, right_element)
            self.huffman_tree.append(new_node)
            self.huffman_tree.sort(key=lambda x: x.occurrence, reverse=True)
            
    def generate_leaves(self):
        char_count = {}
        for char in self.file_content:
            char_count[char] = char_count.get(char, 0) + 1
                   
        self.huffman_tree = [Feuille(count, char) for char, count in char_count.items()]
        self.huffman_tree.sort(key=lambda x: x.occurrence, reverse=True)

    def create_code(self):
        if not self.huffman_tree:
            return
        root = self.huffman_tree[0]
        self._traverse_tree(root, '')

    def _traverse_tree(self, node, code):
        if isinstance(node, Feuille):
            self.huffman_code[node.character] = code
        elif isinstance(node, Noeud):
            self._traverse_tree(node.left_child, code + "0")
            self._traverse_tree(node.right_child, code + "1")


    def _coder(self, node, code):
        if isinstance(node, Noeud):
            self._coder(node.left_child, code + "1")
            self._coder(node.right_child, code + "0")
        elif isinstance(node, Feuille):
            self.huffman_code[node.character] = code

    def display_huffman_code(self):
        print("Code de Huffman :")
        for char, code in self.huffman_code.items():
            print(f"{char}: {code}")

    def encode_text(self):
        encoded_text = ""
        for char in self.file_content:
            encoded_text += self.huffman_code[char]
        return encoded_text

    def save_huffman_code_to_file(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.huffman_code, file)

    def load_huffman_code_from_file(self, file_path):
        with open(file_path, 'rb') as file:
            self.huffman_code = pickle.load(file)

    def __str__(self):
        return f"HuffmanCode - Fichier: {self.file_content}, Arbre: {self.huffman_tree}, Code: {self.huffman_code}"


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

    def __str__(self):
        return f"Occurrence: {self.occurrence}"


class Feuille(Element):
    def __init__(self, occurrence, character):
        super().__init__(occurrence)
        self.character = character

    def __eq__(self, other):
        if isinstance(other, Feuille):
            return self.character == other.character
        return False

    def __str__(self):
        return f"Feuille - Caractère: {self.character}, {super().__str__()}"


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

    def __str__(self):
        return f"Noeud - {super().__str__()}"


if __name__ == "__main__":
    huffman = HuffmanCode()
    huffman.read_file('./test.txt')
    huffman.generate_huffman_list()
    huffman.build_huffman_tree()
    huffman.create_code()
    print("Arbre de Huffman :")
    print(huffman)
    print()
    print("Affichage du code de Huffman :")
    huffman.display_huffman_code()
    print()
    encoded_text = huffman.encode_text()
    print("Texte encodé :")
    print(encoded_text)

    # Sauvegarde du code de Huffman dans un fichier binaire
    huffman.save_huffman_code_to_file("huffman_code.bin")

    # Chargement du code de Huffman depuis le fichier binaire
    huffman.load_huffman_code_from_file("huffman_code.bin")

    # Exemple de décodage du texte encodé
    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        for char, code in huffman.huffman_code.items():
            if code == current_code:
                decoded_text += char
                current_code = ""
                break

    print("Texte décodé :")
    print(decoded_text)
