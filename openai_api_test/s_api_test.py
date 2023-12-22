import openai

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
        max_tokens=150,
        stop=["用户:", "GPT-3:"]  # 添加停止序列，有助于模型更好地区分每个回合
    )
    return response

def main():
    api_key = "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"  # 替换为你的OpenAI API密钥
    initial_prompt = ("我的屋子里有一些智能设备：灯、空调；我希望你扮演一个能调度整个屋子的智能机器人，"
                      "我向你发送自然语言，你理解后通来向我的家居发送一个控制指令，这个指令的格式是：\n"
                      "'{\"object\":\"A\",\"status\":\"B\"}'"
                      "其中A只能是lights或者air-conditioning或者other；\n"
                      "其中B只能是on或者off或者other；\n"
                      "object和status这两个参数的值完全依据接下来我向你说的话来确定。\n")

    print("输入'exit'或'quit'结束对话。")

    while True:
        user_input = input("请输入你的问题: ").strip()  # 获取用户输入
        if user_input.lower() in ["exit", "quit"]:
            break  # 如果用户输入exit或quit，结束对话

        if not user_input or user_input.lower() in ['hello', 'hi']:
            print("请输入一些具体的问题。")
            continue

        # 设置每次请求的对话历史为初始提示加上当前的用户输入
        conversation = initial_prompt + f"用户: {user_input}\n"
        
        # 发送请求并获取响应
        response = query_openai(conversation, api_key)
        
        # 获取并打印响应
        ai_response = response.choices[0].text.strip()
        print(f"GPT-3: {ai_response}\n")

if __name__ == "__main__":
    main()
