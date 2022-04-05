import MeCab
import time
import sys
 
# 引数で指定されたファイル名を取得
from sys import argv
input_file_name= sys.argv[1]
 
# ファイル名を出力
#print(input_file_name)
 
# 指定されたファイルを読み込む
with open(input_file_name, encoding="UTF-8") as f:
    data = f.read()
 
# 形態素解析結果を取得する
text = MeCab.Tagger().parse(data)
 
#print(text)
 
# 形態素解析結果を改行で分割
lines = text.split("\n")
 
 
cnt_word = 0 # 名詞の数
words = [] # 単語リスト
 
# 各行ごとに処理を行う
for line in lines:
    #形態素解析結果を分割
    blocks = line.split("\t")
    #print(blocks[1])
     
    if len(blocks) > 1:
        word = blocks[0] #対象文字列（例：すもも）
        info  = blocks[1] #品詞情報（例：名詞,一般,*,*,*,*,すもも,スモモ,スモモ）
        items = info.split(",") #品詞情報を分割
         
        if words.count(word) == 0:
            for item in items:
                #print(item)
                 
                # 対象文字の品詞が名詞、形容詞、動詞、副詞、いずれかの場合、カウンタをインクリメント
                if item == "名詞" or item == "形容詞" or item == "動詞" or item == "副詞":
                    cnt_word += 1
                    words.append(word)
 
# 結果を出力する
print('Total : ' + str(cnt_word))
print('Words : ' + ', '.join(words))
