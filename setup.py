# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

AICARUS_PROTOCOL_VERSION = "1.2.0" # 与你文档中的版本号保持一致

setuptools.setup(
    name="aicarus_protocols",
    version=AICARUS_PROTOCOL_VERSION,
    author="Dax233",
    author_email="bakadax@qq.com",
    description="AIcarus 项目核心与适配器之间的通信协议定义库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AIcarusDev/AIcarus-Message-Protocol",

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),

    # Python 版本要求
    python_requires=">=3.12",
)
