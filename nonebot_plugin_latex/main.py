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

from nonebot_plugin_alconna.uniseg import Text


nonebot.require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import (
    Image as Alconna_Image,
    Reply,
    Text as Alconnna_Text,
    UniMessage,
    UniMsg
)

from .data import LATEX_PATTERN
from .converter import _converter

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
    msg: UniMsg,
    # state: T_State,
) -> bool:
    """
    检查是否为 LaTeX 指令
    """
    return any(
        isinstance(seg, Text) and seg.text.strip().startswith(command_heads)
        for seg in msg
    )


latexg = nonebot.on_message(
    rule=check_for_scan,
    block=False,
    priority=90,
)


@latexg.handle()
async def handle_pic(
    msgs: UniMsg,
    # state: T_State,
    # arg: Optional[Message] = CommandArg(),
):
    # print("正在解决reply指令……")
    latexes = []
    if msgs.has(Reply):
        i = msgs[Reply, 0]
        if i.msg:
            latexes.extend(LATEX_PATTERN.finditer(i.msg if isinstance(i.msg, str) else i.msg.extract_plain_text()))

    # print(arg)
    latexes.extend(LATEX_PATTERN.finditer(msgs.extract_plain_text()))

    if not latexes:
        await latexg.finish(
            "同志！以我们目前的实力，暂时无法读取你大脑中的公式，你还是把它通过你的输入设备打出来吧。"
        )
        return

    result_msg = UniMessage()

    for tex_macher in latexes:
        tex = tex_macher.group().replace("$", "")
        if (result := await _converter.generate_png(tex))[0]:
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
