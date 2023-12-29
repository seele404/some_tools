# -*- coding: utf-8 -*-

import openai
import json
from pathlib import Path


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
        max_tokens=1000,
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

    # 获取当前脚本文件的绝对路径
    script_dir = Path(__file__).resolve().parent
    config_path = script_dir / 'config.json'

    # 使用构建的绝对路径打开config.json
    with open(config_path, 'r') as file:
        config = json.load(file)
    api_key = config['OPENAI_API_KEY']
    initial_prompt = ("我的屋子里有一些智能设备：灯、空调；我希望你扮演一个能调度整个屋子的智能机器人，"
                  "我向你发送自然语言，你理解后来向我的家居发送一个控制指令，这个指令的格式是：\n"
                  "'{\"object\":\"A\",\"status\":\"B\"}'\n"
                  "其中A只能是lights或者air-conditioning或者other；\n"
                  "其中B只能是on或者off或者other；\n"
                  "object和status这两个参数的值完全依据接下来我向你说的话来确定，我举个例子，如果我接下来对你说：“好热啊，"
                  "如果能凉快一点就好了”，那你应该能理解到需要打开空调，用非常标准的格式回答我：'{\"object\":\"air-conditioning\",\"status\":\"on\"}'，"
                  "如果我的言语没有涉及到上面的智能设备，就全部用other代替，你的回答就变成了：'{\"object\":\"other\",\"status\":\"other\"}'，"
                  "请一定要注意你的回答中必须要求包含这个格式，不允许没有这个。"
                  "好了，接下来我要提出需求了：\n\n")

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
