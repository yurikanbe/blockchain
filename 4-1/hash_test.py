import hashlib

indata = "こんにちは"
hash = hashlib.sha256(indata.encode('utf-8')).hexdigest()
print(hash)
indata = "こんにちは。"
hash = hashlib.sha256(indata.encode('utf-8')).hexdigest()
print(hash)