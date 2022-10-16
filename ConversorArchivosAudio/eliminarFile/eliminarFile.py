from os import remove

class EliminarFile:
    def eliminar(self, path):
        remove(path)
        return True    
        