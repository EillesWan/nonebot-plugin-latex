"""
NoneBot2 LaTeX图形渲染插件
nonebot-plugin-latex

Copyright (c) 2024 金羿Eilles
nonebot-plugin-latex is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:
         http://license.coscl.org.cn/MulanPSL2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""

from nonebot import get_plugin_config, get_driver
from nonebot.plugin import PluginMetadata

from .config import Config
from .converter import _converter, get_converter

__version__ = "0.0.3.2"

__author__ = "Eilles"

__plugin_meta__ = PluginMetadata(
    name="LaTeX 在线渲染插件",
    description="从互联网服务渲染 LaTeX 公式",
    usage="发送 latex 或 公式，后接内容或回复公式信息。",
    type="library",
    homepage="https://github.com/EillesWan/nonebot-plugin-latex",
    config=Config,
    supported_adapters={
        "nonebot.adapters.telegram",
        "nonebot.adapters.dodo",
        "nonebot_adapter_tailchat",
        "nonebot.adapters.onebot.v11",
        "nonebot.adapters.minecraft",
        "nonebot.adapters.github",
        "nonebot.adapters.discord",
        "nonebot.adapters.mail",
        "nonebot.adapters.ding",
        "nonebot.adapters.console",
        "nonebot.adapters.qq",
        "nonebot.adapters.kritor",
        "nonebot.adapters.feishu",
        "nonebot.adapters.red",
        "nonebot.adapters.satori",
        "nonebot.adapters.onebot.v12",
        "nonebot.adapters.kaiheila",
        "nonebot.adapters.mirai",
        "nonebot.adapters.ntchat",
    },  # inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "Mulan PSL v2", "Author": __author__},
)

__all__ = ["get_converter"]


@get_driver().on_startup
async def init():
    await _converter.load_channel()


config = get_plugin_config(Config)


if config.latex_enable_as_application:
    from .main import *
