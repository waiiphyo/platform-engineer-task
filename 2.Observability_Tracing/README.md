# 2. Observability &amp; Tracing

### This setup demonstrates how to:

- Use OpenTelemetry Python SDK to create a manual span inside the process_payment(user_id) function.
- Add baggage (user_id) and a custom span attribute (payment_method).
- Export trace data to a locally running OTEL Collector via the OTLP exporter.
- Visualize traces using Jaeger UI via Docker Compose.

### This project uses Python Virtual Environment for dependency isolation.
### Create and activate venv:
```
python3 -m venv venv
source venv/bin/activate

```
### Install dependencies:
```
pip install -r requirements.txt
```

### Docker Setup
Services:
- OpenTelemetry Collector: Accepts OTLP data via gRPC on port 4317

### Running the Project
```
docker-compose up -d
python main.py
```

### Output
```
otel-collector_1  |      -> service.name: Str(payment-service)
otel-collector_1  | ScopeSpans #0
otel-collector_1  | ScopeSpans SchemaURL: 
otel-collector_1  | InstrumentationScope __main__ 
otel-collector_1  | Span #0
otel-collector_1  |     Trace ID       : a7fca6d17df3626f16c213bf672f80ce
otel-collector_1  |     Parent ID      : 
otel-collector_1  |     ID             : 6e91a29841832e21
otel-collector_1  |     Name           : process_payment
otel-collector_1  |     Kind           : Internal
otel-collector_1  |     Start time     : 2025-05-03 04:36:13.176233236 +0000 UTC
otel-collector_1  |     End time       : 2025-05-03 04:36:13.17626782 +0000 UTC
otel-collector_1  |     Status code    : Unset
otel-collector_1  |     Status message : 
otel-collector_1  | Attributes:
otel-collector_1  |      -> payment_method: Str(credit_card)
otel-collector_1  |      -> user_id: Str(123457)
```
---

## /checkout API - SLO-based Alerting Rules

### Summary

This setup defines **Service Level Indicators (SLIs)**, **Service Level Objectives (SLOs)**, and **Prometheus alerting rules** using a **multi-window burn rate strategy** to monitor the performance and reliability of the `/checkout` API endpoint, which is experiencing frequent latency spikes.

---

## SLIs (Service Level Indicators)

1. **Request Latency**  
   - Metric: `http_request_duration_seconds_bucket`
   - SLI: Proportion of requests to `/checkout` completing within **250ms**  
   - Formula:
     ```text
     rate(http_request_duration_seconds_bucket{le="0.25", path="/checkout"}[5m])
     / rate(http_requests_total{path="/checkout"}[5m])
     ```

2. **Error Rate**  
   - Metric: `http_requests_total`
   - SLI: Proportion of **5xx errors** returned by `/checkout`  
   - Formula:
     ```text
     rate(http_requests_total{status=~"5..", path="/checkout"}[5m])
     / rate(http_requests_total{path="/checkout"}[5m])
     ```

---

## SLO Targets

| SLI Type        | Objective             |
|----------------|-----------------------|
| Latency         | 95% of requests < 250ms |
| Error Rate      | < 0.1% (99.9% success)  |

---

## Prometheus Alerting Rules (Multi-Window Burn Rate)

```yaml
groups:
- name: checkout-api-alerts
  rules:
  - alert: HighLatencyBurnRate
    expr: |
      (rate(http_request_duration_seconds_bucket{le="0.25", path="/checkout"}[5m])
       / rate(http_requests_total{path="/checkout"}[5m])) < 0.95
    for: 10m
    labels:
      severity: critical
    annotations:
      summary: "High latency on /checkout endpoint"

  - alert: HighErrorRateBurnRate
    expr: |
      (rate(http_requests_total{status=~"5..", path="/checkout"}[5m])
       / rate(http_requests_total{path="/checkout"}[5m])) > 0.001
    for: 10m
    labels:
      severity: critical
    annotations:
      summary: "Error rate too high on /checkout"
```
---