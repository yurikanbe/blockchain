from ecdsa import SigningKey, SECP256k1
import binascii

# Aさんの秘密鍵
secret_key_str = "6a559a7ba42e9b407787bd24169cb061f90895b6110f4eb81e071b555f5b1641"

secret_key = SigningKey.from_string(binascii.unhexlify(secret_key_str), curve=SECP256k1)
public_key = secret_key.verifying_key
public_key_str = public_key.to_string().hex()

print("=== キー確認 ===")
print(f"Aさんの秘密鍵: {secret_key_str}")
print(f"Aさんの公開鍵: {public_key_str}")
print()

# mining.pyで定義されている公開鍵と比較
mining_keys = {
    "Aさん": "29fb7e4bd445401da7b2ace0affb97d443946304acf2d4c4886f93ebfd120c03a9b145c85d64953fedac37b81fe8f6e19a22cc286f6d3df949df4f7c9b01c68b",
    "Cさん": "2054c535b46f5a8526d3940b19754d76c39a4bee44563ad24ca6848e88245825ecd45aaa05e8080e3cf2ae3811a4efca57e09ab2eb488f1b044210059591cd08", 
    "Dさん": "3dff63e15d388046bd1fae2edc3b82ebc9054243bc214c510f14b2917452e1f07de1ee87bc076bfa0dfea1c88bd1eef6b059c4655f1dd4238f2d42a59abf96fa"
}

print("=== mining.pyで定義されている公開鍵 ===")
for name, key in mining_keys.items():
    print(f"{name}: {key}")
    if key == public_key_str:
        print(f"  ✅ Aさんの秘密鍵から導出された公開鍵と一致！")
    else:
        print(f"  ❌ 一致しません")
print()

print("=== 推奨解決方法 ===")
print("1. mining.pyのminerをAさんの公開鍵に設定する")
print("2. または、post_transaction.pyでAさんがマイニング報酬を受け取ったアカウントから送金する") 