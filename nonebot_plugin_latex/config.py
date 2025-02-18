from pydantic import BaseModel


class Config(BaseModel):
    latex_enable_as_application: bool = False
    """
    是否启用应用逻辑：响应“latex”、“公式”指令
    """
