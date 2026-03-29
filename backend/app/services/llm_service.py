import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.models.schemas import AnalysisResult

logger = logging.getLogger(__name__)


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
    def __init__(self):
        self._llm: Optional[ChatOpenAI] = None

    @property
    def llm(self) -> ChatOpenAI:
        if self._llm is None:
            if settings.llm_provider == "openai":
                self._llm = ChatOpenAI(
                    model=settings.openai_model,
                    api_key=settings.openai_api_key,
                    base_url=settings.openai_base_url,
                    temperature=0.3,
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
        return self._llm

    def _format_metrics_summary(self, metrics_data: Dict[str, Any]) -> str:
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

    def analyze_root_cause(
        self,
        alert_data: Dict[str, Any],
        metrics_data: Dict[str, Any],
    ) -> AnalysisResult:
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

        messages = [
            ("system", "你是一个专业的 SRE 专家，擅长告警根因分析。请严格按照 JSON 格式输出。"),
            ("user", prompt),
        ]

        try:
            response = self.llm.invoke(messages)
            content = response.content.strip()

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


llm_service = LLMService()
