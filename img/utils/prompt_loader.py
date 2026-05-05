from utils.config_handler import prompts_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from utils.history_handler import search_related_history

"""提示词加载工具"""


def load_system_prompts(query: str = "") -> str:
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts] 在yaml配置文件中没有main_prompt_path配置项: {e}")
        raise e

    try:
        base_prompt = open(system_prompt_path, 'r', encoding="utf-8").read()
        if query:
            history_text = search_related_history(query)
            if history_text:
                return base_prompt + "\n\n" + history_text
        return base_prompt
    except Exception as e:
        logger.error(f"[load_system_prompts] 读取系统提示语文件出错: {str(e)}")
        raise e


def load_rag_prompts() -> str:
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summary_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts] 在yaml配置文件中没有rag_summary_prompt_path配置项: {e}")
        raise e

    try:
        return open(rag_prompt_path, 'r', encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts] 读取rag总结提示词文件出错: {str(e)}")
        raise e


def load_report_prompts(query: str = "") -> str:
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts] 在yaml配置文件中没有report_prompt_path配置项: {e}")
        raise e

    try:
        base_prompt = open(report_prompt_path, 'r', encoding="utf-8").read()
        if query:
            history_text = search_related_history(query)
            if history_text:
                return base_prompt + "\n\n" + history_text
        return base_prompt
    except Exception as e:
        logger.error(f"[load_report_prompts] 读取报告生成提示语文件出错: {str(e)}")
        raise e


if __name__ == '__main__':
    print(load_report_prompts())
