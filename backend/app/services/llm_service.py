"""
LLM 服务模块

封装与大语言模型的交互，用于告警根因分析。
"""
import json
import logging
from typing import Dict, Any, Optional

from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas import AnalysisResult

logger = logging.getLogger(__name__)


# 根因分析提示词模板
PROMPT_TEMPLATE = """你是一个经验丰富的 SRE 专家。请分析以下告警并给出根因分析和解决方案建议。

【告警信息】
名称: {alert_name}
严重程度: {severity}
摘要: {summary}
描述: {description}
标签: {labels}
开始时间: {starts_at}

【相关指标数据】
{metrics_summary}

请以 JSON 格式返回结果，格式如下：
{{
  "root_cause": "详细的根因分析，说明可能是什么导致了这个告警",
  "possible_solutions": [
    "建议的解决方案 1",
    "建议的解决方案 2"
  ],
  "reasoning": "你的推理过程，说明是如何得出这个结论的",
  "confidence_score": 0.8
}}

要求：
- confidence_score 是 0-1 之间的数字，表示你对分析结果的置信度
- root_cause 要具体，不要太笼统
- possible_solutions 要可操作
"""


class LLMService:
    """
    LLM 服务类

    封装与大语言模型的交互，提供根因分析功能。
    """

    def __init__(self):
        """初始化 LLM 服务"""
        self._client: Optional[AsyncOpenAI] = None

    @property
    def client(self) -> AsyncOpenAI:
        """
        获取 AsyncOpenAI 客户端（懒加载）

        Returns:
            AsyncOpenAI 客户端实例
        """
        if self._client is None:
            logger.info("=" * 60)
            logger.info("Initializing Async OpenAI client...")
            logger.info(f"  Model: {settings.openai_model}")
            logger.info(f"  Base URL: {settings.openai_base_url}")
            logger.info(f"  API Key: {'set' if settings.openai_api_key else 'not set'}")
            logger.info("=" * 60)

            self._client = AsyncOpenAI(
                api_key=settings.openai_api_key,
                base_url=settings.openai_base_url,
            )
        return self._client

    def _format_metrics_summary(self, metrics_data: Dict[str, Any]) -> str:
        """
        格式化指标数据摘要

        Args:
            metrics_data: 指标数据

        Returns:
            格式化后的指标摘要字符串
        """
        if not metrics_data or not metrics_data.get("metrics"):
            return "暂无相关指标数据"

        summary_lines = []
        for name, data in metrics_data["metrics"].items():
            if data:
                summary_lines.append(f"- {name}: 有 {len(data)} 个时间序列")
                for series in data[:3]:
                    metric_labels = series.get("metric", {})
                    values = series.get("values", [])
                    if values:
                        last_val = values[-1][1]
                        summary_lines.append(f"  * {metric_labels}: {last_val}")

        return "\n".join(summary_lines) if summary_lines else "暂无相关指标数据"

    async def analyze_root_cause(
        self,
        alert_data: Dict[str, Any],
        metrics_data: Dict[str, Any],
    ) -> AnalysisResult:
        """
        分析告警根因

        Args:
            alert_data: 告警数据
            metrics_data: 指标数据

        Returns:
            分析结果

        Raises:
            Exception: 当 LLM 调用失败时
        """
        metrics_summary = self._format_metrics_summary(metrics_data)

        prompt = PROMPT_TEMPLATE.format(
            alert_name=alert_data.get("alert_name", ""),
            severity=alert_data.get("severity", ""),
            summary=alert_data.get("summary", ""),
            description=alert_data.get("description", ""),
            labels=json.dumps(alert_data.get("labels", {}), ensure_ascii=False),
            starts_at=alert_data.get("starts_at", ""),
            metrics_summary=metrics_summary,
        )

        logger.info(f"Invoking LLM for alert: {alert_data.get('alert_name')}")

        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "你是一个专业的 SRE 专家，擅长告警根因分析。请严格按照 JSON 格式输出。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from LLM")

            content = content.strip()

            # 清理 JSON 格式
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            result_json = json.loads(content)

            return AnalysisResult(
                root_cause=result_json.get("root_cause", ""),
                possible_solutions=result_json.get("possible_solutions", []),
                reasoning=result_json.get("reasoning", ""),
                confidence_score=result_json.get("confidence_score", 0.5),
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {content}, error: {e}")
            return AnalysisResult(
                root_cause="LLM 返回结果解析失败",
                possible_solutions=["请检查 LLM 配置"],
                reasoning="JSON 解析失败",
                confidence_score=0.0,
            )
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            raise


# 全局 LLM 服务实例
llm_service = LLMService()
