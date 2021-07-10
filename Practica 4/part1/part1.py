import hashlib
from sympy import isprime
import ecpy
from ecpy.curves import Curve,Point

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

if __name__ == "__main__":
    #a) Comproveu que el nombre de punts (ordre) de la corba que es fa servir al certificat es primer.
    n = 115792089210356248762697446949407573529996955224135760342422259061068512044369 #nombre de punts (ordre)

    print("-" * 50)
    print("Ordre: " + str(n))
    print("Ordre es primer: " + str(isprime(n)))

    #b) Comproveu que la clau publica P de www.wikipedia.org es realment un punt de la corba.
    p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
    a = -3
    b = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
    Gx = int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
    Gy = int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)

    clau_publica_x_wikipedia = int("dedb39245f4d61ed2e9b2f892c9d2e7b9d56283c2e4feb71cf410839b825e15a", 16)
    clau_publica_y_wikipedia = int("175d2cb9e5def9e95e17028dd3e6a7a4b42542c4a98e134b4d0a50356e6f67b3", 16)

    E  = Curve.get_curve('secp256r1')

    G = Point(Gx, Gy, E)

    clau_publica_wikipedia = Point(clau_publica_x_wikipedia, clau_publica_y_wikipedia, E)

    print('Generador es de la curva? ', E.is_on_curve(G))
    print('La clave pública es de la curva? ', E.is_on_curve(clau_publica_wikipedia))

    #c) Calculeu l’ordre del punt P
    print('Punto del infinito?', n * G)
    print('Punto del infinito?', n * clau_publica_wikipedia)

    #d) Comproveu que la signatura ECDSA es correcta
    f = open ('mensaje.bin','rb')
    mensaje = f.read()

    mensaje_sha384 = hashlib.sha384(mensaje).hexdigest()

    #TLS 1.3, server CertificateVerify
    preambulo = '20' * 64 + '544c5320312e332c20736572766572204365727469666963617465566572696679' + '00'

    m = preambulo + mensaje_sha384
    mensaje = hashlib.sha256(bytes(bytearray.fromhex(m))).hexdigest()
    mensaje = int(mensaje, 16)

    f1 = int("4304f2366ef7238164f338b8bd544b37773e23ab061d9f2c4f128f5b17ae0bab", 16)
    f2 = int("12c35189719af0f12e2d90c5ddda15243c5462b33e229c126c5255b0b08689de", 16)

    f2_1 = modinv(f2, n)

    w1 = (mensaje * f2_1) % n
    w2 = (f1 * f2_1) % n
    Q = clau_publica_wikipedia
    result = w1 * G + w2 * Q

    print('Firma correcta?', result.x % n == f1)