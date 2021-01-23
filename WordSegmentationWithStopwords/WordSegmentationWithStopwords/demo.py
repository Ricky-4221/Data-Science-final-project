import sys
import jieba
import os

# -*- encoding:utf-8 -*-
# 配置UTF-8的环境
import imp
imp.reload(sys)

# 判断是否为中文字符
def isChinese(word):
    for ch in word:
        if not '\u4e00' <= ch <= '\u9fff':
            return False
    return True

# 写入文件
def savefile(savepath, content):
    fp = open(savepath, "wb")
    fp.write(content)
    fp.close()

# 读取文件
def readfile(path):
    fp = open(path, "rb")
    content = fp.read()
    fp.close()
    return content

# 获取路径名
seg_path = "ResourceSegWithStopwords/202001/"
corpus_path = "ResourceSeg/202001_seg/"

catelist = os.listdir(corpus_path)

# 获取每个目录下的所有文件
for mydir in catelist:
    # 拼接出分类子目录的路径
    class_path = corpus_path + mydir + "/"
    # 拼出分词后的预料分类目录
    seg_dir = seg_path + mydir + "/"
    # 判断目录是否为空
    if not os.path.exists(seg_dir):
        # 创建目录
        os.makedirs(seg_dir)
    # 获取类别目录下的所有目录
    file_list = os.listdir(class_path)
    # 将类别下面的所有目录遍历出来
    for file_path in file_list:
        # 拼出文件名全路径
        fullname = class_path + file_path
        # 读取文件内容
        content = readfile(fullname).strip()
        # 将换行替换掉
        content = content.replace('\r\n'.encode(), ''.encode()).strip()
        # 为文件内容分词
        content_seg = jieba.cut(content)
        # 创建停用词表
        stopwords = [line.strip() for line in open('stopwords_master/final_stopwords.txt', encoding='UTF-8').readlines()]
        # 去停用词
        outstr = ''
        for word in content_seg:
            if word not in stopwords:
                if word != '\t' and word != '　' and isChinese(word):
                    outstr += word
                    outstr += "|"
        # 将处理后的文件保存到分词后的语料目录
        savefile(seg_dir + file_path, outstr.encode())

print('读写完毕')