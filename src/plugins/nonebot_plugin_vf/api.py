import json
import os
import random
import threading
import time

from typing import Union

plugin_path = os.path.dirname(os.path.realpath(__file__))

waiting_time = 20

start_message = ["在吗", "我来了"]
end_message = ["拜拜", "我先下线了", "我有点事先走了"]


def timer(vf_name):
    # 已修改, 计时器, 镶嵌在连接函数内部, 连接成功后自动启动
    while True:
        vf_data = get_vf_data()
        if vf_data[vf_name]["remain_time"] is not None and vf_data[vf_name]["remain_time"] >= 1:
            vf_data[vf_name]["remain_time"] -= 1
            set_vf_data(vf_data)
            time.sleep(60)
        else:
            vf_data[vf_name]["target_type"] = None
            vf_data[vf_name]["target_id"] = None
            vf_data[vf_name]["remain_time"] = None
            set_vf_data(vf_data)
            break


def get_vf_data() -> dict:
    with open(os.path.join(plugin_path, "resource/vf_data.json"), "r", encoding="utf-8-sig") as file:
        data = json.load(file)
    return data


def set_vf_data(data: dict):
    with open(os.path.join(plugin_path, "resource/vf_data.json"), "w", encoding="utf-8-sig") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return True


def get_vf_name(vf_id):
    for vf in get_vf_data().items():
        if int(vf[1]["vf_id"]) == vf_id:
            return vf[0]


def timer_restart():
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["target_id"] is not None:
            threading.Thread(target=timer, args=(vf[0],)).start()


async def connect(target_type: str, target_id: int, vf_name: str, remain_time: int = waiting_time):
    # 已修改
    result = False
    message = None
    vf_id = None
    vf_data = get_vf_data()
    if get_using_vf_id(target_type, target_id) is not None:
        message = "当前正在与%s会话, 请断开后再试" % get_vf_name(get_using_vf_id(target_type, target_id))
    elif vf_name in vf_data:
        # 虚拟朋友存在
        if vf_data[vf_name]["target_id"] is None:
            # 虚拟朋友未占用
            vf_data[vf_name]["target_id"] = target_id
            vf_data[vf_name]["target_type"] = target_type
            vf_data[vf_name]["remain_time"] = remain_time
            vf_id = int(vf_data[vf_name]["vf_id"])
            set_vf_data(vf_data)
            result = True
            message = "已连接到%s, 若%s分钟你没有发送新的消息, 系统将自动断开" % (vf_name, remain_time)
            threading.Thread(target=timer, args=(vf_name,)).start()
        else:
            if vf_data[vf_name]["target_id"] == target_id and vf_data[vf_name]["target_type"] == target_type:
                message = "当前已连接到%s, 无需再次连接" % vf_name
            else:
                message = "%s正在进行其他会话, 请稍等或换一个虚拟朋友吧" % vf_name
    else:
        message = "%s不存在, 请换一个虚拟朋友试试吧" % vf_name
    return result, message, vf_id


async def disconnect(target_type: str, target_id: int):
    # 已修改
    result = False
    message = None
    vf_id = None
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["target_id"] == target_id and vf[1]["target_type"] == target_type:
            result = True
            vf_name = vf[0]
            vf_data[vf[0]]["target_id"] = None
            vf_data[vf[0]]["target_type"] = None
            vf_data[vf[0]]["remain_time"] = None
            vf_id = int(vf_data[vf_name]["vf_id"])
            set_vf_data(vf_data)
            message = "已从%s断开连接" % vf[0]
            break
    else:
        vf_name = None
        message = "当前未连接到任何虚拟朋友"
    return result, message, vf_id


async def transfer(target_type: str, target_id: int, vf_name: str, remain_time: int = waiting_time):
    # 已修改
    result = False
    message = None
    vf_data = get_vf_data()
    if vf_name in vf_data:
        # 虚拟朋友存在
        if vf_data[vf_name]["target_id"] is None:
            # 虚拟朋友未占用
            vf_data[vf_name]["target_type"] = target_type
            vf_data[vf_name]["target_id"] = target_id
            vf_data[vf_name]["remain_time"] = remain_time
            set_vf_data(vf_data)
            result = True
            message = "已将%s连接到%s:%s, 若%s分钟目标用户没有发送新的消息, 系统将自动断开" % (vf_name, target_type, target_id, remain_time)
            thread = threading.Thread(target=timer, args=(vf_name,))
            thread.start()
        else:
            if vf_data[vf_name]["target_id"] == target_id and vf_data[vf_name]["target_type"] == target_type:
                message = "%s连接到%s, 无需再次连接" % (target_id, vf_name)
            else:
                message = "%s正在进行其他会话, 请稍等或换一个虚拟朋友吧" % vf_name
    else:
        message = "%s不存在, 请换一个虚拟朋友试试吧" % vf_name
    return result, message


async def release(vf_name):
    # 已修改
    """
    :param vf_name:
    :return: result, msg1, msg2, target_type, target_id
    """
    result = False
    message = None
    vf_data = get_vf_data()
    if vf_name in ["all", "所有"]:
        for vf in vf_data.items():
            if vf[1]["target_id"] is not None:
                vf_data[vf[0]]["target_id"] = None
                vf_data[vf[0]]["target_type"] = None
                vf_data[vf[0]]["remain_time"] = None
        set_vf_data(vf_data)
        return True, "已将全部虚拟朋友断开", None
    else:
        for vf in vf_data.items():
            if vf[0] == vf_name:
                result = True
                target_type = vf_data[vf[0]]["target_type"]
                target_id = vf_data[vf[0]]["target_id"]
                vf_id = vf[1]["vf_id"]
                vf_data[vf[0]]["target_type"] = None
                vf_data[vf[0]]["target_id"] = None
                vf_data[vf[0]]["remain_time"] = None
                set_vf_data(vf_data)
                message = "已将%s从%s:%s断开" % (vf[0], target_type, target_id)
                message2 = "管理员已将你和%s强制断开" % vf_name
                break
        else:
            message = "%s不存在" % vf_name
            message2 = None
            target_type = None
            target_id = None
            vf_id = None

        return result, message, message2, target_type, target_id, vf_id


async def list_superuser():
    message = "虚拟朋友情况-管理员:\n"
    vf_data = get_vf_data()
    target_type = None
    target_id = None
    for vf in vf_data.items():
        if vf[1]["target_id"] is None:
            state = "未占用"
            remain_time = 0
            user = "无"
            target_type = None
            target_id = None
        else:
            state = "已占用"
            remain_time = vf[1]["remain_time"]
            target_type = vf[1]["target_type"]
            target_id = vf[1]["target_id"]
        message += "\n- %s:\n" \
                   "   - 朋友id: %s\n" \
                   "   - 占用情况: %s\n" \
                   "   - 占用对象: %s:%s\n" \
                   "   - 剩余时间: %s 分钟\n" % (vf[0], vf[1]["vf_id"], state, target_type, target_id, remain_time)

    return True, message[:-1]


async def list_user():
    message = "虚拟朋友情况:\n"
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["target_id"] is None:
            state = "未占用"
            remain_time = 0
        else:
            state = "已占用"
            remain_time = vf[1]["remain_time"]
        message += "\n- %s:\n" \
                   "   - 朋友id: %s\n" \
                   "   - 占用情况: %s\n" \
                   "   - 剩余时间: %s 分钟\n" % (vf[0], vf[1]["vf_id"], state, remain_time)

    return True, message[:-1]


def get_online_vf_ids() -> dict:
    # 无需修改
    """
    获取在线的虚拟朋友id列表, 用于消息转发判定
    """
    vf_ids = {}
    vf_data = get_vf_data()
    for vf in vf_data.items():
        if vf[1]["target_id"] is not None:
            vf_ids[vf[1]["vf_id"]] = (vf[1]["target_type"], vf[1]["target_id"])
    return vf_ids


def get_using_vf_id(target_type: str, target_id: int) -> Union[int, None]:
    # 无需修改
    """
    获取用户或群聊使用的机器人, 若为None则未使用机器人
    """
    for vf in get_online_vf_ids().items():
        if vf[1][0] == target_type and vf[1][1] == target_id:
            return vf[0]
    else:
        return None


def database_init():
    if not os.path.exists(os.path.join(plugin_path, "resource")):
        os.mkdir(os.path.join(plugin_path, "resource"))
    if not os.path.exists(os.path.join(plugin_path, "resource/vf_data.json")):
        with open(os.path.join(plugin_path, "resource/vf_data.json"), "w", encoding="utf-8-sig") as file:
            file.write('''{
    "虚拟男友": {
        "vf_id": 2854201761,
        "target_type": null,
        "target_id": null,
        "remain_time": null,
        "force": true
    },
    "虚拟女友": {
        "vf_id": 2854201860,
        "target_type": null,
        "target_id": null,
        "remain_time": null,
        "force": true
    },
    "小冰": {
        "vf_id": 2854196306,
        "target_type": null,
        "target_id": null,
        "remain_time": null,
        "force": false
    },
    "babyQ": {
        "vf_id": 66600000,
        "target_type": null,
        "target_id": null,
        "remain_time": null,
        "force": false
    },
    "创造恋人": {
        "vf_id": 2854205672,
        "target_type": null,
        "target_id": null,
        "remain_time": null,
        "force": false
    }
}''')
