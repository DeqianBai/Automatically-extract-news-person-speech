## LTP installation and virtualenv usage
    我没有使用aconda，所以构建虚拟环境使用的是virtualenv，我的系统是Ubuntu18
### virtualenv 
* 安装
```
pip3 install virtualenv   
sudo pip install virtualenvwrapper （这个是虚拟环境中包管理工具）
```
* 创建虚拟环境存放文件
```
mkdir ~./virtualenvs
```
* 配置 
```
cd ~/.bashrc
在该文件中添加下面语句
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
使得配置生效
source ~/.bashrc
```
* 基本使用语法
    1. 创建虚拟环境，有在Python2下的，有在Python3下的
	默认是Python2 下的，例如创建flask的虚拟环境： mkvirtualenv py_flask
	python3下的： mkvirtualenv -p python3 py3_flask (两者都需要联网)
    2. 使用virtualenvwrapper的命令来管理虚拟环境
	workon ：查看有哪些虚拟环境
	workon  xxx： 使用xxx虚拟环境
	deactivate：退出虚拟环境
	rmvirtualenv xxx：删除xxx虚拟环境
    3. 进入xxx虚拟环境后，在该环境安装的包，都会安装在~/.virtualenvs/xxx下
    4. 进入xxx环境后，pip freeze：查看安装了哪些包

### LTP installation
* 最好在虚拟环境中安装，例如先进入py3_flask: workon py3_flask
* 没使用pip安装，很可能出问题，使用源码安装
[LTP](https://github.com/HIT-SCIR/pyltp)
```
 $ git clone https://github.com/HIT-SCIR/pyltp
 $ git submodule init
 $ git submodule update
 $ python setup.py install
```
* 下载model文件
[model 文件](http://ltp.ai/download.html)下载model栏中第一个即可，下载后将其解压在pyltp路径中，具体例子测试参照
[LTP](https://github.com/HIT-SCIR/pyltp)，要说明的是，导入模型的路径最好填写绝对路径，我测试没问题
### jupyter-notebook使用安装了LTP的虚拟环境
* 如果不是安装在虚拟环境中的，那么直接可以使用LTP
* 否则，参照[虚拟环境使用jupyter-notebook](http://umi101108.com/2017/09/26/%E4%BD%BF%E7%94%A8%E7%89%B9%E5%AE%9A%E8%99%9A%E6%8B%9F%E7%8E%AF%E5%A2%83virtualenv-%E8%BF%90%E8%A1%8CJupyter-Notebook/)，注意，要将文中虚拟环境名改为自己的环境名
