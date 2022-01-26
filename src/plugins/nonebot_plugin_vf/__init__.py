import traceback
from .api import *
from nonebot import on_command, on_message
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent, GroupMessageEvent, GROUP_OWNER, GROUP_ADMIN, PRIVATE
from nonebot.exception import FinishedException
from nonebot.permission import SUPERUSER

vf = on_command("vf", aliases={"虚拟朋友"}, block=True, permission=GROUP_OWNER | GROUP_ADMIN | PRIVATE | SUPERUSER)
vfs = on_command("vfs", aliases={"虚拟管理"}, block=True, permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN | SUPERUSER)
vf_trans = on_message(block=False)
database_init()
timer_restart()


@vf.handle()
async def vf_handle(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]):
    try:
        args = event.raw_message.strip().split()
        if type(event) is GroupMessageEvent:
            target_id = event.group_id
            target_type = "group"
        else:
            target_id = event.user_id
            target_type = "user"
        if args[1] in ["connect", "连接"]:
            r = await connect(target_type=target_type, target_id=target_id, vf_name=args[2])
            if r[2] is not None:
                await bot.send_private_msg(user_id=r[2], message=random.choice(start_message))
            await vf.finish(r[1])
        elif args[1] in ["disconnect", "断开"]:
            r = await disconnect(target_type=target_type, target_id=target_id)
            if r[2] is not None:
                await bot.send_private_msg(user_id=r[2], message=random.choice(end_message))
            await vf.finish(r[1])
        elif args[1] in ["list", "列出"]:
            # 还没写
            r = await list_user()
            await vf.finish(r[1])
        elif args[1] in ["help", "帮助"]:
            reply = "虚拟朋友插件帮助文档\n" \
                    "普通用户命令:\n" \
                    "- 虚拟朋友 连接 虚拟朋友名称\n" \
                    "- 虚拟朋友 断开\n" \
                    "- 虚拟朋友 列出\n" \
                    "超级用户命令:\n" \
                    "- 虚拟管理 转接 虚拟朋友名称 目标类型 目标id\n" \
                    "- 虚拟管理 释放 虚拟朋友名称\n" \
                    "- 虚拟管理 释放 所有\n" \
                    "- 虚拟管理 列出\n" \
                    "# 说明:\n" \
                    "目标类型参数:群聊, 用户"
        else:
            await vf.finish("未知的参数:%s" % args[1])
    except BaseException as error:
        if type(error) is not FinishedException:
            traceback.print_exc()
            await vf.send("出错了哦, 请使用vf help查看使用方法")
            await vf.finish(error.__repr__())


@vfs.handle()
async def vfs_handle(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]):
    try:
        args = event.raw_message.strip().split()
        if type(event) is GroupMessageEvent:
            target_id = event.group_id
            target_type = "group"
        else:
            target_id = event.user_id
            target_type = "user"

        if args[1] in ["transfer", "转接"]:
            vf_name = args[2]
            target_type = args[3]
            if target_type in ["group", "群聊", "群"]:
                target_type = "group"
            else:
                target_type = "user"
            target_id = int(args[4])
            r = await transfer(target_type, target_id, vf_name)
            await vfs.finish(r[1])
        elif args[1] in ["release", "释放"]:
            vf_name = args[2]
            if vf_name in ["all", "所有"]:
                r = True, "已将所有虚拟朋友释放"
                for vf_n in get_vf_data():
                    await release(vf_n)
            else:
                r = await release(vf_name)
            await vfs.finish(r[1])
        elif args[1] in ["list", "列出"]:
            r = await list_superuser()
            await vfs.finish(r[1])
        else:
            await vf.finish("未知的参数:%s" % args[1])
    except BaseException as error:
        if type(error) is not FinishedException:
            traceback.print_exc()
            await vf.send("出错了哦, 请使用vf help查看使用方法")
            await vf.finish(error.__repr__())


@vf_trans.handle()
async def vf_handle(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]):
    try:
        if type(event) is PrivateMessageEvent:
            target_id = event.user_id
            target_type = "user"
        else:
            target_id = event.group_id
            target_type = "group"

        if target_type == "user" and target_id in get_online_vf_ids():
            recipient = get_online_vf_ids()[target_id]
            recipient_type = recipient[0]
            recipient_id = recipient[1]
            if recipient_type is not None and recipient_id is not None:
                if recipient_type == "group":
                    await bot.send_group_msg(group_id=recipient_id, message=event.message)
                elif recipient_type == "user":
                    await bot.send_private_msg(user_id=recipient_id, message=event.message)
            else:
                pass
            # 是机器人发给用户和群聊
        if get_using_vf_id(target_type, target_id) is not None:
            vf_id = get_using_vf_id(target_type, target_id)
            await bot.send_private_msg(user_id=vf_id, message=event.message)

    except BaseException as error:
        if type(error) is not FinishedException:
            traceback.print_exc()
            await vf.send("消息呈递中出现错误")
            await vf.finish(error.__repr__())
