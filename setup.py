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
        "anyio==3.7.1",
        "certifi==2023.5.7",
        "exceptiongroup==1.1.2",
        "h11==0.14.0",
        "httpcore==0.17.3",
        "httpx==0.24.1",
        "idna==3.4",
        "sniffio==1.3.0",
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
