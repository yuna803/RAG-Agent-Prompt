import os,hashlib
from xml.dom.minidom import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from utils.logger_handler import logger

"""上传文件的工具"""
def get_file_md5_hex(file_path: str):
    """
    获取文件的md5值
    :param file_path: 文件路径
    :return: md5值
    """
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return

    if not os.path.isfile(file_path):
        logger.error(f"不是文件: {file_path}")
        return
    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(file_path, "rb") as f:
            while chunk :=f.read(chunk_size):
                md5_obj.update(chunk)
            return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"计算文件md5值失败: {file_path}")
        return  None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """
    列出指定目录下的所有文件，并筛选出指定类型的文件
    :return:
    """
    files=[]
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type] {path}不是有效地址")
        return allowed_types

    for file in os.listdir(path):
        if file.endswith(allowed_types):
            files.append(os.path.join(path,file))
    return tuple(files)

def pdf_loader(path: str,password=None)->list[Document]:
    """
    加载pdf文件
    :return:
    """
    return PyPDFLoader(path, password).load()


def txt_loader(path: str)->list[Document]:
    """
    加载txt文件
    :return:
    """
    return TextLoader(path,encoding="utf-8").load()