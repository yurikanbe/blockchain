import blockchain
import requests

# サーバーから現在のチェーンを取得
response = requests.get("http://127.0.0.1:8000/chain")
chain = response.json()

# 新しいダミーブロックを追加してverify_chainをテスト
blockchain_instance = blockchain.Blockchain()

# デバッグ用のverify_chainメソッドを作成
def debug_verify_chain(self, chain):
    print("=== チェーン検証デバッグ開始 ===")
    all_block_transactions = []
    
    for i in range(len(chain["blocks"])):
        block = chain["blocks"][i]
        print(f"\nブロック {i} を検証中...")
        print(f"  ブロック時間: {block['time']}")
        print(f"  トランザクション数: {len(block['transactions'])}")
        
        if i == 0:
            if block != self.first_block:
                print("  ❌ 初期ブロックが一致しません")
                return False
            else:
                print("  ✅ 初期ブロック OK")
        else:
            previous_block = chain["blocks"][i-1]
            expected_hash = self.hash(previous_block)
            if block["hash"] != expected_hash:
                print(f"  ❌ ハッシュ不一致:")
                print(f"    期待値: {expected_hash}")
                print(f"    実際値: {block['hash']}")
                return False
            else:
                print("  ✅ ハッシュ検証 OK")
                
            # PoW検証
            block_without_time = {
                "transactions": block["transactions"],
                "hash": block["hash"],
                "nonce": block["nonce"],
            }
            block_hash = self.hash(block_without_time)
            binary_hash = format(int(block_hash, 16), '0256b')
            suffix = binary_hash[-blockchain.POW_DIFFICULTY:]
            required_suffix = '0' * blockchain.POW_DIFFICULTY
            
            if suffix != required_suffix:
                print(f"  ❌ PoW検証失敗:")
                print(f"    ハッシュ: {block_hash}")
                print(f"    末尾: {suffix}")
                print(f"    必要: {required_suffix}")
                return False
            else:
                print("  ✅ PoW検証 OK")
                
        # トランザクション検証
        reward_trans_fig = False
        print(f"  トランザクション検証中...")
        for j, transaction in enumerate(block["transactions"]):
            print(f"    トランザクション {j}: {transaction['sender'][:10]}... -> {transaction['receiver'][:10]}... ({transaction['amount']})")
            
            if transaction["sender"] == "Blockchain":
                if not reward_trans_fig:
                    reward_trans_fig = True
                    print("      ✅ マイニング報酬トランザクション")
                else:
                    print("      ❌ 重複するマイニング報酬")
                    return False
                if transaction["amount"] != blockchain.REWARD_AMOUNT:
                    print(f"      ❌ 報酬額が間違っています: {transaction['amount']} != {blockchain.REWARD_AMOUNT}")
                    return False
            else:
                if not self.verify_transaction(transaction):
                    print("      ❌ トランザクション署名検証失敗")
                    return False
                else:
                    print("      ✅ 署名検証 OK")
                    
            if transaction not in all_block_transactions:
                all_block_transactions.append(transaction)
            else:
                print("      ❌ 重複トランザクション")
                return False
                
        # 残高チェック
        if all_block_transactions != []:
            accounts = self.account_calc(all_block_transactions)
            print(f"  現在の残高: {accounts}")
            if min(accounts.values()) < 0:
                print("  ❌ 残高がマイナスになりました")
                return False
            else:
                print("  ✅ 残高チェック OK")
                
    print("\n✅ チェーン検証完了")
    return True

# デバッグメソッドをインスタンスにバインド
blockchain_instance.debug_verify_chain = debug_verify_chain.__get__(blockchain_instance, blockchain.Blockchain)

# テスト実行
result = blockchain_instance.debug_verify_chain(chain)
print(f"\n最終結果: {'成功' if result else '失敗'}") 