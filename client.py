import requests
from docx import Document

# URL de base du serveur Flask
BASE_URL = 'http://localhost:5000'

def get_file_list():
    response = requests.get(f'{BASE_URL}/files')
    if response.status_code == 200:
        file_list = response.json()
        print('List of files on server:')
        for file_name in file_list:
            print(file_name)
    else:
        print('Failed to get file list from server.')

def upload_file(file_name):
    files = {'file': open(file_name, 'rb')}
    response = requests.post(f'{BASE_URL}/upload', files=files)
    if response.status_code == 200:
        print('File uploaded successfully.')
    else:
        print('Failed to upload file to server.')



def download_file(file_name):
    response = requests.get(f'{BASE_URL}/download/{file_name}')
    if response.status_code == 200:
        data = response.json()  # Convertir les données JSON
        if data["file_name"].endswith(".doc") or data["file_name"].endswith(".docx"):
            doc = Document()
            doc.add_paragraph(data["file_data"])
            doc.save(data["file_name"])
        else:
            with open(data["file_name"], 'wb') as f:
                f.write(data["file_data"].encode('utf-8'))  # Convertir la chaîne de caractères en octets
        print('File downloaded successfully.')
    else:
        print('Failed to download file from server.')


if __name__ == '__main__':
    # Test de la fonctionnalité de récupération de la liste des fichiers
    get_file_list()


        # Test de la fonctionnalité de téléchargement de fichier
    file_to_upload = 'revisions_1.txt'  # Remplacez par le chemin absolu du fichier que vous souhaitez télécharger
    upload_file(file_to_upload)

    # Test de la fonctionnalité de téléchargement de fichier
    file_to_download = 'revisions_1.txt'  # Remplacez par le nom du fichier que vous souhaitez télécharger
    download_file(file_to_download)


