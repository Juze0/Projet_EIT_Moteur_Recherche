import lzma
from time import time
from .file_handler import FileHandler

class FileCompressorDecorator(FileHandler):
    """Implémentaton d'un decorator de FileHandler afin de traiter la compression/décomrpession de fichier gérés par FileHandler.
    C'est un décorateur, car on ajoute ces nouveaux comportements à l'éxecution, exemple: Compressor(JSONFileHandler)"""
    
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.compressed_file_extension = ".xz"


    def save(self, data, file_path):
        """Génère le fichier correspondant puis le compresse"""
        # 1/2 - On délègue l'écriture du fichier à la méthode save de notre service file_handler!
        #self.file_handler.save(data, file_path) => pas nécessaire car on utilise jamais le save de cette facon! La compression est réalisé depuis ask_compressioon 
        original_size = self.path_getsize(file_path)

        # 2/2 - On lance notre algorithme de compression sur le contenu du fichier créer dans l'étape 1, enfin on le supprime !
        start_time = time()
        with open(file_path, 'rb') as f_in, lzma.open(file_path + self.compressed_file_extension, 'wb') as f_out:
            f_out.writelines(f_in)
        compressed_size = self.path_getsize(file_path + '.xz')
        # on supprime le fichier original
        self.remove_path(file_path)
        end_time = time()

        compression_ratio = original_size / compressed_size
        print(f"[COMPRESSOR.save] Le fichier {file_path} a été compressé")
        print(f"[COMPRESSOR.save] Ratio de compression: {compression_ratio:.2f} / Temps de compression: {(end_time - start_time)/60:.2f} min")


    def load(self, file_path):
        """Charge le fichier compressé et le décompresse pour le lire"""
        # 1/3 - On va charger le fichier et on le décompresse
        decompressed_file_path = file_path
        compressed_file_path = file_path + self.compressed_file_extension

        # 2/3 - On lance notre algorithme de décompression sur le contenu du fichier créer dans l'étape 1, enfin on le supprime !
        start_time = time()

        with lzma.open(compressed_file_path, 'rb') as f_in, open(decompressed_file_path, 'wb') as f_out:
            f_out.write(f_in.read())
        # On supprime le fichier compréssé
        self.remove_path(compressed_file_path)
        end_time = time()

        print(f"[COMPRESSOR.load] Le fichier {file_path} a été décompressé")
        print(f"[COMPRESSOR.load] Temps de décompression: {end_time - start_time:.2f} seconds")
        
        # 3/3 - On charge le fichier !
        # Ici, on réalise les opérations de décompression au tout début du chargement du projet, donc pas besoin de renvoyer le résultat
        #return self.file_handler.load(decompressed_file_path)
