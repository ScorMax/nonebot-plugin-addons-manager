from pydantic import BaseModel
from typing import List

class Config(BaseModel):
    admin_qq:List[int]=[]
    destination_path:str=r"/root/Steam/steamapps/common/Left 4 Dead 2 Dedicated Server/left4dead2/addons"

