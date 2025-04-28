from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.llms import ChatGLM

from utils import LOG
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

class TranslationChain:
    def __init__(self, model_name: str = "gpt-4o-mini", verbose: bool = True):
        
        # 翻译任务指令始终由 System 角色承担
        template = (
            """You are a translation expert, proficient in various languages. \n
            Translates {source_language} to {target_language}.\n
            Translation style: {style}.\n
            Translation author: {author}.\n
            If no style is specified, use a neutral, standard style."""
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # 待翻译文本由 Human 角色输入
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        # 为了翻译结果的稳定性，将 temperature 设置为 0
        if model_name.startswith("chatglm"):
            # 使用本地 ChatGLM 模型
            endpoint_url = "https://127.0.0.1:8000"
            # 使用本地 ChatGLM 模型
            chat = ChatGLM (endpoint_url = endpoint_url,
                            max_tokens=4096,
                            temperature=0, 
                            verbose=verbose)
        else:
            chat = ChatOpenAI(model_name=model_name
                              , base_url='https://vip.apiyi.com/v1'
                              , temperature=0
                              , verbose=verbose)
        
        
        self.chain = LLMChain(llm=chat, prompt=chat_prompt_template, verbose=verbose)

    def run(self, text: str, source_language: str, target_language: str, style: str = None, author: str = None) -> (str, bool):
        result = ""
        try:
            result = self.chain.run({
                "text": text,
                "source_language": source_language,
                "target_language": target_language,
                "style": style or "neutral",
                "author": author or "鲁迅"
            })
        except Exception as e:
            LOG.error(f"An error occurred during translation: {e}")
            return result, False

        return result, True