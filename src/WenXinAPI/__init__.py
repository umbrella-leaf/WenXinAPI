"""
WenXinAPI的 __init__.py

通过以下写法来引入WenXinAPI:
WenXinAPI.V1
"""
from WenXinAPI.version import version

__version__ = version
__all__ = ()


def verify() -> None:
    from WenXinAPI import typings as t

    major_version = int(__import__("platform").python_version_tuple()[0])
    minor_version = int(__import__("platform").python_version_tuple()[1])
    cur_version = __import__('platform').python_version()
    if major_version < 3:
        error = t.NotAllowRunningError("该依赖包不可以在Python2上运行！")
        raise error
    elif minor_version < 6:
        error = t.NotAllowRunningError(f"Python版本不匹配！当前版本{cur_version}，至少为3.6")
        raise error
    elif minor_version < 8:
        __import__("warnings").warn(
            UserWarning(
              f"当前Python版本{cur_version}，推荐版本3.8"
            ),
        )


verify()