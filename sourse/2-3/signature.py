from ecdsa import SigningKey, BadSignatureError, SECP256k1

secret_key = SigningKey.generate( curve = SECP256k1)
print("秘密鍵：" + secret_key.to_string().hex())
public_key = secret_key.verifying_key
print("公開鍵：" + public_key.to_string().hex())

doc = "これは送信したい文書です。"
signature = secret_key.sign(doc.encode('utf-8'))
print("電子署名：" + signature.hex())

try:
    public_key.verify(signature, doc.encode('utf-8'))
    print("文書は改ざんされていません。")
except BadSignatureError:
    print("文書が改ざんされています。")