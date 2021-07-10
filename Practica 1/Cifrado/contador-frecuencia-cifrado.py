import collections
import pprint

nombre = "entrada.txt"

with open(nombre, 'r') as f:
    conteo = collections.Counter(f.read().upper())
    salida = pprint.pformat(conteo)
    
print(salida)
