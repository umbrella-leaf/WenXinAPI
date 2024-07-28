from pathlib import Path

from setuptools import setup, find_namespace_packages

PATH = Path("README.md")

VERSION_PATH = Path(__file__).parents[0] / "src/WenXinAPI/version.py"
with open(VERSION_PATH, encoding="utf-8") as f:
    version = f.read().split('"')[1]

description = "WenXinAPI is a simple wrapper for the official WenXin API"

setup(
    name="revWenXin",
    version=version,
    description=description,
    long_description=open(PATH, encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/umbrella-leaf/WenXinAPI",
    author="Zhongnuo Liu",
    author_email="2313678365@qq.com",
    license="Apache-2.0 license",
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    py_modules=["WenXinAPI"],
    install_requires=[
        "httpx"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
