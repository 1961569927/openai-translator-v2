from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# 你的 OpenAI API Key
import os
os.environ["OPENAI_API_KEY"] = "52404798a6aa4d95a3b150f5a93927bb.oInd94SYpq2niOkr"

# 示例文本
text = """
在遥远的东方，有一个名叫李云的年轻剑客。他身穿青衫，目光如炬，行侠仗义。李云自幼失去父母，由师父抚养长大，性格坚毅果敢。一天，他在山林中遇见了神秘的少女苏瑶。苏瑶聪慧机敏，身世成谜，总是带着一丝淡淡的忧伤。
"""
def generate_role():
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
if __name__ == "__main__":
    result = generate_role()
    print(result["info"])
    print(result["name"])
