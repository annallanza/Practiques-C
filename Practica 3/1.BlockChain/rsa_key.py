from sympy.core.numbers import mod_inverse
from sympy import randprime
from hashlib import sha256
from time import time
from Crypto import Random
from Crypto.Util import number

class rsa_key:

	def __init__(self,bits_modulo=2048,e=2**16+1):
		'''
		genera una clau RSA (de 2048 bits i amb exponent public 2**16+1 per defecte) 
		'''
		self.publicExponent = e
		self.primeP = randprime(pow(2,int(bits_modulo/2) - 1), pow(2,int(bits_modulo/2)) - 1) #generem un nombre primer aleatori amb total_bits = bits_modulo/2
		self.primeQ = randprime(pow(2,int(bits_modulo/2) - 1), pow(2,int(bits_modulo/2)) - 1) #generem un nombre primer aleatori amb total_bits = bits_modulo/2
		self.modulus = self.primeP * self.primeQ #calculem n = p * q

		fi_n = (self.primeP - 1) * (self.primeQ - 1) #φ(n) = (p − 1)(q − 1)
		self.privateExponent = mod_inverse(self.publicExponent, fi_n) #d = e ^ −1 mod φ(n)
		while(self.privateExponent < 0):
			self.privateExponent = mod_inverse(self.privateExponent, fi_n) #d = e ^ −1 mod φ(n)

		self.privateExponentModulusPhiP = mod_inverse(self.privateExponent,self.primeP - 1)
		self.privateExponentModulusPhiQ = mod_inverse(self.privateExponent,self.primeQ - 1)
		self.inverseQModulusP = mod_inverse(self.primeQ,self.primeP) #es l’invers de primeQ modul primeP representat per un enter,

	def sign(self,message):
		'''
    	c = message = hash(missatge)
    	retorna un enter que es la signatura de "message" feta amb la clau RSA fent servir el TXR (TEOREMA XINES DE RESIDU)
    	'''
		d_1 = self.privateExponent % (self.primeP - 1) #d_1 = d mod (p - 1)
		d_2 = self.privateExponent % (self.primeQ - 1) #d_2 = d mod (q - 1)

		p_1 = mod_inverse(self.primeP, self.primeQ) #p_1 =p ^ −1 mod q
		q_1 = mod_inverse(self.primeQ, self.primeP) #q_1 =q ^ −1 mod p

		c_1 = pow(message, d_1, self.primeP) #c_1 = c ^ d_1 mod p
		c_2 = pow(message, d_2, self.primeQ) #c_2 = c ^ d_2 mod q

		signatura = (c_1 * q_1 * self.primeQ + c_2 * p_1 * self.primeP) % self.modulus #signatura m = c_1 * q_1 * q + c_2 * p_1 * p mod n

		return signatura

	def sign_slow(self,message): 
		'''
		c = message = hash(missatge)
		retorna un enter que es la signatura de "message" feta amb la clau RSA sense fer servir el TXR (TEOREMA XINES DE RESIDU)
		'''
		signatura = pow(message, self.privateExponent, self.modulus) #signatura m = c ^ d mod n

		return signatura

if __name__ == "__main__":

	#Una taula comparativa amb el temps necessari per signar, fent servir el TXR i sense fer-ho servir, 
	#100 missatges diferents amb claus de 512, 1024, 2048 i 4096 bits.

	bits_claus = [512, 1024, 2048, 4096]
	missatges = [int(sha256(f"missatge {i}".encode()).hexdigest(), 16) for i in range(100)]


	for clau in bits_claus:
		clau_privada = rsa_key(clau, 2**16+1)
		print('Utilitzant una clau de ' + str(clau) + ' bits: ')

		t1 = time()
		for missatge in missatges:
			clau_privada.sign(missatge)
		t2 = time()
		print('Temps signatura de 100 missatges amb TXR: ' + str(t2 - t1) + ' s')

		t1 = time()
		for missatge in missatges:
			clau_privada.sign_slow(missatge)
		t2 = time()
		print('Temps signatura de 100 missatges sense TXR: ' + str(t2 - t1) + ' s')

		print('-' * 50)
	






