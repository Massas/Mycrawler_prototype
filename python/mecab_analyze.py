import csv
import MeCab
import sys
 
# 引数で指定されたファイル名を取得
from sys import argv
input_file_name= sys.argv[1]

# ファイル名を出力
#print(input_file_name)
 
# 指定されたファイルを読み込む
with open(input_file_name, encoding="UTF-8") as f:
    data = f.read()

accumulate_file_name = "python/accumulate.csv"
with open(accumulate_file_name, encoding="UTF-8") as f_a:
    # 単語情報集積ファイルを読み込む
    accum_lines = f_a.readlines()
    for csvobj in csv.reader(accum_lines):
        print(csvobj)

# debug
#print('[ACCUM_DEBUG]')
#for accum_dbg in accum_lines:
#    print(accum_dbg)

# 形態素解析結果を取得する
text = MeCab.Tagger().parse(data)
 
# 形態素解析結果を改行で分割
lines = text.split("\n")

cnt_word = 0 # 名詞の数
words = [] # 抽出した単語のリスト
result_format = [['','',0]]
candidates = [] # 単語と品詞と抽出した回数の記録を2次元配列で実現

# 各行ごとに処理を行う
for line in lines:
    #形態素解析結果を分割
    blocks = line.split("\t")
    print('[DEBUG]' + 'blocks: ')
    for dbg in blocks:
        print(dbg)
     
    if len(blocks) > 1:
        word = blocks[0] #対象文字列（例：すもも）
        info  = blocks[1] #品詞情報（例：名詞,一般,*,*,*,*,すもも,スモモ,スモモ）
        items = info.split(",") #品詞情報を分割

        if words.count(word) == 0:
            print("品詞解析")
            for item in items:                 
                # 対象文字の品詞が名詞、形容詞、動詞、副詞、いずれかの場合、カウンタをインクリメント
                if item == "名詞" or item == "形容詞" or item == "動詞" or item == "副詞":
                    print('item == "名詞" or item == "形容詞" or item == "動詞" or item == "副詞"')
                    cnt_word += 1
                    words.append(word)
                    is_new_word = False

                    num = 0
                    for accum_line in accum_lines:
                        accum_blocks = accum_line.split(",")
                        accum_word = accum_blocks[0].replace("'", "")
                        accum_partspeech = accum_blocks[1]
                        accum_count = int(accum_blocks[2])
                        print('[DEBUG]' + 'word: '+ word + 'candidate: ' + accum_word)
                        if accum_word == word:
                            print("accum_word == word")
                            accum_count+=1
                            accum_blocks[2] = str(accum_count)
                            is_new_word = True
                            print("accum_word:" + accum_word + " accum_count: " + str(accum_count))
                            accum_lines[num] = "'" + accum_blocks[0]+ "'" + "," + "'" + accum_blocks[1] + "'" + ","  + str(accum_blocks[2])
                            num+=1
                            break
                    
                    if is_new_word == False:
                        print("is_new_word == False")
                        # candidates.extend(result_format)
                        new_word = [word,info,0]
                        accum_lines.append(new_word)

# 結果を出力する
print('Total : ' + str(cnt_word))
print('Words : ' + ', '.join(words))
print('candidates: ')
for accum_line in accum_lines:
    print(accum_line)
#    f_a.write(accum_line)
f_a.close
