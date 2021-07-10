from rsa_public_key import rsa_public_key
from rsa_key import rsa_key

class transaction:
	def __init__(self, message, RSAkey):
		'''
		genera una transaccio signant "message" amb la clau "RSAkey"
		'''
		self.public_key = rsa_public_key(RSAkey)
		self.message = message
		self.signature = RSAkey.sign(message)
	
	def verify(self):
		'''
		retorna el boolea True si "signature" es correspon amb una signatura de "message" feta amb la clau publica "public_key". En qualsevol altre cas retorna el boolea False
		'''
		return self.public_key.verify(self.message, self.signature)