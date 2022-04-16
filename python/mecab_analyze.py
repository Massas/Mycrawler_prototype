import csv
import MeCab
import sys
import re

# 除外したいパターン
re_alphabet = re.compile('[a-zA-Z]+')
re_symbol = re.compile(',\.!><=?/')

# 引数で指定されたファイル名を取得
from sys import argv
input_file_name= sys.argv[1]

accumulate_file_name = "python/accumulate.csv"
with open(accumulate_file_name, encoding="UTF-8") as f_a:
    # 単語情報集積ファイルを読み込む
    accum_tmp = f_a.readlines()
    accum_lines = list(dict.fromkeys(accum_tmp))
    for csvobj in csv.reader(accum_lines):
        print(csvobj)

# ファイル名を出力
print(input_file_name)
 
# 指定されたファイルを読み込む
# searchkey
with open(input_file_name, encoding="UTF-8") as f:
    data = f.read()
    print("data:" + data)

# 形態素解析結果を取得する
text = MeCab.Tagger().parse(data)
print("text: " + text)
# 形態素解析結果を改行で分割
tmplines = text.split("\n")

# 重複データを省く
lines = list(dict.fromkeys(tmplines))

print('[LINES_DEBUG]')
for lines_dbg in lines:
    if lines_dbg == "" or lines_dbg == " " or lines_dbg == "EOS" or lines_dbg[0] == ",":
        continue
    else:
        print("[" + lines_dbg + "]")

cnt_word = 0 # 名詞の数
words = [] # 抽出した単語のリスト
result_format = [['','',0]]
candidates = [] # 単語と品詞と抽出した回数の記録を2次元配列で実現
linenum = 0

# 各行ごとに処理を行う
for line in lines:
    if line == "" or line == " " or line == "EOS" or line[0] == ",":
        continue

    #形態素解析結果を分割
    blocks = line.split("\t")

    is_exist_word = False
     
    if len(blocks) > 1:
        word = blocks[0] #対象文字列（例：すもも）
        info  = blocks[1] #品詞情報（例：名詞,一般,*,*,*,*,すもも,スモモ,スモモ）
        items = info.split(",") #品詞情報を分割

        if words.count(word) == 0:
            print("========================================================")
            print("品詞解析")
            for item in items:
                print("word = " + word + ", item = " + item)
                if word == "," or word == " ":
                    break
                if word.isdigit() == True:
                    break
                if word.isalnum() == True:
                    break
                if re_alphabet.match(word) == True or re_symbol.match(word) == True:
                    break

                istarget = False
                # 対象文字の品詞が名詞、形容詞、動詞、副詞、いずれかの場合、カウンタをインクリメント
                if item == "名詞" or item == "固有名詞" or item == "形容詞" or item == "動詞" or item == "副詞":
                    print('item == "名詞" or item == "固有名詞" or item == "形容詞" or item == "動詞" or item == "副詞"')
                    istarget = True
                    cnt_word += 1
                    words.append(word)

                    for accum_line in accum_lines:
                        print("accum_line:" + accum_line)
                        accum_blocks = accum_line.split(",")
                        accum_word = accum_blocks[0].replace("'", "")
                        print("accum_word: " + accum_word + "," + "accum_blocks[0]: " + accum_blocks[0])
                        accum_partspeech = accum_blocks[1]
                        accum_count = int(accum_blocks[2])
                        print('[DEBUG]' + 'word: '+ word + ', accum_word: ' + accum_word)
                        if word == accum_word:
                            print("word == accum_word")
                            accum_count+=1
                            accum_blocks[2] = str(accum_count)
                            is_exist_word = True
                            print("linenum: " + str(linenum) + " accum_word:" + accum_word + " accum_count: " + str(accum_count))
                            accum_lines[linenum] = accum_blocks[0]+ "," + accum_blocks[1] + ","  + str(accum_blocks[2])
                            print("accum_lines[num]: " + accum_lines[linenum])
                            break
            
                if is_exist_word == False and istarget == True:
                    print("is_exist_word == False")
                    # candidates.extend(result_format)
                    new_word = "'" + word + "','" + item + "'" + "," + str(1)
                    print("new_word: "+ new_word)
                    accum_lines.append(new_word)
                    break
                else:
                    break
    linenum+=1

# 結果を出力する
print('*****************************************')
print('Total : ' + str(cnt_word))
print('Words : ' + ', '.join(words))
print('*****************************************')
# 集積ファイルへの書き込み
print('candidates: ')
with open(accumulate_file_name, 'w', encoding="UTF-8") as f_a:
    for accum_line in accum_lines:
        print(accum_line)
        f_a.write(accum_line + '\n')
