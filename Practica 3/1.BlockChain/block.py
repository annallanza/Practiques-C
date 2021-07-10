from transaction import transaction
from rsa_key import rsa_key
from hashlib import sha256
from random import randint

class block:
	def __init__(self):
		'''
		crea un bloc (no necesariamnet valid)
		''' 
		self.d = 16
		self.previous_block_hash = 0
		self.transaction = transaction(randint(1, 1000), rsa_key())

		self.seed = randint(0, pow(2, 256))
		entrada = str(self.previous_block_hash) 
		entrada = entrada + str(self.transaction.public_key.publicExponent) 
		entrada = entrada + str(self.transaction.public_key.modulus) 
		entrada = entrada + str(self.transaction.message) 
		entrada = entrada + str(self.transaction.signature) 
		entrada = entrada + str(self.seed)

		self.block_hash =int(sha256(entrada.encode()).hexdigest(),16) #Pot ser no es un bloc valid


	def genesis(self,transaction):
		'''
		genera el primer bloc d’una cadena amb la transaccio "transaction" que es caracteritza per: 
		- previous_block_hash=0
		- ser valid
		'''
		self.d = 16
		self.previous_block_hash = 0
		self.transaction = transaction
		self.block_hash = self.generar_block_hash_valid()

		return self

	def next_block(self, transaction):
		'''
		genera el seguent block valid amb la transaccio "transaction"
		'''
		new_block = block()
		new_block.genesis(transaction)
		new_block.previous_block_hash = self.block_hash
		new_block.transaction = transaction

		return new_block


	def verify_block(self):
		'''
		Verifica si un bloc es valid:
		-Comprova que el hash del bloc anterior cumpleix las condicions exigides 
		-Comprova la transaccio del bloc es valida
		-Comprova que el hash del bloc cumpleix las condicions exigides
		Si totes les comprovacions son correctes retorna el boolea True. En qualsevol altre cas retorna el boolea False
		'''
		if self.previous_block_hash >= pow(2, 256 - self.d):
			return False
		if not self.transaction.verify():
			return False
		if self.block_hash >= pow(2, 256 - self.d):
			return False

		return True

	def next_block_invalid(self, transaction):
		'''
		genera el seguent block valid amb la transaccio "transaction"
		'''
		new_block = block()
		new_block.d = 16
		new_block.block_hash = new_block.generar_block_hash_invalid()
		new_block.previous_block_hash = self.block_hash
		new_block.transaction = transaction

		return new_block

	def generar_block_hash_valid(self):
		trobat = False
		while(not trobat):
			self.seed = randint(0, pow(2, 256))
			entrada = str(self.previous_block_hash) 
			entrada = entrada + str(self.transaction.public_key.publicExponent) 
			entrada = entrada + str(self.transaction.public_key.modulus) 
			entrada = entrada + str(self.transaction.message) 
			entrada = entrada + str(self.transaction.signature) 
			entrada = entrada + str(self.seed)
			entrada = int(sha256(entrada.encode()).hexdigest(),16)

			if entrada < pow(2, 256 - self.d):
				trobat = True

		return entrada

	def generar_block_hash_invalid(self):
		trobat = False
		while(not trobat):
			self.seed = randint(0, pow(2, 256))
			entrada = str(self.previous_block_hash) 
			entrada = entrada + str(self.transaction.public_key.publicExponent) 
			entrada = entrada + str(self.transaction.public_key.modulus) 
			entrada = entrada + str(self.transaction.message) 
			entrada = entrada + str(self.transaction.signature) 
			entrada = entrada + str(self.seed)
			entrada = int(sha256(entrada.encode()).hexdigest(),16)

			if entrada >= pow(2, 256 - self.d):
				trobat = True

		return entrada

