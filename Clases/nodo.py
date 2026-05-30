
class Nodo:
    def __init__(self, simbolo=None, frecuencia=None):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.hijoIzq = None
        self.hijoDer = None
    
    def __lt__(self, other):
        return self.frecuencia < other.frecuencia