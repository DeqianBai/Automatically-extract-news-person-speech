import jieba
import re


def cut_sentences(para):
    """
    分句
    :param para:
    :return:
    """
    para = re.sub(r'([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub(r'(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号r
    para = re.sub(r'(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub(r'([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return [s for s in para.split("\n") if len(s) > 0]


def cut(string, stop_words=None):
    """
    分词
    :param stop_words:
    :param string:
    :return:
    """
    if not stop_words:
        stop_words = set()

    def token(txt):
        return ''.join(re.findall(r'[\u4e00-\u9fa5]+', txt))

    return [w for w in jieba.lcut(token(string)) if len(w.strip()) > 0 and w not in stop_words]
