import pytest


@pytest.mark.parametrize("sentence", [
    "今天的谷歌，是一个颇为平庸的公司。",
    "虽然它搞出了一些很亮眼的技术，但对人的帮助来讲，它远不像过去那么大。"
])
def test_sentence2vec(sif_model, sentence):
    sen_embdding = sif_model.sentence2vec([sentence])
    print(sentence, ":", sen_embdding.shape)
    print(sen_embdding)
    print('*' * 50)


@pytest.mark.parametrize(("s1", "s2"), [
    ("腾讯从来没有过ToB的基因。前些天还跟一些朋友讲就说他们，做云计算的就一直堵在人家企业门口，甚至主动给人家企业先打个一百万进去，说你把数据迁移到我这里。"
     "发现他整个企业做这种服务是完全跟不上的，没有这个基因，你不用想，就像恐龙想去冰河时代生活。",
     "腾讯是一个对社会真是没有危害的公司，但是你说要带给大家多少惊喜，微信之后的我也真说不出来。"),
    ("腾讯从来没有过ToB的基因。",
     "前些天还跟一些朋友讲就说他们，做云计算的就一直堵在人家企业门口，甚至主动给人家企业先打个一百万进去，说你把数据迁移到我这里。"),
    ("腾讯从来没有过ToB的基因。",
     "发现他整个企业做这种服务是完全跟不上的，没有这个基因，你不用想，就像恐龙想去冰河时代生活。")
])
def test_sentence_similarity(sif_model, s1, s2):
    print(sif_model.sentence_similarity(s1, s2))
