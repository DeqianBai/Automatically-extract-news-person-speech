import collections
from flaskr.utils import *
from mxnet import nd
from mxnet.gluon import nn, rnn
from mxnet.contrib import text


class BiRNN(nn.Block):
    """
    双向循环神经网络模型
    在这个模型中，每个词先通过嵌入层得到特征向量。然后，我们使用双向循环神经网络对特征序列进一步编码得到序列信息。
    最后，我们将编码的序列信息通过全连接层变换为输出。具体来说，我们可以将双向长短期记忆在最初时间步和最终时间步的隐藏状态连结，
    作为特征序列的表征传递给输出层分类。在下面实现的`BiRNN`类中，`Embedding`实例即嵌入层，`LSTM`实例即为序列编码的隐藏层，
    `Dense`实例即生成分类结果的输出层。
    """

    def __init__(self, vocab, embed_size=100, num_hiddens=100, num_layers=2, **kwargs):
        super(BiRNN, self).__init__(**kwargs)
        self.vocab = vocab
        self.embedding = nn.Embedding(len(vocab), embed_size)
        # bidirectional设为True即得到双向循环神经网络
        self.encoder = rnn.LSTM(num_hiddens, num_layers=num_layers, bidirectional=True, input_size=embed_size)
        self.decoder = nn.Dense(2)

    def forward(self, inputs):
        # inputs的形状是(批量大小, 词数)，因为LSTM需要将序列作为第一维，所以将输入转置后
        # 再提取词特征，输出形状为(词数, 批量大小, 词向量维度)
        embeddings = self.embedding(inputs.T)
        # rnn.LSTM只传入输入embeddings，因此只返回最后一层的隐藏层在各时间步的隐藏状态。
        # outputs形状是(词数, 批量大小, 2 * 隐藏单元个数)
        outputs = self.encoder(embeddings)
        # 连结初始时间步和最终时间步的隐藏状态作为全连接层输入。它的形状为
        # (批量大小, 4 * 隐藏单元个数)。
        encoding = nd.concat(outputs[0], outputs[-1])
        outs = self.decoder(encoding)
        return outs

    def predict(self, sentence):
        sentence = nd.array(self.vocab.to_indices(cut(sentence)))
        prob = self(sentence.reshape((1, -1)))
        label = nd.argmax(prob, axis=1)
        return True if label.asscalar() == 1 else False, max(0, (prob[0, 0] - prob[0, 1]).asscalar())


def load_vocabulary(source, encoding='utf-8'):
    """
    加载词汇表
    :param source: 文件路径
    :param encoding:
    :return:
    """
    counter = collections.Counter()
    with open(source, encoding=encoding) as f:
        for line in f:
            s = line.strip().split(' ')
            counter[s[0]] = int(s[1])
    return text.vocab.Vocabulary(counter, min_freq=5)


def load_model(model_path, vocab):
    """
    加载已训练rnn模型
    :param model_path: 模型文件路径
    :param vocab:  词汇表
    :return:
    """
    net = BiRNN(vocab)
    net.load_parameters(model_path)
    return net
