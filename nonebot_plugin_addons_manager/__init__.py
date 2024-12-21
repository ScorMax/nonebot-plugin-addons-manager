import nonebot
from .config import Config
import re
from pathlib import Path
from typing import  List
from nonebot import on_message, on_notice,on_command
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.params import CommandArg
from nonebot import get_plugin_config
from nonebot.adapters.onebot.v11 import (
    Event,
    Bot, GroupMessageEvent, GroupUploadNoticeEvent,PrivateMessageEvent
)
from nonebot.log import logger
import os
import aiohttp
from aiohttp import ClientTimeout
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="addons_manager",
    description="用来对v社游戏的addons文件夹进行vpk的管理，如求生之路",
    usage="将vpk文件上传至群文件可以自动下载，/file可以查询已有vpk文件，/delete可以删除文件，/rename可以重命名文件",

    type="application",

    homepage="https://github.com/ScorMax/nonebot-plugin-addons-manager",

    config=Config,

    supported_adapters={"~onebot.v11"},

)

"""
配置初始化
"""
config = get_plugin_config(Config)
destination_path=config.destination_path
admin_qq=config.admin_qq


class ExpectSignal(Exception):
    """自定义异常类，用于发出 Expect 信号"""
    pass

async def download_file(url,event,bot, filename=None):
    # 如果没有提供文件名，则从URL中提取
    if not filename:
        filename = url.split('/')[-1]

    # 确保目标文件夹存在
    if not os.path.exists(destination_path):
        await bot.send(event, destination_path + "不存在")
        return

    # 构建完整的文件路径
    file_path = os.path.join(destination_path, filename)

    timeout = ClientTimeout(total=60 * 20)  # 设置总的超时时间为20分钟
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(file_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                logger.info(f"文件已成功下载到 {file_path}")
                await bot.send(event, filename + "已成功下载,输入/file查看已加载vpk文件")
            else:
                logger.info(f"下载失败，状态码: {response.status}")
                await bot.send(event, filename + f"下载失败，状态码: {response.status}")



#捕获消息
def message_rule(event: GroupMessageEvent):
    return isinstance(event, Event)
get_file = on_message(rule=message_rule,block=False)


#返回文件夹下的所有文件
def list_files_in_directory(directory_path):
    # 确保传入的是一个目录
    if not os.path.isdir(directory_path):
        logger.info("Provided path is not a directory!")
        return []

    # 使用os.listdir来获取目录中的所有文件和子目录名
    files = os.listdir(directory_path)

    # 可选：仅返回文件，过滤掉子目录
    files = [file for file in files if os.path.isfile(os.path.join(directory_path, file))]

    return files

# 获取文件信息（根据id）

# 判断是否为vpk
def is_vpk_file(filename: str) -> bool:
    return bool(re.match(r".*\.vpk$", filename, re.IGNORECASE))

#下载文件并处理
@get_file.handle()
async def file_message_judge(event: Event, bot: Bot):
    file_info = event.get_message()[0].data
    message_type=event.get_message()[0].type
    # logger.info(message_type)
    # logger.info(event.get_message()[0].data)
    # logger.info(file_info["file"])
    if message_type == "file"  and is_vpk_file(file_info["file"]):
        message_id = event.message_id
        msg_detail = await bot.call_api("get_msg", message_id=message_id)
        logger.info(msg_detail)
        group_id=msg_detail["group_id"]
        #权限认证
        if msg_detail["user_id"] not in admin_qq and len(admin_qq)!=0:
            await get_file.finish()
        addons_list=list_files_in_directory(destination_path)
        if file_info["file"] in addons_list:
            await bot.send(event, file_info["file"]+"已存在,输入/file查看已加载vpk文件")
            await get_file.finish()
        await bot.send(event,
                       "已检测到" + file_info["file"] + "文件,开始下载,请稍等")
        try:
            url_info = await bot.call_api("get_group_file_url", file_id=file_info["file_id"], group_id=group_id)
            logger.info("文件url:" + url_info["url"])
        except:
            logger.info("get url error")
            await bot.send(event,"获取" + file_info["file"] + "url失败")
            await get_file.finish()
        await download_file(url_info["url"],event,bot,filename=file_info["file"])


#查询vpk
find_vpk = on_command("file", aliases={"File"})
vpk_path = "left4dead2/addons"
origin_path = r"/root/Steam/steamapps/common/Left 4 Dead 2 Dedicated Server"
def get_vpk(map_path: Path, file_: str = ".vpk") -> List[str]:
    """
    获取路径下所有vpk文件名，并存入vpk_list列表中
    """
    vpk_list: List[str] = [str(file) for file in map_path.glob(f"*{file_}")]
    return vpk_list

def mes_list(mes: str, name_list: List[str]) -> str:
    if name_list:
        for idx, name in enumerate(name_list):
            mes += f"\n{idx+1}、{name}"
    return mes

@find_vpk.handle()
async def _():
    path = destination_path
    # 确保目标文件夹存在
    if not os.path.exists(destination_path):
        await find_vpk.finish(Message(destination_path+"文件夹不存在"))
        return
    vpk_path = Path(destination_path)
    name_vpk = get_vpk(vpk_path)
    #logger.info(name_vpk)
    logger.info("获取文件列表成功")
    mes = "服务器有以下vpk文件"
    for i in range(len(name_vpk)):
        temp = name_vpk[i]
        name_vpk[i] = temp[len(path) + 1:]
    name_vpk=sorted(name_vpk)
    #logger.info(name_vpk)
    msg = mes_list("", name_vpk)
    #msg=sorted(msg)
    #logger.info(msg)
    await find_vpk.finish(Message(mes+msg))

#删除vpk
delete = on_command("delete",block=False)
@delete.handle()
async def delete_file(bot: Bot, event: Event, args: Message = CommandArg()):
    if not os.path.exists(destination_path):
        await find_vpk.finish(Message(destination_path+"文件夹不存在"))
        return
    message_id = event.message_id
    msg_detail = await bot.call_api("get_msg", message_id=message_id)
    if msg_detail["user_id"] not in admin_qq and lem(admin_qq)!=0:
        await delete.finish()
    files=list_files_in_directory(destination_path)
    filename=args.extract_plain_text()
    if filename in files:
        filepath=destination_path+"/"+filename
        os.remove(filepath)
        await bot.send(event,filename+"删除成功")
    else:
        await bot.send(event, "无"+ filename + "文件，删除失败")

#修改文件名
rename = on_command("rename",block=False)
@rename.handle()
async def rename_file(bot: Bot, event: Event, args: Message = CommandArg()):
    if not os.path.exists(destination_path):
        await find_vpk.finish(Message(destination_path+"文件夹不存在"))
        return
    message_id = event.message_id
    msg_detail = await bot.call_api("get_msg", message_id=message_id)
    if msg_detail["user_id"] not in admin_qq:
        await rename.finish()
    files=list_files_in_directory(destination_path)
    filenames=args.extract_plain_text().split(",")
    logger.info(filenames)
    if len(filenames)<2:
        await bot.send(event, "请输入两个文件名")
        await rename.finish()
    old_file_name = filenames[0]
    new_file_name = filenames[1]
    if new_file_name in files:
        await bot.send(event, f"错误：文件'{new_file_name}'已存在")
        await rename.finish()
    # 修改文件名
    try:
        os.rename(destination_path+'/'+old_file_name, destination_path+'/'+new_file_name)
        await bot.send(event,f"文件名已从'{old_file_name}'成功修改为'{new_file_name}'")
    except FileNotFoundError:
        await bot.send(event,f"错误：文件'{old_file_name}'不存在")
    except Exception as e:
        await bot.send(event,f"修改文件名时发生错误: {e}")





















