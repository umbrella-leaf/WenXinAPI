# WenXinAPI

[![PyPi](https://img.shields.io/pypi/v/revWenXin.svg)](https://pypi.python.org/pypi/revWenXin)

对百度文心一言API的简单封装，支持多用户上下文对话
[github地址](https://github.com/umbrella-leaf/WenXinAPI)

## 安装

```
python -m pip install --upgrade WenXinAPI
```

## 支持Python版本

- 最小版本 - Python3.6
- 推荐 - Python3.8+

## 使用方法

### 配置方法

1. 在百度智能云的 [文心千帆平台](https://console.bce.baidu.com/ai/#/ai/wenxinworkshop/overview/index) 上申请使用资格
2. 在控制台 [应用列表页面](https://console.bce.baidu.com/ai/#/ai/wenxinworkshop/app/list) 创建应用
3. 获取并保存API_KEY和SECRET_KEY

### 使用示例（异步流式)

```python
from WenXinAPI.V1 import ChatBot
chatbot = ChatBot(
    api_key="<your API_KEY>",
    secret_key="<your SECRET_KEY>",
    engine="<ENGINE you choose>"
)
print(await chatbot.ask("你好！"))
```


