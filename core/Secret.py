import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad



key = 'SU2FsdGVkX18ZUVv'



def encrypt(raw: str, iv: str) -> bytes:
    civ = iv.encode('utf-8')
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, civ)
    return base64.b64encode(cipher.encrypt(raw))


def decrypt(enc: str, iv: str) -> str:
    civ = iv.encode('utf-8')
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, civ)
    decrypted = unpad(cipher.decrypt(enc), 16)
    return str(decrypted, 'utf-8')
