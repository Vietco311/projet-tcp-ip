import pickle
from flask import Flask, request, jsonify
from docx import Document
import os

app = Flask(__name__)

class HuffmanCode:
    def __init__(self):
        self.file_content = ""
        self.file_name = ""
        self.huffman_tree = []
        self.huffman_code = {}
        self.encoded_text = ""

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

    def create_code(self):
        if not self.huffman_tree:
            return
        root = self.huffman_tree[0]
        self.traverse_tree(root, '')

    def traverse_tree(self, node, code):
        if isinstance(node, Feuille):
            self.huffman_code[node.character] = code
        elif isinstance(node, Noeud):
            self.traverse_tree(node.left_child, code + "0")
            self.traverse_tree(node.right_child, code + "1")


    def display_huffman_code(self):
        print("Code de Huffman :")
        for char, code in self.huffman_code.items():
            print(f"{char}: {code}")

    def encode_text(self):
        for char in self.file_content:
            self.encoded_text += self.huffman_code[char]

    def taux_compression(self, fichier_original, fichier_compressé, code_huffman):
        taille_original = os.path.getsize(fichier_original)
        taille_compressé = os.path.getsize(fichier_compressé)
        taille_code = os.path.getsize(code_huffman)
        taux = ((taille_original - (taille_compressé + taille_code)) / taille_original) * 100
        print(f"Le taux de compression est de {taux:.2f}%")    


    def save_huffman_code_to_file(self, file_path):
        with open(f"upload_folder/{file_path}.bin", 'wb') as file:
            compressed_bits = ''.join(self.encoded_text)
            current_byte = 0
            bit_count = 0
            
            for bit in compressed_bits:
                current_byte = (current_byte << 1) | int(bit)
                bit_count += 1
                
                if bit_count == 8:
                    file.write(bytes([current_byte]))
                    current_byte = 0
                    bit_count = 0
                    
            if bit_count > 0:
                current_byte <<= (8 - bit_count)
                file.write(bytes([current_byte]))
        with open(f"huffman_code/{file_path}.bin", 'wb') as file:
            pickle.dump(self.huffman_code, file)
        self.taux_compression(f"{file_path}", f"upload_folder/{file_path}.bin", f"huffman_code/{file_path}.bin")

    def load_huffman_code_from_file(self, file_path):
        with open(f"huffman_code/{file_path}.bin", 'rb') as file:
            self.huffman_code = pickle.load(file)
        encoded_bits = []
        with open(f"upload_folder/{file_path}.bin", 'rb') as file:
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                for i in range(7, -1, -1):
                    bit = (byte >> i) & 1
                    encoded_bits.append(str(bit))
                byte = file.read(1)
        self.encoded_text = encoded_bits


    def compress(self, file):
        if file.filename.endswith(".doc") or file.filename.endswith(".docx"):
            doc = Document(file.filename)
            self.file_content = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        else:
             self.file_content = file.read().decode('utf-8')       
        self.file_name = file.filename
        self.generate_huffman_list()
        self.build_huffman_tree()
        self.create_code()
        print("Arbre de Huffman :")
        print(self)
        print()
        print("Affichage du code de Huffman :")
        self.display_huffman_code()
        print()
        self.encode_text()
        print("Texte encodé :")
        print(self.encoded_text)

        # Sauvegarde du code de Huffman dans un fichier binaire
        self.save_huffman_code_to_file(self.file_name)

    def decompress(self, file_name):
        self.load_huffman_code_from_file(file_name)
        decoded_text = ""
        current_code = ""
        for bit in self.encoded_text:
            current_code += bit
            for char, code in self.huffman_code.items():
                if current_code.startswith(code):
                    if current_code == code:
                        decoded_text += char
                        current_code = ""
                    break
        return decoded_text



    def __str__(self):
        return f"HuffmanCode - Fichier: {self.file_name}, Arbre: {self.huffman_tree}, Code: {self.huffman_code}"


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
        return f"Feuille - Caractère: {self.character}"


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
        return f"Noeud({self.left}, {self.right})"
