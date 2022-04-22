import csv
import MeCab
import sys
import re

# 除外したいパターン
re_specialchar = re.compile('[\_\.,:\>\<!=^~)(|?"\'+/\]⋅\[*%&$\-}{#@;:]+')
re_alphabet = re.compile('[a-zA-Z]+')
re_slash = re.compile(r'\+')
re_return = re.compile('\n+')

# 引数で指定されたファイル名を取得
from sys import argv
input_file_name= sys.argv[1]

outfile_name = "python/sentences.txt"
f_a = open(outfile_name, "w", encoding="UTF-8")

# 指定されたファイルを読み込む
# searchkey
with open(input_file_name, encoding="UTF-8") as f:
    data = f.read()

# 形態素解析結果を取得する
text = MeCab.Tagger().parse(data)
# 形態素解析結果を改行で分割
tmplines = text.split("\n")

# 重複データを省く
lines = list(dict.fromkeys(tmplines))

cnt_word = 0 # 名詞の数
words = [] # 抽出した単語のリスト
linenum = 0

# 各行ごとに処理を行う
# 各行のデータ構造は以下
# ペルシャ	名詞,固有名詞,地域,一般,*,*,ペルシャ,ペルシャ,ペルシャ
# そびえる	動詞,自立,*,*,一段,基本形,そびえる,ソビエル,ソビエル
# CXIhbQeQ	名詞,一般,*,*,*,*,*
# 963744999999996	名詞,数,*,*,*,*,*
for line in lines:
    if line == "" or line == " " or line == "EOS" or line[0] == ",":
        continue

    #形態素解析結果を分割
    blocks = line.split("\t")

    if len(blocks) > 1:
        word = blocks[0] # 抽出ワード：モザイク,壮大,トプカプ etc
        info  = blocks[1] # 品詞情報

        if word.isdigit() == True or re_specialchar.search(word) != None or re_alphabet.search(word) != None or re_slash.search(word) != None:
            continue

    f_a.write(line + '\n')
