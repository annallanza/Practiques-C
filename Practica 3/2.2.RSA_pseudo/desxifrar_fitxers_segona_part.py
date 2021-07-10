from math import sqrt
from sympy import isprime
from sympy.core.numbers import mod_inverse
from Crypto.PublicKey import RSA
import gmpy2

def DecimalABase(decimal, m):
	list_base = []
	while decimal != 0: 
		res = decimal % pow(2,m)
		list_base.append(res)
		decimal = int(decimal // pow(2,m))

	result_list = []
	for i in range(0,len(list_base)):
		element = list_base[len(list_base) - i - 1]
		result_list.append(element)

	return result_list

def BaseADecimal(list_base, m):
	decimal = 0
	base = pow(2,m)
	for i in range(0, len(list_base)):
		decimal = decimal + pow(base, len(list_base) - i - 1) * list_base[i]

	return decimal

if __name__ == '__main__':
	#El meu modul
	#Per transformar fitxer .pem a modul: openssl rsa -pubin -in anna.llanza_pubkeyRSA_pseudo.txt -text -modulus -out public_key.txt
	a = 'CEC23F23BEF508254AC389F962CB2FE6A39EECB154C67402490A458AEEA5A1955381CAC30351BEFD0A6DFE4C6F08D4637D0B4770029807E057E0B2BAD59C3E7D5A9B8A505E528C5ED631443635069B3117281649D67BEF74AFB92EFACAB1DBD4D50E346C587224B551D0A88B5E93851F4293F30669EAC82D819096F69AE8554A93FEC698513864C505FBE82650ED1617C08E8336C403CE361EE9771E08BF371D6103B607F42E3794AB5E85A176711AC4D9C1266BC0744770DA117E03A7303635B85923F7543968FD8F550164A2020EBD48ED39A343190287E1421DCA07B637201820867F9B2863227D1C2BDC3539C1A440A040C0B0B6FE0F3F90770CD7E011D5'
	a = int(a,16)

	a_binari = '{0:08b}'.format(a)
	len_a_binari = len(a_binari) #2048 bits

	m = int(len_a_binari / 4) #512 bits 

	list_base = DecimalABase(a, m)

	d = 2 #Pot ser 0, 1 o 2

	r_base = list_base[0] - d
	s_base = list_base[3]

	r_s_base = [r_base, s_base]
	r_s_decimal = BaseADecimal(r_s_base, m) # r * s

	#PART CENTRAL
	part_central_base = [d, list_base[1], list_base[2]]
	part_central = BaseADecimal(part_central_base, m)

	r2_mes_s2 = part_central - (pow(2, m) * s_base + r_base) # r ^ 2 + s ^ 2
	
	aux = (r2_mes_s2 + 2 * r_s_decimal)

	n=gmpy2.mpz(aux)
	gmpy2.get_context().precision=2048
	r_mes_s=int(gmpy2.sqrt(n))

	#Cal comprovar que sigui un numero enter
	#print(r_mes_s)

	#Calculem r i s resolent la equacio: x^2 - (r + s)x + rs = 0
	r = int((r_mes_s + int(gmpy2.sqrt(gmpy2.mpz(r_mes_s * r_mes_s - 4 * r_s_decimal)))) // 2)
	s = int((r_mes_s - int(gmpy2.sqrt(gmpy2.mpz(r_mes_s * r_mes_s - 4 * r_s_decimal)))) // 2)

	#print("r: " + str(r))
	#print("s: " + str(s))

	#Calculem num_primerP i num_primerQ:
	num_primerP = pow(2,m) * r + s
	num_primerQ = pow(2,m) * s + r

	#Comprovar que els numeros siguin primers:
	#es_num_primer = isprime(num_primerP)
	#print('NUMPRIMERP es primer: ' + str(es_num_primer))
	#print(num_primerP)

	#es_num_primer = isprime(num_primerQ)
	#print('NUMPRIMERQ es primer: ' + str(es_num_primer))
	#print(num_primerQ)

	#---------------------------------------------------------------------------------------------------------------------------------------
	#Calcul de la clau privada
	publicExponent = 2**16+1
	modulus = a
	primeP = num_primerP
	primeQ = num_primerQ
	inversePModulusQ = mod_inverse(primeP,primeQ)

	fi_n = (primeP - 1) * (primeQ - 1) #φ(n) = (p − 1)(q − 1)
	privateExponent = mod_inverse(publicExponent, fi_n) #d = e ^ −1 mod φ(n)
	while(privateExponent < 0):
		privateExponent = mod_inverse(privateExponent, fi_n) #d = e ^ −1 mod φ(n)

	#Genereacio del fitxer .pem de la clau privada
	tupla_key = (modulus,publicExponent,privateExponent,primeP,primeQ,inversePModulusQ)

	key = RSA.construct(tupla_key,consistency_check=True)
	f = open('clau_privada.pem','wb')
	f.write(key.exportKey('PEM'))
	f.close()
	
	#PER DESENCRIPTAR FITXER nom.cognom_RSA_pseudo.enc:
	#openssl rsautl -decrypt -in anna.llanza_RSA_pseudo.enc -out clau_privada_decrypted.txt -inkey clau_privada.pem

	#PER DESENCRIPTAR FITXER nom.cognom_AES_pseudo.enc:
	#openssl enc -d -aes-128-cbc -pbkdf2 -kfile clau_privada_decrypted.txt -in anna.llanza_AES_pseudo.enc -out fitxer_decrypted.jpeg

