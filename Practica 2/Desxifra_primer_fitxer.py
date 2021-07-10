from Crypto.Cipher import AES

clau = open("Fitxers_encriptats/2020_09_25_10_32_21_anna.llanza.key", 'rb').read()
C = open("Fitxers_encriptats/2020_09_25_10_32_21_anna.llanza.enc", 'rb').read()
iv = C[:AES.block_size]
mode = AES.MODE_OFB
aes = AES.new(clau, mode, iv)
M = aes.decrypt(C[AES.block_size:])
open('Fitxers_desencriptats/primer_fitxer_desxifrat.jpeg', 'wb').write(M)