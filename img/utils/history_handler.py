import json
import os
from datetime import datetime

from utils.logger_handler import logger
from utils.path_tool import get_abs_path

"""对话历史记录工具"""

HISTORY_DIR = get_abs_path("data/history")

# 延迟导入，避免循环依赖（vector_store → model.factory → utils）
_history_vector_store = None


def _get_history_vector_store():
    """单例懒加载，首次调用时初始化 HistoryVectorStore"""
    global _history_vector_store
    if _history_vector_store is None:
        from rag.vector_store import HistoryVectorStore
        _history_vector_store = HistoryVectorStore()
    return _history_vector_store


class HistoryHandler:
    """
    负责将每轮对话持久化：
      1. JSON 文件（data/history/session_*.json）— 保留完整可读的对话归档
      2. 向量库（HistoryVectorStore）— 支持按语义召回相关历史
    """

    def __init__(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = os.path.join(HISTORY_DIR, f"session_{session_id}.json")
        self._init_session_file(session_id)
        logger.info(f"[HistoryHandler] 会话历史文件已创建: {self.session_file}")

    def _init_session_file(self, session_id: str):
        data = {"session_start": session_id, "records": []}
        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_turn(self, user_query: str, ai_response: str):
        """
        保存一轮对话：
        - 追加写入 JSON 归档文件
        - 同步写入向量库供后续语义召回
        """
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ai_response = ai_response.strip()

        # 1. 写 JSON
        try:
            with open(self.session_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            data["records"].append({
                "time": time_str,
                "user": user_query,
                "ai": ai_response
            })

            with open(self.session_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"[HistoryHandler] JSON 记录已保存，共 {len(data['records'])} 轮")
        except Exception as e:
            logger.error(f"[HistoryHandler] JSON 保存失败: {str(e)}")

        # 2. 写向量库
        try:
            _get_history_vector_store().add_turn(user_query, ai_response, time_str)
        except Exception as e:
            logger.error(f"[HistoryHandler] 向量库写入失败: {str(e)}")


def search_related_history(query: str) -> str:
    """
    用当前用户提问做语义检索，返回最相关的历史记录格式化字符串。
    无结果时返回空字符串，不影响主流程。

    :param query: 当前用户的提问
    :return: 格式化的历史片段，用于注入提示词
    """
    try:
        docs = _get_history_vector_store().search(query)
        if not docs:
            return ""

        lines = ["### 相关历史对话（语义召回，仅供参考）", ""]
        for doc in docs:
            m = doc.metadata
            lines.append(f"[{m.get('time', '')}]")
            lines.append(f"用户：{m.get('user', '')}")
            lines.append(f"助手：{m.get('ai', '')}")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"[search_related_history] 检索失败: {str(e)}")
        return ""
