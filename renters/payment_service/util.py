private_key = None

def encrypt(message, public_key_path='public_key.pem'):
    from Crypto.Cipher import PKCS1_OAEP
    from Crypto.PublicKey import RSA

    with open(public_key_path, 'r') as fin:
        pub_key = RSA.importKey(fin.read())
        cipher = PKCS1_OAEP.new(pub_key)
        ciphertext = cipher.encrypt(message)
        return ciphertext

def decrypt(message, private_key_path='private_key.pem'):
    """
    Could decrypt ciphertext encrypted by forge.js
    var pem = "-----BEGIN PUBLIC KEY-----" +
              "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwb7gVFbFCHd3vrPMUlBs" +
              "4WzNDc14Lw73KGjhxWix6K9TDJWtVBVPkyD5aEku1EN+tEKW8OwLMZSW6O5q3XBE" +
              "ycItJEWS2gBJ2GYsvXIWkVMgELz2oUm/obOjoTGbKE/51n9q1xXtNpZ2gCug2JH6" +
              "0lH0KmNToFpjSJ8yzcUuC5XfbMQLryRlE0soeucMMYJ7Yrwq5Up+EXVh24rgs9Ak" +
              "/iNzcFVJtOHLXxXheR4TftPZP6kyz7NowY3YHPBBOiXe0nQKbNhWUXR1vmNNLzvz" +
              "jE3F9Cmv8I+iNTpNbHrqcUbXkx/bDfcIsWqaVVdZBeq2mEP1BrXTsIHQAu6IAhFj" +
              "3wIDAQAB" +
              "-----END PUBLIC KEY-----"
    var publicKey = forge.pki.publicKeyFromPem(pem);
    var encrypted = publicKey.encrypt("hello", 'RSA-OAEP');
    var msg = forge.util.encode64(encrypted)

    References:
    1. Usages: https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.PKCS1_OAEP-module.html
    2. Create Keys: https://www.pidder.de/pidcrypt/?page=demo_rsa-encryption
    """
    global private_key

    from Crypto.Cipher import PKCS1_OAEP
    from Crypto.PublicKey import RSA

    # cached private key to impove performance
    if not private_key:
        with open(private_key_path, 'r') as fin:
            private_key = fin.read()

    pvt_key = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(pvt_key)
    message = cipher.decrypt(message)
    return message

if __name__=='__main__':
    # The encrypt card information is encoded to base64 string by client side, should decode before decrypt
    import base64
    txt = base64.b64decode("sY6knn1pnC107WW4k6rCsUr2h1/tE9Qs+dvPWaoQufanLpTkj2ALyDV1iSjVnId6ZX9LNNXI1YHwBwhkwD8ECA9tHiN9T3XcoILzLFUxkpnoWtpCSJJfvnackyBQtmafi0Ur05+qaHW1cXLAz8JZGU87Rv18zFCBj/5FUeMDn/UkarYZnj08bX5p+I6y6f7jRQOBLHFW9mZEGj2WPptflh252ppTjXK12g6boEV382sdyzPmrxL8wZ7XGhc0N1EiTfwBKn932NymiVpvVqtvqBO9Q09LRCnOepQysaMoWUNUg3eMt+qipUPHdYJSbZcDkqwmCyg7eHoA9ZuKQYVnMQ==")
    print(decrypt(txt))
