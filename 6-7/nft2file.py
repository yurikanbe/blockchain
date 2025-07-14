import base64

NFT = "（ここにnft_dataの中身の文字列をコピー＆ペーストする）"
with open("./sample.jpg", "wb") as f:
    f.write(base64.b64decode(NFT))