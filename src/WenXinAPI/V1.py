"""
对百度文心一言API的简单封装，支持多用户和上下文
"""
import json
import re
import httpx
import asyncio
import threading
from typing import AsyncGenerator

from WenXinAPI import typings as t
from WenXinAPI.typings import ENGINE, ENDPOINT, ROLE


ENGINES = [engine.value for engine in ENGINE]


class ChatBot:
    """
    文心官方API封装的机器人类
    """
    regNonWord = re.compile(r'\W+')  # 匹配连续的非单词(非字母、数字以及汉字，即匹配标点符号与空白，作为单词分隔符）
    regHanzi = re.compile(r"([\u4e00-\u9fa5])")  # 匹配单个汉字
    lock = threading.Lock()  # 限制并发使用的锁

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            engine: str = "ERNIE-Bot-turbo",
            timeout: float = None,
            max_tokens: int = None,
            temperature: float = 0.95,
            top_p: float = 0.8,
            penalty_score: float = 1.0,
            truncate_limit: int = None
    ) -> None:
        """
        初始化文心API机器人，需要用到百度智能云平台的API_KEY和SECRET_KEY (地址 https://console.bce.baidu.com/ai/#/ai/wenxinworkshop/app/list)
        :param api_key: 文心千帆应用的的API Key
        :param secret_key:文心千帆应用的的Secret Key
        :param engine: 使用引擎
        :param timeout: 超时时间
        :param max_tokens: 单轮对话最长token数
        :param temperature: 影响回答随机性，值越高随机性越强，默认值0.95
        :param top_p: 影响回答文本多样性，值越大多样性越强，默认值0.8
        :param penalty_score: 对已生成的token增加惩罚，减少重复生成的现象，值越大表示惩罚越大，默认值1.0
        :param truncate_limit: 截断对话的限制token数
        """
        # 初始化机器人参数
        if engine not in ENGINES:
            raise t.ActionsError(f"引擎 {engine} 不被支持， 请从 {ENGINES} 中选择！")
        self.engine: ENGINE = ENGINE(engine)
        # 获取请求地址endpoint
        self.endpoint: str = getattr(ENDPOINT, self.engine.name).value
        self.api_key: str = api_key
        self.secret_key: str = secret_key
        self.timeout: float = timeout
        self.max_tokens: int = max_tokens or 2000
        self.temperature: float = temperature
        self.top_p: float = top_p
        self.penalty_score: float = penalty_score
        self.truncate_limit: int = truncate_limit or 2000
        self._access_token: str = ""
        asyncio.get_event_loop().create_task(self.get_access_token())

        # 初始化请求session
        self.session = httpx.AsyncClient(
            follow_redirects=True,
            timeout=timeout,
        )

        # 初始化对话字典（每一项储存单个用户全部对话）
        self.conversations: dict[str, list[dict]] = {
            "default": []
        }

    def add_to_conversation(
            self,
            message: str,
            role: ROLE,
            convo_id: str = "default"
    ) -> None:
        """
        向convo_id对应的会话中添加一条对话message
        :param message: 对话内容
        :param role: 对话角色类型
        :param convo_id: 会话id，默认值“default”
        :return:
        """
        if self.get_message_token_count(message) > self.max_tokens:
            raise t.ActionsError(f"单次对话长度超过最大长度{self.max_tokens}")
        self.conversations[convo_id].append({
            "role": role.value,
            "content": message,
        })

    def __truncate_conversation(self, convo_id: str = "default") -> None:
        """
        截断convo_id对应的用户会话（删去最早的历史记录）
        :param convo_id: 会话id，默认值"default"
        :return:
        """
        while True:
            if (
                self.get_token_count(convo_id=convo_id) > self.truncate_limit
                and len(self.conversations[convo_id]) > 1
            ):
                # 截断最早的一条对话
                self.conversations[convo_id].pop(0)
            else:
                break

    def IsHanzi(self, string: str) -> bool:
        """判断字符是否是汉字"""
        return True if self.regHanzi.search(string) else False

    def get_message_token_count(self, message: str) -> int:
        """
        计算单条对话的总token数，计算公式为：汉字数+英文单词数*1.3
        :param message: 对话内容
        :return: 对话的总token数
        """
        num_tokens: float = 0.0

        words = self.regNonWord.split(message)  # 分割得到消息的单词列表
        # 对列表中每个单词分成单个汉字和英文单词（如果有），然后进行token统计
        for word in words:
            partitions = self.regHanzi.split(word)
            for partition in partitions:
                # 非空则按公式计算
                if len(partition.strip()) > 0:
                    num_tokens += 1 if self.IsHanzi(partition) else 1.3

        return int(num_tokens)

    def get_token_count(self, convo_id: str = "default") -> int:
        """
        计算convo_id对应的会话的总token数
        :param convo_id: 会话id，默认值"default"
        :return: 会话所有内容的总token数
        """
        num_tokens: int = 0
        for message in self.conversations[convo_id]:
            num_tokens += self.get_message_token_count(message=message["content"])
        return num_tokens

    async def get_access_token(self, refresh: bool = False) -> str:
        """
        通过api_key和secret_key获取access_token
        :param refresh: 为True则强制刷新access_token，默认值False
        :return: 文心API访问凭证access_token
        """
        # 如果没有现成的access_token或者强制刷新，则调用鉴权接口获取；
        if len(self._access_token) == 0 or refresh:
            oauth_url = "https://aip.baidubce.com/oauth/2.0/token"
            response = (await self.session.post(
                url=oauth_url,
                params={
                    "grant_type": "client_credentials",
                    "client_id": self.api_key,
                    "client_secret": self.secret_key
                },
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            )).json()
            if response.get("error"):
                error_description = response.get("error_description")
                if error_description == "unknown client id":
                    raise t.AuthenticationError("API_KEY不正确！")
                raise t.AuthenticationError("SECRET_KEY不正确！")
            self._access_token = response.get("access_token")
        return self._access_token

    async def send_request(self, convo_id: str = "default", **kwargs) -> AsyncGenerator[str, None]:
        """
        发送API请求的实际函数，含token过期重试逻辑
        :param convo_id: 会话id，默认值"default"
        :return: 回答文本异步生成器
        """
        # 获取鉴权密钥access_token
        access_token = await self.get_access_token()
        # 获取回答，默认异步
        async with self.session.stream(
                method="post",
                url=f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.endpoint}",
                params={"access_token": access_token},
                json={
                    "messages": self.conversations[convo_id],
                    "stream": True,
                    # 可选参数，为方便起见一并传输
                    "temperature": kwargs.get("temperature", self.temperature),
                    "top_p": kwargs.get("top_p", self.top_p),
                    "penalty_score": kwargs.get("penalty_score", self.penalty_score),
                    "user_id": convo_id,
                },
                timeout=kwargs.get("timeout", self.timeout),
        ) as response:
            if response.status_code != 200:
                await response.aread()
                raise t.APIConnectionError(
                    f"{response.status_code} {response.reason_phrase} {response.text}"
                )
            async for line in response.aiter_lines():
                line = line.strip()
                if not line:
                    continue
                # 单行以"data: "开头，说明正常返回
                if line.startswith("data: "):
                    # 去除 "data: "
                    line = line[6:]
                resp: dict = json.loads(line)
                error_code: int = resp.get("error_code")
                is_end: bool = resp.get("is_end")
                first_sentence: bool = True if resp.get("sentence_id") == 0 else False
                # 错误码111说明token过期，此时应该重新获取token并再次发起请求，而非抛出错误
                if error_code and error_code == 111:
                    await self.get_access_token(refresh=True)
                    async for content in self.send_request(convo_id, **kwargs):
                        yield content
                    break
                # 否则如果出错，直接抛出响应错误
                elif error_code:
                    raise t.ResponseError(f"{error_code} {resp.get('error_msg')}")
                # 否则按正常流程执行，is_end为真且不是第一个回答则说明回答结束
                elif is_end and (not first_sentence):
                    break
                else:
                    content: str = resp.get("result")
                    yield content

    async def ask_stream(
            self,
            prompt: str,
            convo_id: str = "default",
            **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        调用文心API进行某个会话的问答，默认异步
        :param prompt: 用户问题
        :param convo_id: 会话id，默认值"default"
        :return: 回答文本的异步生成器
        """
        # 如果会话不存在则创建
        if convo_id not in self.conversations:
            self.reset(convo_id=convo_id)
        self.add_to_conversation(message=prompt, role=ROLE.USER, convo_id=convo_id)
        self.__truncate_conversation(convo_id=convo_id)
        # 完整的回答文本
        full_response: str = ""

        # 没有获得锁则一直死循环
        while not self.lock.acquire(blocking=False):
            pass
        # 获得锁则启动定时器，1s后释放，使得其他请求可以发送，这样就解决了QPS限制为1下的并发问题
        threading.Timer(interval=1, function=self.lock.release).start()

        async for content in self.send_request(convo_id=convo_id, **kwargs):
            full_response += content
            yield content
        self.add_to_conversation(full_response, ROLE.ASSISTANT, convo_id=convo_id)

    async def ask(
            self,
            prompt: str,
            convo_id: str = "default",
            **kwargs,
    ) -> str:
        """
        调用文心一言流式问答API
        :param prompt: 用户问题
        :param convo_id: 会话id，默认值"default"
        :return: 完整的回答文本
        """
        response = self.ask_stream(
            prompt=prompt,
            convo_id=convo_id,
            **kwargs,
        )
        full_response: str = "".join([r async for r in response])
        return full_response

    def reset(self, convo_id: str = "default") -> None:
        """
        重置convo_id对应的会话
        :param convo_id: 会话id，默认值"default"
        :return:
        """
        self.conversations[convo_id] = []
