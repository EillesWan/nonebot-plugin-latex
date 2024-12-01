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

__version__ = "0.0.1"

__author__ = "Eilles"

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="LaTeX图形渲染插件",
    description="从互联网服务渲染LaTeX公式并发送",
    usage="发送 latex 或 公式，后接内容或回复公式信息。",
    type="application",
    homepage="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai",
    extra={"License": "Mulan PSL v2", "Author": __author__},
)

from .main import *