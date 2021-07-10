from sympy import isprime
from sympy.core.numbers import mod_inverse
from Crypto.PublicKey import RSA
import sys
sys.setrecursionlimit(10000)

def mcd(a,b): 
    if(b==0): 
        return a 
    else: 
        return mcd(b,a%b)

if __name__ == '__main__':
	#modul alvaro.macias_pubkeyRSA_RW.pem
	b = "B5C52160D5B58DEA946258C5D6391EC0184CFA6C459C3D615A2E2278CFF07C34B6305B32783C41A4B63E581383F18050843C16B8613A4E644D5A19E7149866A9953B14AEF8FB3385BADCCA455706AD81B34BEE6119E2D4FBCB16F5E909F7803123F6945E2B032ECDE11B51387DB7F1A0AF667ABFEAB62170490BBBDBA857A3A01CC7E9C064EA9ABE09A22168EC00F56651A7EDE4FE0AA50718A2393B71287E152A17F6275C0E0F66F634C0394388808AEA8A13223480AB964C8294D375950EDF0EC7FEE6C2E323D42304607AD99AD074D38FF9500DFD4F7CF684EA95FE0367D91D66C5C426F2EB9107FA2F4B17BCCAB8A5C82C81C3D09060EF338D8F038D389D"
	b = int(b, 16)

	#El meu modul
	#Per transformar fitxer .pem a modul: openssl rsa -pubin -in anna.llanza_RSA_RW.txt -text -modulus -out public_key.txt
	a = '8C367F01647DAD6D619E53BBB29D3C531868004EDDCEEE946D5684A791F058C1388CEFCE6252785EE818A17D6B811EAE96BDC8916700A8BF89FA234E469145FA869FA9D6F87F324A63B2FACA214440CA952822F3D66CB65C5F46D17682ECCFFD58BFD2ACA0BED0368D2ADD20081918B8B352F0A440517C4DF5F1FDEC4F0845189D3D162924EA8F31B5028A8650320C4EBCA15192A2F7603827A79FDFA7EBABFA212019CB8F953B395AB860B988676D9C4BBC80860B709F38333E234BB2CBCF54FBB2FA71D1452C7C4910186598FEA1C449BF042ECB6BF0CB7E9164C6B4915C9FDA8AF89B438F33F6CEAD1CC5EB906FD2136B8204D88CF384E5A1C5E0506EC96D'
	a = int(a,16)

	num_primerQ = mcd(a, b)

	#Per comprovar si es un numero primer
	#es_num_primer = isprime(num_primerQ)
	#print('NUMPRIMERQ es primer: ' + str(es_num_primer))

	num_primerP = a // num_primerQ

	#Per comprovar si es un numero primer
	#es_num_primer = isprime(num_primerP)
	#print('NUMPRIMERP es primer: ' + str(es_num_primer))

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

	#PER DESENCRIPTAR FITXER nom.cognom_RSA_RW.enc:
	#openssl rsautl -decrypt -in anna.llanza_RSA_RW.enc -out clau_privada_decrypted.txt -inkey clau_privada.pem

	#PER DESENCRIPTAR FITXER nom.cognom_AES.enc:
	#openssl enc -d -aes-128-cbc -pbkdf2 -kfile clau_privada_decrypted.txt -in anna.llanza_AES_RW.enc -out fitxer_decrypted.png


