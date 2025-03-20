from Crypto.PublicKey import RSA

n = 340282366920938460843936948965011886881
e = 65537

key = RSA.construct((n, e))
pem_key = key.publickey().exportKey()

with open('public_key.pem', 'wb') as f:
    f.write(pem_key)
