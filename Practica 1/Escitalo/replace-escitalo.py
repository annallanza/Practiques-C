def partir_text(s):
	f = open("source-escitalo.txt", "r")
	text = f.read()
	f.close()

	f = open("Resultats-Escitalo/sortida-escitalo" + str(s) + ".txt", "w")

	k = s #numero maxim de caracters per linea
	i = 0 #contador caracters visitats
	for c in text:
		f.write(c)
		i = i + 1
		if i == k:
			i = 0
			f.write("\n")

	f.close()


def transposar_text(nom_fitxer):
	f = open(nom_fitxer, "r")
	linies_text = f.readlines()
	f.close()

	f = open("Resultats-Escitalo/sortida-transposada-escitalo185.txt", "w")

	nfiles = len(linies_text)
	ncolumnes = len(linies_text[0])

	for j in range(ncolumnes - 1):
		for i in range(nfiles - 1):
			f.write(linies_text[i][j])

	f.close()


def main():
	for s in range(185, 186):
		partir_text(s)

	transposar_text("Resultats-Escitalo/sortida-escitalo185.txt")

if __name__ == '__main__':
	main()
