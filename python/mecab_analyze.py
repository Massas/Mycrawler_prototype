import MeCab
import sys
 
# 引数で指定されたファイル名を取得
from sys import argv
input_file_name= sys.argv[1]
accumulate_file_name = "python/accumulate.txt"

# ファイル名を出力
#print(input_file_name)
 
# 指定されたファイルを読み込む
with open(input_file_name, encoding="UTF-8") as f, open(accumulate_file_name, encoding="UTF-8") as f_a:
    data = f.read()
    # 単語情報集積ファイルを読み込む
    accum_lines = f_a.readlines()

# debug
print('[ACCUM_DEBUG]')
for accum_dbg in accum_lines:
    print(accum_dbg)
    print(type(accum_dbg))

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
            for item in items:                 
                # 対象文字の品詞が名詞、形容詞、動詞、副詞、いずれかの場合、カウンタをインクリメント
                if item == "名詞" or item == "形容詞" or item == "動詞" or item == "副詞":
                    cnt_word += 1
                    words.append(word)
                    is_new_word = False

                    for accum_line in accum_lines:
                        print('[DEBUG]' + 'word: '+ word + 'candidate: ' + accum_line[0])
                        if accum_line[0] == word and accum_line[1] == info:
                            accum_line[2]+=1
                            is_new_word = True
                            break
                    
                    if is_new_word == False:
                        # candidates.extend(result_format)
                        new_word = [word,info,0]
                        accum_lines.append(new_word)

# 結果を出力する
print('Total : ' + str(cnt_word))
print('Words : ' + ', '.join(words))
print('candidates: ')
for accum_line in accum_lines:
    print(accum_line)
