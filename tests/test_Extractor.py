import pytest

from flaskr.extractor import SIFExtractor, SpeckExtractor


@pytest.mark.parametrize("sentence", [
    '近日，腾讯原副总裁吴军接受《头条有约》采访时表示，腾讯从来没有To B的基因。',
    '一位路人告诉记者，“没人认出他们俩”。',
    '声明中指出，示威者于8月12及13日围堵机场的行为，已对香港国际机场的声誉和经济造成严重损害，更带来不可估量的损失。',
    '陈恒当地时间５日指出，对于许多分散在美东各州的乡亲来说，纽约因为便利生活而成为他们的“故乡”',
    '谷歌之所以说有时候发展不行，跟这个CEO（桑达尔˙皮查伊）平庸也有很大的关系。'
])
def test_sif_extractor(sif_model, say_words, sentence):
    extractor = SIFExtractor(sif_model, say_words)
    print(extractor.extract(sentence))


@pytest.mark.parametrize("sentence", [
    '近日，腾讯原副总裁吴军接受《头条有约》采访时表示，腾讯从来没有To B的基因。',
    '一位路人告诉记者，“没人认出他们俩”。',
    '声明中指出，示威者于8月12及13日围堵机场的行为，已对香港国际机场的声誉和经济造成严重损害，更带来不可估量的损失。',
    '陈恒当地时间５日指出，对于许多分散在美东各州的乡亲来说，纽约因为便利生活而成为他们的“故乡”',
    '谷歌之所以说有时候发展不行，跟这个CEO（桑达尔˙皮查伊）平庸也有很大的关系。'
])
def test_speck_extractor(speck_model, say_words, sentence):
    extractor = SpeckExtractor(speck_model, say_words)
    print(extractor.extract(sentence))
