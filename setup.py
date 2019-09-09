import io

from setuptools import find_packages
from setuptools import setup

with io.open("INSTALL.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="StandpointExtract",
    version="1.0.0",
    url="https://github.com/4keyboardman/StandpointExtract",
    license="BSD",
    maintainer="4keyboardman",
    maintainer_email="fyjun2071@163.com",
    description="新闻人物观点自动提取",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", 'pyhanlp', 'gensim', 'scikit-learn', 'numpy', 'jieba', 'mxnet'],
    extras_require={"test": ["pytest", "coverage"]},
)
