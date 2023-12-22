import openai

def query_openai(prompt, api_key):
    """
    使用新版OpenAI库向GPT-3发送文本，并返回响应。
    :param prompt: 包含整个对话历史和详细提示的文本。
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
    # 设置详细的提示词，指导模型如何响应

    initial_prompt = (
    "我的屋子里有一些智能设备：灯、空调；我希望你扮演一个能调度整个屋子的智能机器人，我向你发送自然语言，你理解后通来向我的家居发送一个控制指令，这个指令的格式是：\n"
    "'{\"object\":\"A\",\"status\":\"B\"}'"
    "其中A只能是lights或者air-conditioning或者other；\n"
    "其中B只能是on或者off或者other；\n"
    "object和status这两个参数的值完全依据接下来我向你说的话来确定，我举个例子，"
    "如果我接下来对你说：“好热啊，如果能凉快一点就好了”，那你应该能理解到需要打开空调，用非常标准的格式回答我："
    "'{\"object\":\"air-conditioning\",\"status\":\"on\"}'，如果我的言语没有涉及到上面的智能设备，"
    "就全部用other代替，你的回答就变成了：'{\"object\":\"other\",\"status\":\"other\"}'，"
    "请一定要注意你的回答格式必须要求包含这个格式。\n")

    # initial_prompt = ("你是一个友好而知识渊博的助手，专门回答各种问题。"
    #                   "请以清晰、简洁、准确的方式提供帮助。\n")
    conversation_history = initial_prompt

    print("输入'exit'或'quit'结束对话。")

    while True:
        user_input = input("请输入你的问题: ").strip()  # 获取用户输入
        if user_input.lower() in ["exit", "quit"]:
            break  # 如果用户输入exit或quit，结束对话

        # 过滤无效或重复的输入
        if not user_input or user_input.lower() in ['hello', 'hi']:
            print("请输入一些具体的问题。")
            continue
        
        # 更新对话历史
        conversation_history += f"用户: {user_input}\n"
        
        # 发送请求并获取响应
        response = query_openai(conversation_history, api_key)
        
        # 获取并打印响应
        ai_response = response.choices[0].text.strip()
        print(f"GPT-3: {ai_response}\n")

        # 更新对话历史
        conversation_history += f"GPT-3: {ai_response}\n"

if __name__ == "__main__":
    main()
