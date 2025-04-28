from api import get_characterglm_response
import json
import time
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# 你的 OpenAI API Key
import os
os.environ["OPENAI_API_KEY"] = "52404798a6aa4d95a3b150f5a93927bb.oInd94SYpq2niOkr"


def generate_role(text: str):
# 构建提示词
    prompt = ChatPromptTemplate.from_template(
       """
    你是一位角色设定专家。请根据以下文本，提取并生成所有出现角色的人设信息，包括姓名、性别、外貌、性格、背景、与其他角色的关系等。用结构化的方式输出。

    文本如下：
    {text}

    请用如下格式输出：
    - 角色名：
    - 性别：
    - 外貌：
    - 性格：
    - 背景：
    - 与其他角色的关系：
    """
    )

    # 创建 LLM 模型
    llm = ChatOpenAI(model="glm-4-plus"
                    , base_url="https://open.bigmodel.cn/api/paas/v4/"
                    , temperature=0)

    # 创建链
    chain = LLMChain(llm=llm, prompt=prompt)

    # 运行链
    result = chain.run(text)
    print("result:")
    return {
        "name": "李云",
        "info": result
    }

# 角色人设
text1 = """
在遥远的东方，有一个名叫李云的年轻剑客。他身穿青衫，目光如炬，行侠仗义。
"""
text2 = """
苏瑶聪慧机敏，身世成谜，总是带着一丝淡淡的忧伤。
"""
character1 = generate_role(text1)
character2 = generate_role(text2)

# character1 = {
#     "name": "李云",
#     "info": "男，身穿青衫，目光如炬，坚毅果敢，行侠仗义，自幼失去父母，由师父抚养长大"
# }
# character2 = {
#     "name": "苏瑶",
#     "info": "女，神秘少女，聪慧机敏，性格温婉，身世成谜，带着淡淡忧伤"
# }

# 构造meta
def build_meta(speaker, listener):
    return {
        "user_info": listener["info"],
        "bot_info": speaker["info"],
        "bot_name": speaker["name"],
        "user_name": listener["name"]
    }

# 初始对话
speaker_messages = []
listener_messages = []
dialogues = []
turns = 10
first_utterance = "你好，你是谁？"
speaker_messages.append({"role": "user", "content": first_utterance})
listener_messages.append({"role": "assistant", "content": first_utterance})
dialogues.append({"speaker": character1["name"], "text": first_utterance})

speaker_mete = build_meta(character1, character2)
listener_mete = build_meta(character2, character1)

speaker_role = "assistant"
listener_role = "user"
for i in range(turns):
    # 只取最新的若干轮对话，防止上下文过长
    response = ""

    recent_messages = speaker_messages
    # print("speaker_mete:", speaker_mete)
    # print("recent_messages:", recent_messages)
    for chunk in get_characterglm_response(recent_messages, speaker_mete):
        response += chunk
    speaker_messages.append({"role": speaker_role, "content": response.strip()})
    listener_messages.append({"role": listener_role, "content": response.strip()})
    dialogues.append({"speaker": character1["name"], "text": response.strip()})
    # print("response:", response)
    
    # print(f"第{i+1}轮1:")

    response = ""

    recent_messages = listener_messages
    # print("listener_mete:", listener_mete)
    # print("recent_messages:", recent_messages)
    for chunk in get_characterglm_response(recent_messages, listener_mete):
        response += chunk
    listener_messages.append({"role": speaker_role, "content": response.strip()})
    speaker_messages.append({"role": listener_role, "content": response.strip()})
    dialogues.append({"speaker": character2["name"], "text": response.strip()})
        
    # print("response:", response)
    # print(f"第{i+1}轮:")
    # print("recent_messages:", recent_messages)
    time.sleep(0.5)

# 保存到文件
with open("dialogues.json", "w", encoding="utf-8") as f:
    json.dump(speaker_messages, f, ensure_ascii=False, indent=2)

print("对话已保存到 dialogues.json")