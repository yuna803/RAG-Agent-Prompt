import logging
import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from model.factory import embed_model
from utils.config_handler import chroma_conf
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.path_tool import get_abs_path



class VectorStoreService:
    def __init__(self):

        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"],
        )

        self.spliter =RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs={"k": chroma_conf["k"]}
        )

    def load_documents(self):
        """
        将读取的文件转为向量存入向量数据库
        用md5去重
        """
        def check_md5_hex(md5_for_check: str):
            # 检查文件
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w",encoding="utf-8").close()
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r",encoding="utf-8") as f:
                md5_hex_list = f.readlines()
                for md5_hex in md5_hex_list:
                    md5_hex = md5_hex.strip()
                    if md5_hex.strip() == md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_save: str):
            # 保存文件
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a",encoding="utf-8") as f:
                f.write(md5_for_save + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader(read_path)

            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            return []

        allowed_files_paths:list[ str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for file_path in allowed_files_paths:
            file_md5_hex = get_file_md5_hex(file_path)
            if check_md5_hex(file_md5_hex):
                logging.info(f"文件{file_path}已存在，跳过")
                continue
            try:
                documents : list[Document]=get_file_documents(file_path)

                if not documents:
                    logging.warning(f"文件{file_path}为空，跳过")
                    continue
                split_document: list[Document] =self.spliter.split_documents(documents)
                if not split_document:
                    logging.warning(f"文件{file_path}分片后为空，跳过")
                    continue
                self.vector_store.add_documents(split_document)
                #记录文件防止重复打印
                save_md5_hex(file_md5_hex)
                logging.info(f"文件{file_path}已添加到向量数据库")
            except Exception as e:
                #exc_info= True会记录详细的报错堆栈，如果False，则只记录错误信息
                logging.error(f"文件{file_path}添加到向量数据库出错: {str(e)}",exc_info= True)

if __name__ == '__main__':
    vs=VectorStoreService()
    vs.load_documents()
    retriever=vs.get_retriever()
    res=retriever.invoke("迷路")
    for i in res:
        print(i.page_content)