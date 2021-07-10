from transaction import transaction
from rsa_key import rsa_key
from block import block
from hashlib import sha256
import pickle

class block_chain:
	def __init__(self,transaction):
		'''
		genera una cadena de blocs que es una llista de blocs,
		el primer bloc es un bloc "genesis" generat amb la transaccio "transaction"
		'''
		self.list_of_blocks = [block().genesis(transaction)]

	def add_block(self,transaction):
		'''
		afegeix a la llista de blocs un nou bloc valid generat amb la transaccio "transaction"
		'''
		previous_block = self.list_of_blocks[-1]

		new_block = previous_block.next_block(transaction)

		self.list_of_blocks.append(new_block)

	def verify(self):
		'''
  		verifica si la cadena de blocs es valida:
		- Comprova que tots el blocs son valids
		- Comprova que el primer bloc es un bloc "genesis"
		- Comprova que per cada bloc de la cadena el seguent es el correcte
		Si totes les comprovacions son correctes retorna el boolea True.
		En qualsevol altre cas retorma el boolea False i fins a quin bloc la cadena es valida
		'''
		i = 0
		previous_block = None
		for block in self.list_of_blocks:
			if not block.verify_block():
				return False

			if i == 0:
				i = i + 1
				if block.previous_block_hash != 0:
					return False
			elif block.previous_block_hash != previous_block.block_hash:
				return False

			previous_block = block

		return True

	def add_block_invalid(self,transaction):
		'''
		afegeix a la llista de blocs un nou bloc valid generat amb la transaccio "transaction"
		'''
		previous_block = self.list_of_blocks[-1]

		new_block = previous_block.next_block_invalid(transaction)

		self.list_of_blocks.append(new_block)

if __name__ == "__main__":
	
	#Un fitxer amb una cadena valida de 100 blocs.
	clau_privada = rsa_key()
	transactions = [transaction(int(sha256(f"missatge {i}".encode()).hexdigest(), 16), clau_privada) for i in range(100)]

	valida = False
	while(not valida):
		cadena_de_blocs = block_chain(transactions[0])
		#print('afegit el block ' + str(0))

		for i in range(1, 100):
			cadena_de_blocs.add_block(transactions[i])
			#print('afegit el block ' + str(i))
		
		valida = cadena_de_blocs.verify()
		#print('es valid: ' + str(valida))

	with open('Fitxers/cadena_100_blocks', 'wb') as file: 
		pickle.dump(cadena_de_blocs, file)

	print("S'ha generat el fitxer cadena_100_blocks amb una cadena valida de 100 blocs")


	#Un fitxer amb una cadena de 100 blocs que nomes sigui valida fins al bloc XX, on XX son les dues ultimes xifres del teu dni XX = 32
	
	clau_privada = rsa_key()
	transactions = [transaction(int(sha256(f"missatge {i}".encode()).hexdigest(), 16), clau_privada) for i in range(100)]

	valida = False
	while(not valida):
		cadena_de_blocs = block_chain(transactions[0])
		#print('afegit el block ' + str(0))

		for i in range(1, 32):
			cadena_de_blocs.add_block(transactions[i])
			#print('afegit el block ' + str(i))

		valida = cadena_de_blocs.verify()
		#print('es valid: ' + str(valida))

	for i in range(32, 100):
		cadena_de_blocs.add_block_invalid(transactions[i])
		#print('afegit el block ' + str(i))

	#valida = cadena_de_blocs.verify()
	#print('es valid: ' + str(valida))

	with open('Fitxers/cadena_100_blocks_DNI', 'wb') as file: 
		pickle.dump(cadena_de_blocs, file)

	print("S'ha generat el fitxer cadena_100_blocks_DNI amb una cadena valida fins al bloc 32")

