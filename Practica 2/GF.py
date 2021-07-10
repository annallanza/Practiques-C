import time

def suma_p(a,b):
	list_suma = []

	for i in range(0,len(a)):
		list_suma.append(a[i] ^ b[i])
	return list_suma

def modul(list_b_binari):
	#list_m_binari = [1, 0, 0, 0, 1, 1, 1, 0, 1] # m = x^8 + x^4 + x^3 + x^2 + 1
	#list_m_binari = [1, 0, 0, 0, 1, 1, 0, 1, 1] # m = x^8 + x^4 + x^3 + x + 1 --> AES  𝑥8+𝑥4+𝑥3+𝑥+1
	#list_m_binari = [1, 1, 0, 0, 1, 1, 1, 1, 1] # m = 𝑥8+𝑥7+𝑥4+𝑥3+𝑥2+𝑥+1 
	list_m_binari = [1, 0, 1, 1, 0, 1, 0, 0, 1] # m = 𝑥8+𝑥7+𝑥4+𝑥3+𝑥2+𝑥+1 
	list_modul = []
	
	for i in range(0,len(list_b_binari)):
		list_modul.append(list_b_binari[i] ^ list_m_binari[i])
		
	return list_modul

def enter_a_binari_list(b):
	b_binari = '{0:08b}'.format(b)
	
	list_b_binari = []
	for char in b_binari:
		list_b_binari.append(int(char))
		
	return list_b_binari
	
def prod_por_x(list_b_binari):
	if list_b_binari[0] == 0:
		list_b_binari.pop(0)
		list_b_binari.append(0)
	else:
		list_b_binari.append(0)
		list_b_binari = modul(list_b_binari)
		list_b_binari.pop(0)
		
	return list_b_binari

def GF_product_p(a,b):
	if a == 1:
		return b
	if b == 1:
		return a
	if a == 0 or b == 0:
		return 0

	list_b_binari = enter_a_binari_list(b)

	list_sum_binari = []
	for i in range(8):
		list_ax_binari = []
		if list_b_binari[8 - 1 - i] == 1:
			list_ax_binari = enter_a_binari_list(a)
			for j in range(i):              
				list_ax_binari = prod_por_x(list_ax_binari)
			
			if len(list_sum_binari) == 0:
				list_sum_binari = list_ax_binari
			else:
				list_sum_binari = suma_p(list_sum_binari, list_ax_binari)

	resultat = ''
	for i in range(len(list_sum_binari)):
		resultat = resultat + str(list_sum_binari[i])

	return int(resultat, 2)

def GF_es_generador(a):
	if a == 0:
		return False
	
	resultat = 1
	for i in range(1,256):
		resultat = GF_product_p(resultat, a)
		if resultat == 1:
			if i == 255:
				return True
			else:
				return False
	return False

def GF_tables():
	g = 2 #Un exemple de generador, podria ser un altre 
	#g = 3 #Un exemple de generador, per a AES
	taula_exponencial = []
	taula_logaritme = []
	
	#Calculem la taula exponencial tal que a la posicio i tingui a = g^i
	resultat = 1
	taula_exponencial.append(resultat)
	for i in range(1,256):
		resultat = GF_product_p(resultat, g)
		taula_exponencial.append(resultat)

	#Calculem la taula logaritme tal que a la posicio a tingui i tal que a = g^i
	for i in range(0,256):
		taula_logaritme.append('#')

	resultat = 1
	for i in range(0,255):
		taula_logaritme[resultat] = i
		resultat = GF_product_p(resultat, g)

	return taula_exponencial, taula_logaritme

def GF_product_t(a,b):
	pos_a = taula_logaritme[a]
	pos_b = taula_logaritme[b]

	pos_ab = pos_a + pos_b

	if pos_ab > 255:
		pos_ab -= 255

	resultat = taula_exponencial[pos_ab]

	return resultat

def GF_invers(a):
	if a == 0:
		return 0

	pos_a = taula_logaritme[a]

	resultat = taula_exponencial[255 - pos_a]

	return resultat
		
if __name__ == '__main__':
	#a, b i c son valors en decimal
	a = 115
	b = 6

	taula_exponencial, taula_logaritme = GF_tables()

	#c = GF_es_generador(2)
	c = GF_product_t(a, b)

	#c = GF_invers(a)

	#c = GF_product_p(a, b)

	print(c)

	#----------------------------------COMPROVACIO FUNCIO PROD_POR_X(B)----------------------------
	'''
	b = 6
	c = prod_por_x(b)

	print('b: ' + str(enter_a_binari_list(b)))
	print('c: ' + str(c))
	'''
	#----------------------------------COMPROVACIO FUNCIO GF_PRODUCT_P(A,B)----------------------------
	'''
	a = 88
	b = 80
	c = GF_product_p(a,b)

	print('UTILITZEM GF_product_p')
	print('a: ' + str(enter_a_binari_list(a)))
	print('b: ' + str(enter_a_binari_list(b)))
	print('c: ' + str(c))
	'''
	#----------------------------------COMPROVACIO FUNCIO GF_ES_GENERADOR(A)----------------------------
	'''
	a = 2
	es_generador = GF_es_generador(a)
	print(es_generador)
	'''
	#----------------------------------COMPROVACIO FUNCIO GF_TABLES()----------------------------
	#taula_exponencial, taula_logaritme = GF_tables()

	'''
	print('TAULA EXPONENCIAL:')
	print(taula_exponencial)
	print('-' * 100)
	print('TAULA LOGARITME:')
	print(taula_logaritme)
	print('-' * 100)
	'''
	#----------------------------------COMPROVACIO FUNCIO GF_PRODUCT_T(A,B)----------------------------
	'''
	a = 88
	b = 80
	c = GF_product_t(a,b)

	print('UTILITZEM GF_product_t')
	print('c: ' + str(c))
	'''
	#----------------------------------COMPROVACIO FUNCIO GF_INVERS(A)----------------------------
	'''
	a = 34
	c = GF_invers(a)

	print('c: ' + str(c))
	'''
	#----------------------------------ALTRES COMPROVACIONS----------------------------
	'''
	a = 56
	c = GF_product_p(a, GF_invers(a)) # c == 1

	print('c: ' + str(c))
	'''
	#----------------------------------TAULES COMPARATIVES----------------------------
	'''
	a = 42
	list_b = [2, 3, 9, 11, 13, 14]

	for i in range(len(list_b)):
		t1_p = time.time()
		c_p = GF_product_p(a,list_b[i])
		t2_p = time.time()

		t1_t = time.time()
		c_t = GF_product_t(a,list_b[i])
		t2_t = time.time()

		print('GF_product_p de a = ' + str(a) + ', b = ' + str(list_b[i]) + ': temps = ' + str(t2_p - t1_p) + ' a * b = ' + str(c_p))
		print('GF_product_t de a = ' + str(a) + ', b = ' + str(list_b[i]) + ': temps = ' + str(t2_t - t1_t) + ' a * b = ' + str(c_t))
		print()
	'''	