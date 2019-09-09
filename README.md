# 新闻言论观点提取


 输入: 一段新闻文本(Text)

 输出: 文中每个人物/实体的观点(List)
 
 地址： http://39.100.3.165:8871/

## 1. Getting Started

### Prerequisites


### Installing
-------
1. 获取项目源码 :

       # clone the repository
       $ git clone https://github.com/4keyboardman/StandpointExtract.git
       $ cd StandpointExtract

2. 创建虚拟环境并激活:

   linux系统运行

       $ python3 -m venv venv
       $ . venv/bin/activate

   Windows系统运行cmd

       $ py -3 -m venv venv
       $ venv\Scripts\activate.bat

3. 安装项目:

       $ pip install -e .

4. 下载pyhanlp需要的数据包

   下载 [data](http://nlp.hankcs.com/download.php?file=data)

   下载 [jar与配置文件](http://nlp.hankcs.com/download.php?file=jar)

   将下载好的文件直接放在`pyhanlp`模块的`static`文件夹下：

      `StandpointExtract/venv/lib/python3.6/site-packages/pyhanlp/static/ `

   在终端执行如下命令进行测试，查看pyhanlp是否安装成功

       $ hanlp

       详情参考：https://github.com/hankcs/pyhanlp/wiki/%E6%89%8B%E5%8A%A8%E9%85%8D%E7%BD%AE
   如果报错，可以[参考这里](https://www.jianshu.com/writer#/notebooks/35711942/notes/53734788/preview)

5. 下载模型文件放在项目根目录下

   下载模型：https://pan.baidu.com/s/1hE-p3YTMnxJebzthDNPJbw

   解压文件:

       $ unzip instance.zip

## 2. Running 
---
linux系统运行:

    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask run

Windows系统运行cmd:

    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
    > flask run

打开浏览器访问 http://127.0.0.1:5000

使用gunicorn启动：

    $ gunicorn -D -w 1 -b 0.0.0.0:8871 "flaskr:create_app()"

api command
---
    GET /cmd/model/reload: 重新加载instance中的模型文件
    GET /cmd/extractor: 查询当前使用的判断句子结束的模型类型
    GET /cmd/extractor/{type}: 设置判断句子结束的方法，type类型: 
        sif-句子相似度
        rnn-是否是人说的话
        mix-两者综合，默认类型
        
## Acknowledgments
---

- flask文档：https://dormousehole.readthedocs.io/en/latest/
- pyhanlp：https://github.com/hankcs/pyhanlp
- hanlp在线演示：http://hanlp.com/
- 普林斯顿句子向量论文：https://openreview.net/forum?id=SyK00v5xx
- 论文代码：https://github.com/PrincetonML/SIF
- 论文解读：https://blog.csdn.net/sinat_31188625/article/details/72677088#commentsedit
- 解读代码：https://github.com/jx00109/sentence2vec/blob/master/s2v-python3.py
- 云浮科技句法分析：https://www.yunfutech.com/demo?tab=1

