"""用户提问，搜索参考资料和提问一同返回给模型，让模型总结回复"""
from xml.dom.minidom import Document

from langchain_core.output_parsers import StrOutputParser

from model.factory import chat_model
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate


def print_prompt(prompt_text):
    print(prompt_text.to_string())
    return prompt_text
class RagSummaryService(object):
    def __init__(self):
        self.vector_store=VectorStoreService ()
        self.retriever=self.vector_store.get_retriever()
        self.prompt_text=load_rag_prompts()
        self.prompt_template=PromptTemplate.from_template(self.prompt_text)
        self.model=chat_model
        self.chain= self.__init__chain()


    def __init__chain(self):
        chain =self.prompt_template | print_prompt | self.model | StrOutputParser ()
        return chain



    def retrieve_docs(self,query:str)->list[Document]:
        """
        根据问题，返回参考资料
        :param query: 问题
        :return: 参考资料
        """
        return self.retriever.invoke(query)

    def rag_summarize(self,query:str)->str:
        context_docs=self.retrieve_docs(query)
        context=""
        conter=0
        for doc in context_docs:
            conter+=1
            context+=f"【参考资料{conter}】: 参考资料：{doc.page_content}| 参考元数据：{doc.metadata}\n"

        return self.chain.invoke(
            {
                "input": query,
                "context":context
            }
        )

if __name__ == '__main__':
    rag_service=RagSummaryService()
    print(rag_service.rag_summarize("小户型适合哪些扫地机器人"))