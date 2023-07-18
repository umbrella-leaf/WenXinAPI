import asyncio

from WenXinAPI.V1 import ChatBot


async def main():
    chatbot = ChatBot(
        api_key="OZsbQZGeGKktgPbzhow2KRPZ",
        secret_key="0PPBxji0T5pZUaF6GX8y6hgP0PvsV74z"
    )
    print(await chatbot.ask(prompt="你好！"))
    # print(await chatbot.ask(prompt="你叫什么名字？"))
    # print(await chatbot.ask(prompt="我很喜欢你"))


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())