import yaml
from utils.path_tool import get_abs_path

"""     加载yaml配置文件工具    """

def load_rag_config(config_path:str=get_abs_path("config/rag_config.yaml"),encoding="utf-8"):
    """
    加载配置文件config_path
    :param : 配置文件路径
    :return: 配置文件内容
    """
    with open(config_path , 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_chroma_config(config_path:str=get_abs_path("config/chroma_config.yaml"),encoding="utf-8"):
    """
    加载配置文件
    :param config_path: 配置文件路径
    :return: 配置文件内容
    """
    with open( config_path , 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_prompts_config(config_path:str=get_abs_path("config/prompts_config.yaml"),encoding="utf-8"):
    """
    加载配置文件
    :param config_path: 配置文件路径
    :return: 配置文件内容
    """
    with open(config_path , 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_agent_config(config_path:str=get_abs_path("config/agent_config.yaml"),encoding="utf-8"):
    """
    加载配置文件
    :param config_path: 配置文件路径
    :return: 配置文件内容
    """
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

rag_conf=load_rag_config()
chroma_conf=load_chroma_config()
prompts_conf=load_prompts_config()
agent_conf=load_agent_config()

if __name__ == '__main__':
    print(agent_conf["chat_model_name"])