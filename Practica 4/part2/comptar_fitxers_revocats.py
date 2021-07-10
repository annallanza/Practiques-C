cont = 0
with open('/Users/annallanza/Documents/Uni/4t/C/Laboratori/Practica 4/part2/CRL.txt') as f:
    for linea in f:
    	linea = linea.strip()
    	linea = linea.split(':')
    	if linea[0] == "Serial Number":
    		cont = cont + 1

print(cont)