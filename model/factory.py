from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from utils.config_handler import rag_conf


class BaseModelFactory(ABC):
    """
    模型工厂抽象类
    """
    @abstractmethod
    def generator(self)->Optional[Embeddings | BaseChatModel]:
        """
        模型生成抽象方法
        :return:
        """
        pass


class ChatModelFactory(BaseModelFactory):
    """
    聊天模型工厂类
    """
    def generator(self)->Optional[Embeddings | BaseChatModel]:
        """
        模型生成方法
        :return:
        """
        return ChatTongyi(
            model_name=rag_conf["chat_model_name"]
        )

class EmbeddingModelFactory(BaseModelFactory):
    """
    嵌入模型工厂类
    """
    def generator(self)->Optional[Embeddings | BaseChatModel]:
        """
        模型生成方法
        :return:
        """
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"]
        )

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingModelFactory().generator()
