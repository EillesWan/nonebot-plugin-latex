"""
命令功能集


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

import nonebot
from nonebot.adapters.onebot.v11 import MessageEvent


# from nonebot.matcher import Matcher

nonebot.require("nonebot_plugin_alconna")

# from nonebot_plugin_alconna.util import annotation
from nonebot_plugin_alconna import (
    Image as Alconna_Image,
    Text as Alconnna_Text,
    UniMessage,
)

from .data import LATEX_PATTERN
from .converter import converter

command_heads = (
    "latex",
    "公式",
    "数学公式",
    "latex公式",
    "latex_formula",
    "latex_math",
    "公式渲染",
    "latex渲染",
)
"""
命令头
"""


async def check_for_scan(
    event: MessageEvent,
    # state: T_State,
) -> bool:
    """
    检查是否为 LaTeX 指令
    """

    # print("检查消息满足渲染要求：", event)
    if isinstance(event, MessageEvent):
        # print("此为原始信息：", event.raw_message)
        # event.message
        for msg in event.message:
            # print("这是其中一个信息---", msg)
            if msg.type == "text" and (msgdata := msg.data["text"].strip()):
                if msgdata.startswith(command_heads):

                    # print("判断：这确实是指令发出")
                    return True
                else:
                    # print("判断：这不是指令")
                    return False
        return False


latexg = nonebot.on_message(
    rule=check_for_scan,
    block=False,
    priority=90,
)


@latexg.handle()
async def handle_pic(
    event: MessageEvent,
    # state: T_State,
    # arg: Optional[Message] = CommandArg(),
):
    # print("正在解决reply指令……")
    latexes = []
    if event.reply:
        latexes.extend(LATEX_PATTERN.finditer(event.reply.message.extract_plain_text()))

    # print(arg)
    if event.message:
        latexes.extend(LATEX_PATTERN.finditer(event.message.extract_plain_text()))

    if not latexes:
        await latexg.finish(
            "同志！以我们目前的实力，暂时无法读取你大脑中的公式，你还是把它通过你的输入设备打出来吧。"
        )
        return

    result_msg = UniMessage()

    for tex_macher in latexes:
        tex = tex_macher.group().replace("$", "")
        if (result := await converter.generate_png(tex))[0]:
            result_msg.append(
                Alconna_Image(raw=result[1], mimetype="image/png", name="latex.png")  # type: ignore
            )
        else:
            if isinstance(result[1], str):
                result_msg.append(
                    Alconnna_Text("无法渲染${}$：{}".format(tex, result[1]))
                )
            else:
                result_msg.append(Alconnna_Text("无法渲染${}$".format(tex)))
                result_msg.append(
                    Alconna_Image(raw=result[1], mimetype="image/png", name="error.png")
                )

    await result_msg.send(reply_to=True)
