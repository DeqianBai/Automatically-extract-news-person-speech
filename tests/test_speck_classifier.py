import pytest
from flaskr.speck_classifier import *


@pytest.mark.parametrize("source", [r'instance/vocabulary.txt'])
def test_load_vocabulary(source):
    counter = load_vocabulary(source)
    print(counter['的'])


@pytest.mark.parametrize("sentence", [
    '本次会议对资本市场的关注度较前几次明显提升，这将使得投资者对未来资本市场的政策预期边际转暖，有利于投资者风险偏好的进一步回升。',
    '很多技术它都是起的大早，赶了个晚集。',
    '就是说它最后一个对人类最大的贡献是安卓。',
    '百度的二号人物永远是离职的。',
    '这是 今天 看到 的 最 欢乐 的 微博 了',
    '该 政策 将 于 月 日 正式 实施',
    '近日，腾讯原副总裁吴军接受《头条有约》采访时表示：腾讯从来没有To B的基因。',
    '腾讯从来没有To B的基因。',
    '吴军，原腾讯副总裁。',
    '吴军也是当前Google中日韩文搜索算法的主要设计者。著有《数学之美》、《浪潮之巅》和《文明之光》等畅销书。',
    '而吴军今天这样一番言论，有人认为说的好，很有道理，有人觉得吴军过于狂妄自大了。你们怎么看呢？',
    '有时候发展不行，跟这个CEO（桑达尔˙皮查伊）平庸也有很大的关系。',
    '就是说它最后一个对人类最大的贡献是安卓。',
    '中方的反制手段是充足的，但在当前形势下，我们认为应该讨论的问题是取消对5500亿美元中国商品进一步加征关税，防止贸易战继续升级。'
])
def test_model(speck_model, sentence):
    print(sentence, speck_model.predict(sentence))
