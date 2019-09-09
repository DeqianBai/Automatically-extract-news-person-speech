from flaskr.utils import *
from pyhanlp import *
from flaskr.SIF_embedding import SIFModel
from flaskr.speck_classifier import BiRNN

##  1.
class WordNode:
    """
    构建依存树节点
    """

    def __init__(self, ID, NAME, LEMMA, DEPREL, POSTAG, CPOSTAG):
        self.ID = ID
        self.NAME = NAME
        self.LEMMA = LEMMA
        self.DEPREL = DEPREL
        self.POSTAG = POSTAG
        self.CPOSTAG = CPOSTAG
        self.parent = None
        self.children = {}


def parse_sentence(sentence):
    """
    句子依存分析，构建依存树
    """
    # 依存分析
    parsed_sentence = HanLP.parseDependency(sentence)
    # 构建依存树
    node_dict = {}
    trie = None
    for word in parsed_sentence.iterator():
        head = word.HEAD
        if word.ID in node_dict:
            node = node_dict[word.ID]
        else:
            node = WordNode(word.ID, word.NAME, word.LEMMA, word.DEPREL, word.POSTAG, word.CPOSTAG)
            node_dict[word.ID] = node
        if head.ID in node_dict:
            parent = node_dict[head.ID]
        else:
            parent = WordNode(head.ID, head.NAME, head.LEMMA, head.DEPREL, head.POSTAG, head.CPOSTAG)
            node_dict[head.ID] = parent
        if head.ID == 0:
            trie = node
        node.parent = parent
        parent.children[node.ID] = node
    return parsed_sentence, trie


def search_trie(trie, predicate):
    unseen = [trie]
    while len(unseen) > 0:
        node = unseen.pop(0)
        if predicate(node):
            return node
        unseen += node.children.values()
    return None


def build_sentence(node, sentence=''):
    """
    还原当前节点的句子
    :param node:
    :param sentence:
    :return:
    """
    children = node.children.values()
    if len(children) == 0:
        return sentence + node.LEMMA
    left = [c for c in children if c.ID < node.ID]
    right = [c for c in children if c.ID > node.ID]
    for c in left:
        sentence = build_sentence(c, sentence)
    sentence += node.LEMMA
    for c in right:
        sentence = build_sentence(c, sentence)
    return sentence


def parse_say(node):
    def is_entity(w):
        """判断是否为实体"""
        return w.POSTAG.startswith('n')

    entity = None

    # 查找说话实体
    children = node.children.values()
    for word in children:
        if word.DEPREL == '主谓关系':
            if is_entity(word):
                entity = word
                break
            else:
                return None, None
        elif word.DEPREL == '状中结构' and not entity:
            # 状中结构查找实体
            entity = search_trie(word, is_entity)
            if entity:
                break
        else:
            pass
    if not entity:
        return None, None
    # 获取实体说的话
    exclude_relation = {'主谓关系', '状中结构', '间宾关系', '左附加关系', '右附加关系'}  # 非说话内容关系
    sentence = ''
    speck_words = [c for c in children if c.DEPREL not in exclude_relation]
    if len(speck_words) == 1 and speck_words[0].CPOSTAG == 'wp':
        return None, None
    for w in speck_words:
        sentence += build_sentence(w)
    # 加上实体的修饰词
    say_entity = build_sentence(entity)
    return say_entity, sentence

## 2.
def search_speck(word_trie, say_words):
    """
    查找说话实体及内容
    :param word_trie:
    :param say_words:
    :return:
    """
    unseen = [word_trie]
    while len(unseen) > 0:
        node = unseen.pop(0)
        children = node.children.values()
        unseen += children
        if node.LEMMA in say_words:
            say_entity, sentence = parse_say(node)
            if say_entity:
                return say_entity, sentence
    return None, None

## 3.
def post_process_result(text):
    # 去掉开头标点
    text = re.sub(r'^[：|:|"|“|,|，]+', '', text)
    # 去掉结尾标点
    text = re.sub(r'["|”]+$', '', text)
    return text


class Extractor:

    def extract(self, text: str) -> [['entity', 'standpoint']]:
        """
        根据文本提取人物言论
        :param text:
        :return:
        """
        raise NotImplementedError


class SIFExtractor(Extractor):
    """
    基于SIF方法计算句子相似度，来判断句子结束
    """

    def __init__(self, sif_model: SIFModel, say_words):
        self.sif_model = sif_model
        self.say_words = say_words
        self.similarity_threshold = 0.5

    def extract(self, text):
        return self._extract(text)

    def _extract(self, text):
        def flush_cache(r, c):
            if len(r) > 0 and len(c) > 0:
                r[-1][-1] = ''.join(c)
                c.clear()

        result = []
        cache = []
        for s in cut_sentences(text):
            sen_type, entity, sentence = self._search_dependency(s)
            if 'first' == sen_type:     # 包含说话实体
                flush_cache(result, cache)
                result.append([entity, sentence])
                cache.append(sentence)
            elif 'next' == sen_type and len(cache) > 0:     # 依赖与上文的句子
                cache.append(sentence)
            elif 'candidate' == sen_type and len(cache) > 0 and self._predict(sentence, cache):     # 完整的句子，需要判断
                cache.append(sentence)
            else:
                flush_cache(result, cache)
        flush_cache(result, cache)
        return [[i[0], post_process_result(i[1])] for i in result]

    def _search_dependency(self, sentence):
        """
        分析句子结构
        :param sentence:
        :return:
        """
        _, trie = parse_sentence(sentence)
        # 寻找说语句
        entity, s = search_speck(trie, self.say_words)
        if entity:
            return 'first', entity, s
        # 没有找到说语句，则分析句子结构
        children = trie.children.values()
        for c in children:
            if c.DEPREL == '主谓关系':
                if c.POSTAG == 'r':
                    return 'next', None, sentence  # 主语是代词，依赖于前面的句子
                else:
                    return 'candidate', None, sentence  # 完全独立的句子，待确定
        return None, None, None

    def _predict(self, sentence, cache):
        """ 根据句子相似度判断 """
        similarity = self.sif_model.sentence_similarity(sentence, ''.join(cache))
        return similarity > self.similarity_threshold


class SpeckExtractor(Extractor):
    """
    基于rnn判断一句话能否作为人说的话，来判断句子结束
    """

    def __init__(self, speck_model: BiRNN, say_words):
        self.say_words = say_words
        self.speck_model = speck_model

    def extract(self, text):
        return self._extract(text)

    def _extract(self, text):
        def flush_cache(r, c):
            if len(r) > 0 and len(c) > 0:
                r[-1][-1] = ''.join(c)
                c.clear()

        result = []
        cache = []
        for s in cut_sentences(text):
            entity, sentence = self._search_dependency(s)
            if sentence and self._predict(sentence, cache):
                flush_cache(result, cache)
                result.append([entity, sentence])
                cache.append(sentence)
            elif len(cache) > 0 and self._predict(s, cache):
                cache.append(s)
            else:
                flush_cache(result, cache)
        flush_cache(result, cache)
        return [[i[0], post_process_result(i[1])] for i in result]

    def _search_dependency(self, sentence):
        _, trie = parse_sentence(sentence)
        return search_speck(trie, self.say_words)

    def _predict(self, sentence, cache):
        """ 根据rnn模型判断 """
        return self.speck_model.predict(sentence)[0]


class SpeckSIFExtractor(SpeckExtractor):
    """
    综合句子相似度和rnn模型判断：
    rnn判断结果为True则直接返回
    rnn判断结果为False且可信度大于阈值则返回False
    rnn判断结果为False且可信度小于阈值则根据相似度判断
    """

    def __init__(self, speck_model: BiRNN, sif_model: SIFModel, say_words):
        super().__init__(speck_model, say_words)
        self.sif_model = sif_model
        self.similarity_threshold = 0.5
        self.prob_threshold = 1

    def _predict(self, sentence, cache):
        flag, prob = self.speck_model.predict(sentence)
        if flag:    # rnn判断结果为True
            return True
        else:
            if prob > self.prob_threshold:      # 可信度大于阈值
                return False
        if len(cache) == 0:
            return False
        # 根据相似度判断
        similarity = self.sif_model.sentence_similarity(sentence, ''.join(cache))
        return similarity > self.similarity_threshold
