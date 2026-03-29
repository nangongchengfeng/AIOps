import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from prometheus_api_client import PrometheusConnect

from app.core.config import settings

logger = logging.getLogger(__name__)


class PrometheusClient:
    def __init__(self, url: Optional[str] = None):
        self.url = url or settings.prometheus_url
        self._client: Optional[PrometheusConnect] = None

    @property
    def client(self) -> PrometheusConnect:
        if self._client is None:
            self._client = PrometheusConnect(url=self.url, disable_ssl=True)
        return self._client

    async def check_connection(self) -> bool:
        try:
            self.client.all_metrics()
            return True
        except Exception as e:
            logger.warning(f"Failed to connect to Prometheus: {e}")
            return False

    def query(self, query: str, time: Optional[datetime] = None) -> Dict[str, Any]:
        try:
            params = {}
            if time:
                params["time"] = time.timestamp()
            result = self.client.custom_query(query, params=params)
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Prometheus query failed: {query}, error: {e}")
            return {"success": False, "error": str(e), "data": []}

    def query_range(
        self,
        query: str,
        start: datetime,
        end: datetime,
        step: str = "1m",
    ) -> Dict[str, Any]:
        try:
            result = self.client.custom_query_range(
                query,
                start_time=start,
                end_time=end,
                step=step,
            )
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Prometheus query_range failed: {query}, error: {e}")
            return {"success": False, "error": str(e), "data": []}

    def get_related_metrics(
        self,
        alert_labels: Dict[str, str],
        lookback_minutes: int = 30,
    ) -> Dict[str, Any]:
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=lookback_minutes)

        instance = alert_labels.get("instance", "")
        job = alert_labels.get("job", "")
        pod = alert_labels.get("pod", "")
        namespace = alert_labels.get("namespace", "")

        metrics = {}
        queries = []

        if instance:
            queries.append(
                (
                    "cpu_usage",
                    f'rate(container_cpu_usage_seconds_total{{instance="{instance}"}}[5m])',
                )
            )
            queries.append(
                (
                    "memory_usage",
                    f'container_memory_usage_bytes{{instance="{instance}"}}',
                )
            )

        if job:
            queries.append(
                (
                    "job_up",
                    f'up{{job="{job}"}}',
                )
            )
            queries.append(
                (
                    "job_errors",
                    f'rate(http_requests_total{{job="{job}",status=~"5.."}}[5m])',
                )
            )

        if pod and namespace:
            queries.append(
                (
                    "pod_cpu",
                    f'rate(container_cpu_usage_seconds_total{{pod="{pod}",namespace="{namespace}"}}[5m])',
                )
            )
            queries.append(
                (
                    "pod_memory",
                    f'container_memory_usage_bytes{{pod="{pod}",namespace="{namespace}"}}',
                )
            )

        for name, query_str in queries:
            result = self.query_range(query_str, start_time, end_time)
            if result["success"] and result["data"]:
                metrics[name] = result["data"]

        return {
            "lookback_minutes": lookback_minutes,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "metrics": metrics,
        }


prometheus_client = PrometheusClient()
