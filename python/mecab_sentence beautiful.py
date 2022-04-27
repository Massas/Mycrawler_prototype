from time import sleep
import MeCab
import sys
import re
from bs4 import BeautifulSoup


# 引数で指定されたファイル名を取得
from sys import argv
input_file_name= sys.argv[1]

outfile_name = "python/sentences.txt"
f_a = open(outfile_name, "w+", encoding="UTF-8")

# 指定されたファイルを読み込む
# searchkey
with open(input_file_name, encoding="UTF-8") as f:
    data = f.read()

soup = BeautifulSoup(data, 'html.parser')
print(soup.title.text)
