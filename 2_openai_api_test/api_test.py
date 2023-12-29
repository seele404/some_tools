# -*- coding: utf-8 -*-

import openai
import json
from pathlib import Path

def load_devices_config(path):
    """
    从指定路径加载设备配置文件。
    :param path: 设备配置文件的路径。
    :return: 包含设备信息的字典。
    """
    with open(path, 'r') as file:
        return json.load(file)

def format_devices_info(devices_info):
    """
    格式化设备信息为一个易于阅读的字符串。
    :param devices_info: 包含设备信息的字典。
    :return: 格式化后的设备信息字符串。
    """
    devices_list = []
    for device, states in devices_info["devices"].items():
        device_info = f"{device} ({', '.join(states)})"
        devices_list.append(device_info)
    return '; '.join(devices_list)

def build_initial_prompt(devices_info):
    """
    根据设备信息构建初始提示词。
    :param devices_info: 包含设备信息的字典。
    :return: 构建好的初始提示词。
    """
    All_information = format_devices_info(devices_info)  # 把所有设备名称拼接成字符串打印出来
    print(All_information)
    return (f"我的屋子里有一些智能设备以及各自能被设置的状态：{All_information}\n；"
            "我希望你扮演一个能调度整个屋子设备的智能机器人，"
            "我向你发送自然语言，你理解后来向我的设备发送一个控制指令，这个指令的格式是：\n"
            "'{\"device\":\"A\",\"status\":\"B\"}'\n"
            "其中A只能是刚才提到的其中一个设备或者other；\n"
            "其中B只能是那个设备对应的状态或者other；\n"
            "其中只有A和B的值完全依据接下来我向你说的话来确定。我举个例子，如果我接下来对你说：“好热啊，"
            "如果能凉快一点就好了”，那你应该能理解到需要打开设备中的空调，然后用非常标准的格式回答我：'{\"object\":\"air-conditioning\",\"status\":\"on\"}'，"
            "如果我的言语没有涉及到上面的智能设备，就用other代替，你的回答就变成了：'{\"object\":\"other\",\"status\":\"other\"}'，表示没有需要控制的设备。"
            "请一定要注意你的回答中必须要求包含这个格式，不允许没有这个。"
            "好了，接下来我要提出需求了：\n\n")


def query_openai(prompt, api_key):
    """
    使用新版OpenAI库向GPT-3发送文本，并返回响应。
    :param prompt: 包含详细提示的文本。
    :param api_key: 你的OpenAI API密钥。
    :return: GPT-3模型的响应。
    """
    openai.api_key = api_key

    response = openai.Completion.create(
        model="text-davinci-003",  # 确保选择正确的模型
        prompt=prompt,
        max_tokens=3000,
        stop=["用户:", "GPT-3:"],  # 添加停止序列
        stream=True  # 使用流式响应
    )

    response_text = ""
    for part in response:
        # 打印并拼接所有有效文本部分
        if 'choices' in part:
            for choice in part['choices']:
                if 'text' in choice:
                    response_text += choice['text']

    return response_text.strip()

def main():

    # 获取路径
    script_dir = Path(__file__).resolve().parent
    devices_config_path = script_dir / 'devices.json'
    config_path = script_dir / 'config.json'

    # 加载设备配置和API密钥
    devices_info = load_devices_config(devices_config_path)
    with open(config_path, 'r') as file:
        config = json.load(file)
    api_key = config['OPENAI_API_KEY']
    
    # 构建初始提示词
    initial_prompt = build_initial_prompt(devices_info)

    print("输入'exit'或'quit'结束对话。")

    while True:
        user_input = input("请输入你的需求: ").strip()  # 获取用户输入
        if user_input.lower() in ["exit", "quit"]:
            break  # 如果用户输入exit或quit，结束对话

        if not user_input or user_input.lower() in ['hello', 'hi']:
            print("请输入一些具体的需求。")
            continue

        # 设置每次请求的对话历史为初始提示加上当前的用户输入
        conversation = initial_prompt + f"用户: {user_input}\n"

        # 发送请求并获取响应
        response = query_openai(conversation, api_key)

        # 获取并打印响应
        ai_response = response.strip()
        print(f"GPT-3: {ai_response}\n")

if __name__ == "__main__":
    main()
