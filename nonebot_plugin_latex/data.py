"""
数据类


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

from typing import Optional, Literal, Tuple
import httpx
import time
import re


class ConvertChannel:
    URL: str

    async def get_to_convert(
        self,
        latex_code: str,
        dpi: int = 600,
        fgcolour: str = "000000",
        timeout: int = 5,
        retry: int = 3,
    ) -> Tuple[Literal[True], bytes] | Tuple[Literal[False], bytes | str]:
        return False, "请勿直接调用母类"

    @staticmethod
    def channel_test() -> int:
        return -1


class L2PChannel(ConvertChannel):

    URL = "http://www.latex2png.com"

    async def get_to_convert(
        self,
        latex_code: str,
        dpi: int = 600,
        fgcolour: str = "000000",
        timeout: int = 5,
        retry: int = 3,
    ) -> Tuple[Literal[True], bytes] | Tuple[Literal[False], bytes | str]:

        async with httpx.AsyncClient(
            timeout=timeout,
        ) as client:
            while retry > 0:
                try:
                    post_response = await client.post(
                        self.URL + "/api/convert",
                        json={
                            "auth": {"user": "guest", "password": "guest"},
                            "latex": latex_code,
                            "resolution": dpi,
                            "color": fgcolour,
                        },
                    )
                    if post_response.status_code == 200:

                        if (json_response := post_response.json())[
                            "result-message"
                        ] == "success":

                            # print("latex2png:", post_response.content)

                            if (
                                get_response := await client.get(
                                    self.URL + json_response["url"]
                                )
                            ).status_code == 200:
                                return True, get_response.content
                        else:
                            return False, json_response["result-message"]
                    retry -= 1
                except httpx.TimeoutException:
                    retry -= 1
            raise ConnectionError("服务不可用")
        return False, "未知错误"

    @staticmethod
    def channel_test() -> int:
        with httpx.Client(timeout=5) as client:
            try:
                start_time = time.time_ns()
                latex2png = (
                    client.get(
                        "http://www.latex2png.com{}"
                        + client.post(
                            "http://www.latex2png.com/api/convert",
                            json={
                                "auth": {"user": "guest", "password": "guest"},
                                "latex": "\\\\int_{a}^{b} x^2 \\\\, dx = \\\\frac{b^3}{3} - \\\\frac{a^3}{5}\n",
                                "resolution": 600,
                                "color": "000000",
                            },
                        ).json()["url"]
                    ),
                    time.time_ns() - start_time,
                )
            except:
                return 99999
        if latex2png[0].status_code == 200:
            return latex2png[1]
        else:
            return 99999


class CDCChannel(ConvertChannel):

    URL = "http://latex.codecogs.com"

    async def get_to_convert(
        self,
        latex_code: str,
        dpi: int = 600,
        fgcolour: str = "000000",
        timeout: int = 5,
        retry: int = 3,
    ) -> Tuple[Literal[True], bytes] | Tuple[Literal[False], bytes | str]:
        async with httpx.AsyncClient(
            timeout=timeout,
        ) as client:

            while retry > 0:
                try:
                    response = await client.get(
                        self.URL
                        + r"/png.image?\huge&space;\dpi{"
                        + str(dpi)
                        + r"}\fg{"
                        + fgcolour
                        + r"}"
                        + latex_code
                    )
                    # print("codecogs:", response)
                    if response.status_code == 200:
                        return True, response.content
                    else:
                        return False, response.content
                    retry -= 1
                except httpx.TimeoutException:
                    retry -= 1
        return False, "未知错误"

    @staticmethod
    def channel_test() -> int:
        with httpx.Client(timeout=5) as client:
            try:
                start_time = time.time_ns()
                codecogs = (
                    client.get(
                        r"http://latex.codecogs.com/png.image?\huge%20\dpi{600}\\int_{a}^{b}x^2\\,dx=\\frac{b^3}{3}-\\frac{a^3}{5}"
                    ),
                    time.time_ns() - start_time,
                )
            except:
                return 99999
        if codecogs[0].status_code == 200:
            return codecogs[1]
        else:
            return 99999


class JRTChannel(ConvertChannel):

    URL = "http://latex2image.joeraut.com"

    async def get_to_convert(
        self,
        latex_code: str,
        dpi: int = 600,
        fgcolour: str = "000000",  # 无效设置
        timeout: int = 5,
        retry: int = 3,
    ) -> Tuple[Literal[True], bytes] | Tuple[Literal[False], bytes | str]:

        async with httpx.AsyncClient(
            timeout=timeout,
        ) as client:
            while retry > 0:
                try:
                    post_response = await client.post(
                        self.URL + "/default/latex2image",
                        json={
                            "latexInput": latex_code,
                            "outputFormat": "PNG",
                            "outputScale": "{}%".format(dpi / 3 * 5),
                        },
                    )
                    print(post_response)
                    if post_response.status_code == 200:

                        if not (json_response := post_response.json())["error"]:

                            # print("latex2png:", post_response.content)

                            if (
                                get_response := await client.get(
                                    json_response["imageUrl"]
                                )
                            ).status_code == 200:
                                return True, get_response.content
                        else:
                            return False, json_response["error"]
                    retry -= 1
                except httpx.TimeoutException:
                    retry -= 1
            raise ConnectionError("服务不可用")
        return False, "未知错误"

    @staticmethod
    def channel_test() -> int:
        with httpx.Client(timeout=5) as client:
            try:
                start_time = time.time_ns()
                joeraut = (
                    client.get(
                        client.post(
                            "http://www.latex2png.com/api/convert",
                            json={
                                "latexInput": "\\\\int_{a}^{b} x^2 \\\\, dx = \\\\frac{b^3}{3} - \\\\frac{a^3}{5}",
                                "outputFormat": "PNG",
                                "outputScale": "1000%",
                            },
                        ).json()["imageUrl"]
                    ),
                    time.time_ns() - start_time,
                )
            except:
                return 99999
        if joeraut[0].status_code == 200:
            return joeraut[1]
        else:
            return 99999


CHANNEL_LIST: list[type[ConvertChannel]] = [L2PChannel, CDCChannel, JRTChannel]


class ConvertLatex:

    channel: ConvertChannel

    def __init__(self, channel: Optional[ConvertChannel] = None) -> None:
        """
        LaTeX在线渲染类

        Args:
            channel (Optional[ConvertChannel], optional):
                选择何种在线转换通道，若为空，则自动选择延迟最低的通道。默认为空。
                [WARNING] 请注意！选择通道时采取的是同步函数，因此可能造成阻塞。
        """

        if channel is None:
            self.channel = self.auto_choose_channel()
        else:
            self.channel = channel

    async def generate_png(
        self,
        latex: str,
        dpi: int = 600,
        foreground_colour: str = "000000",
        timeout_: int = 5,
        retry_: int = 3,
    ) -> Tuple[Literal[True], bytes] | Tuple[Literal[False], bytes | str]:
        """
        LaTeX 在线渲染

        参数
        ====

            latex: str
                LaTeX 代码
            dpi: int
                分辨率
            foreground_colour: str
                文字前景色
            timeout_: int
                超时时间
            retry_: int
                重试次数
        返回
        ====
            bytes
            图片
        """
        return await self.channel.get_to_convert(
            latex, dpi, foreground_colour, timeout_, retry_
        )

    @staticmethod
    def auto_choose_channel() -> ConvertChannel:

        return min(
            CHANNEL_LIST,
            key=lambda channel: channel.channel_test(),
        )()


# 正则匹配 LaTeX 公式内容
LATEX_PATTERN = re.compile(
    r"\\begin\{equation\}(.*?)\\end\{equation\}|(?<!\$)(\$(.*?)\$|\$\$(.*?)\$\$|\\\[(.*?)\\\]|\\\[.*?\\\]|\\\((.*?)\\\))",
    re.DOTALL,
)
