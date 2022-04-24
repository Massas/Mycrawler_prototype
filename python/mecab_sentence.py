from time import sleep
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
f_a = open(outfile_name, "w+", encoding="UTF-8")

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

# 各行ごとにワード抽出処理を行う
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

f_a.close
f_a = open(outfile_name, encoding="UTF-8")

# 文章の抽出を行う
# 抽出ファイルの先頭から抽出したワードでデータ全体を走査する
wordstr = f_a.read()
#print(wordstr)
#sleep(3)
wordlist = wordstr.split('\n')
strcnt = len(wordstr)
re_endsentence = re.compile('[。！？!?]+')
sentence = ""
sentences = []
word_found = 0
readpoint = 0
endsentence_tmp = 0

data_tmp = data

for word in wordlist:
    print("word: " + word)
    if len(word) == 0:
        continue

    #形態素解析結果を分割
    blocks = word.split("\t")
    if blocks[0] != "" or len(blocks[0] >= 1):
        word_found = data_tmp.find(blocks[0])
        print("word_found: " + str(word_found))
        if word_found == -1:
            continue

    # データ塊の中から抽出ワードを走査する
    if data_tmp.find(blocks[0]) != 0 or data_tmp.find(blocks[0]) != -1:
        datalen = len(data_tmp)
        print("data length : " + str(datalen))
        startsentence = data_tmp.find(blocks[0])
        print("startsentence : " + str(startsentence))
        # 文末を探す
        endsentence = data_tmp.find("。")
        if endsentence == endsentence_tmp:
            print("no endsentence")
        else:
            endsentence_tmp = endsentence

        print("endsentence: " + str(endsentence))
        sentence = data_tmp[startsentence:endsentence+1]
        print("sentence: " + sentence + " length: " + str(len(data_tmp[startsentence:endsentence+1])))
        readpoint = endsentence + 1
        tmp = data_tmp[readpoint:datalen - readpoint]
        data_tmp = tmp
        sentences.append(sentence)
        sleep(1)

# 抽出した文章を確認する
print("extract result")
extractfile = "python/extract_sentences.txt"
f_extract = open(extractfile, "w+", encoding="UTF-8")
for sentence_result in sentences:
    print(sentence_result)
    f_extract.write(sentence_result)
