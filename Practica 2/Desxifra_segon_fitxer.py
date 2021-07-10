import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


ASCII = ''.join([chr(i) for i in range(256)])
claus = []

def generar_claus():
    for a in ASCII:
        for b in ASCII:
            claus.append(str(a * 8) + str(b * 8))

if __name__ == "__main__":
    
    C = open("Fitxers_encriptats/2020_09_25_10_32_21_anna.llanza.puerta_trasera.enc", 'rb').read()
    generar_claus()

    cont = 0
    for i in range(len(claus)):
        try:
            H = hashlib.sha256(claus[i].encode()).digest()
            aes = AES.new(H[:16], AES.MODE_CBC, H[16:])
            M = unpad(aes.decrypt(C), AES.block_size)

        except ValueError:
            pass
        except StopIteration:
            break

        else:
            if cont == 106:
                open('Fitxers_desencriptats/segon_fitxer_desxifrat.mp4', 'wb').write(M)
                break
            cont += 1


