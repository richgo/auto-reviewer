---
name: observability
description: >
  Detect observability gaps: insufficient logging for debugging, missing metrics for SLOs, high
  cardinality metrics causing cost issues, alert fatigue from noisy alerts, and missing distributed
  tracing correlation. Trigger when reviewing logging statements, metrics instrumentation, alert
  configurations, or distributed system code. Critical for production debugging and SRE health.
---

# Observability Review

## Purpose
Review code for observability gaps that hinder debugging and monitoring: logging insufficient for root cause analysis, missing metrics for SLOs, high-cardinality metrics, alert fatigue, and missing trace correlation in distributed systems.

## Scope
1. **Logging Gaps** — missing context, no structured logging, insufficient error details, log levels wrong
2. **Missing Metrics** — no SLI/SLO instrumentation, business metrics missing, no latency percentiles
3. **Metric Cardinality** — unbounded labels, user IDs in metrics, cardinality explosion
4. **Alert Fatigue** — noisy alerts, no actionable playbook, alert on symptoms not causes
5. **Missing Tracing** — no correlation IDs, spans missing, distributed traces incomplete

## Detection Strategy

### 1. Logging Gaps Red Flags
- **No context** in logs (missing request ID, user ID, operation)
- **Plain string logging** (not structured JSON/key-value)
- **Missing error logs** before exceptions
- **Wrong log levels** (info for errors, debug for warnings)
- **Sensitive data** in logs (covered in data-integrity skill)

**High-risk patterns:**
```python
# ❌ INSUFFICIENT
logger.info("Processing request")  # No context
try:
    result = operation()
except Exception:
    pass  # No error log
```

### 2. Missing Metrics Red Flags
- **No request duration** metrics (latency percentiles)
- **No error rate** metrics
- **Business metrics missing** (orders/min, revenue/hour)
- **Resource utilization** not tracked (CPU, memory, connections)
- **No SLI metrics** (success rate, latency p99)

**High-risk patterns:**
```python
# ❌ MISSING: No instrumentation
def process_order(order):
    # Business-critical operation with no metrics
    payment = charge_card(order)
    ship_order(order)
    return order_id
```

### 3. Metric Cardinality Red Flags
- **User ID as metric label** (unbounded cardinality)
- **URL path with IDs** (`/users/123` → explodes cardinality)
- **Email addresses** in labels
- **Timestamps** as labels
- **High-cardinality dimensions** without aggregation

**High-risk patterns:**
```python
# ❌ CARDINALITY EXPLOSION
metrics.counter('requests', labels={'user_id': user.id, 'path': request.path})
# Millions of time series created
```

### 4. Alert Fatigue Red Flags
- **Alerting on every error** (even expected ones)
- **No alert grouping** (100 alerts for same issue)
- **Alerts without runbooks**
- **Symptom-based alerts** (disk full) without cause-based (writes increasing)
- **No alert thresholds** (alert on any failure)

**High-risk patterns:**
```yaml
# ❌ NOISY
alerts:
  - name: AnyError
    expr: error_count > 0  # Fires constantly
    severity: critical
```

### 5. Missing Tracing Red Flags
- **No trace/correlation ID** propagation across services
- **Spans not created** for external calls
- **Missing trace context** in logs
- **Sampling too aggressive** (missing important traces)
- **No parent-child span relationships**

**High-risk patterns:**
```python
# ❌ MISSING: No tracing
def call_downstream_service():
    response = requests.get('http://service-b/api')
    # No trace propagation
    return response.json()
```

## Platform-Specific Guidance

### Web/API
- **Primary risks:** Missing latency metrics, no correlation IDs, alert fatigue
- **Key review areas:** Route handlers, middleware, error handlers
- **Best practices:** Structured logging (structlog), Prometheus metrics, OpenTelemetry tracing

### Android
- **Primary risks:** Missing crash reporting, no ANR detection, insufficient breadcrumbs
- **Key review areas:** Crashlytics/Sentry integration, StrictMode config, custom events
- **Best practices:** Firebase Crashlytics, custom logging with breadcrumbs, ProGuard mapping upload

### iOS
- **Primary risks:** Unsymbolicated crashes, missing MetricKit data, no hang detection
- **Key review areas:** dSYM upload, MetricKit subscribers, custom signposts
- **Best practices:** Crash reporting (Sentry), MetricKit diagnostics, os_signpost for profiling

### Microservices
- **Primary risks:** Missing correlation IDs, incomplete traces, no SLO tracking
- **Key review areas:** Service-to-service calls, message handlers, gateway middleware
- **Best practices:** OpenTelemetry, Jaeger/Zipkin, SLO dashboards (Grafana), log aggregation (ELK)

## Review Instructions

### Step 1: Audit Logging Coverage
```bash
# Find operations without logging
rg "def (create|update|delete|process)" --type py -A 10 | rg -v "logger\."
```

**Good logging pattern:**
```python
# ✅ GOOD: Structured logging with context
import structlog

logger = structlog.get_logger()

def process_order(order_id, user_id):
    log = logger.bind(order_id=order_id, user_id=user_id, operation="process_order")
    log.info("order_processing_started")
    
    try:
        payment = charge_card(order_id)
        log.info("payment_completed", payment_id=payment.id, amount=payment.amount)
        
        ship_order(order_id)
        log.info("order_shipped")
        
        return order_id
    except PaymentError as e:
        log.error("payment_failed", error=str(e), error_type=type(e).__name__)
        raise
    except Exception as e:
        log.exception("order_processing_failed", error=str(e))
        raise
```

### Step 2: Add Metrics
```python
# ✅ GOOD: Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

order_requests = Counter('orders_total', 'Total orders', ['status'])
order_duration = Histogram('order_duration_seconds', 'Order processing duration')
order_value = Histogram('order_value_dollars', 'Order value')
active_orders = Gauge('active_orders', 'Currently processing orders')

@order_duration.time()
def process_order(order):
    active_orders.inc()
    try:
        result = do_processing(order)
        order_requests.labels(status='success').inc()
        order_value.observe(order.total_amount)
        return result
    except Exception as e:
        order_requests.labels(status='failure').inc()
        raise
    finally:
        active_orders.dec()
```

### Step 3: Fix Cardinality Issues
```python
# ❌ HIGH CARDINALITY
metrics.counter('api_requests', labels={
    'user_id': user.id,  # Unbounded
    'path': request.path  # /users/123, /users/456, ...
})

# ✅ FIXED: Bounded labels
metrics.counter('api_requests', labels={
    'method': request.method,  # GET, POST, PUT, DELETE
    'route': request.route_pattern,  # /users/:id (parameterized)
    'status_code': response.status // 100 * 100  # 200, 400, 500
})
```

### Step 4: Actionable Alerts
```yaml
# ✅ GOOD: SLO-based alert
groups:
  - name: order_processing
    interval: 30s
    rules:
      - alert: OrderProcessingSLOViolation
        expr: |
          (
            sum(rate(order_requests{status="success"}[5m]))
            /
            sum(rate(order_requests[5m]))
          ) < 0.99
        for: 5m
        labels:
          severity: warning
          team: payments
        annotations:
          summary: "Order success rate below 99% SLO"
          description: "Success rate is {{ $value | humanizePercentage }}"
          runbook: "https://wiki.example.com/runbooks/order-slo"
          dashboard: "https://grafana.example.com/d/orders"
```

### Step 5: Add Distributed Tracing
```python
# ✅ GOOD: OpenTelemetry tracing
from opentelemetry import trace
from opentelemetry.propagate import inject

tracer = trace.get_tracer(__name__)

def call_downstream_service(order_id):
    with tracer.start_as_current_span("call_downstream") as span:
        span.set_attribute("order_id", order_id)
        span.set_attribute("service", "inventory")
        
        headers = {}
        inject(headers)  # Inject trace context into headers
        
        try:
            response = requests.get(
                'http://inventory-service/check',
                headers=headers,
                timeout=5
            )
            span.set_attribute("http.status_code", response.status_code)
            return response.json()
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise
```

## Platform-Specific Examples

### Android: Crash Reporting
```kotlin
// ✅ GOOD: Crashlytics with breadcrumbs
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        FirebaseCrashlytics.getInstance().setCrashlyticsCollectionEnabled(!BuildConfig.DEBUG)
    }
}

fun processPayment(amount: Double) {
    FirebaseCrashlytics.getInstance().log("Payment processing started: amount=$amount")
    
    try {
        val result = paymentProcessor.charge(amount)
        FirebaseCrashlytics.getInstance().log("Payment successful: txn=${result.transactionId}")
    } catch (e: PaymentException) {
        FirebaseCrashlytics.getInstance().recordException(e)
        FirebaseCrashlytics.getInstance().setCustomKey("payment_amount", amount)
        FirebaseCrashlytics.getInstance().setCustomKey("error_code", e.code)
        throw e
    }
}
```

### iOS: MetricKit
```swift
// ✅ GOOD: MetricKit diagnostics
import MetricKit

class MetricsManager: NSObject, MXMetricManagerSubscriber {
    override init() {
        super.init()
        MXMetricManager.shared.add(self)
    }
    
    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads {
            // Log metrics to backend
            if let hangDiagnostics = payload.applicationHangTime {
                os_log("Hang detected: %@", log: .default, type: .error, hangDiagnostics.debugDescription)
                sendToBackend(hangDiagnostics)
            }
            
            if let diskWrites = payload.diskIOMetrics {
                os_log("Disk writes: %@ MB", log: .default, type: .info, diskWrites.cumulativeLogicalWrites)
            }
        }
    }
}
```

### Microservices: Correlation ID
```python
# ✅ GOOD: Correlation ID propagation
from flask import Flask, request, g
import uuid

app = Flask(__name__)

@app.before_request
def extract_correlation_id():
    g.correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    logger.bind(correlation_id=g.correlation_id)

@app.after_request
def inject_correlation_id(response):
    response.headers['X-Correlation-ID'] = g.correlation_id
    return response

def call_other_service():
    headers = {'X-Correlation-ID': g.correlation_id}
    response = requests.get('http://service-b/api', headers=headers)
    return response.json()
```

## Migration Coverage

## OWASP References
- [Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [Logging Vocabulary](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html)

## Quick Checklist
- [ ] Structured logging with context (request_id, user_id, operation)
- [ ] Error logs include stack traces and error details
- [ ] Metrics for latency (p50, p95, p99)
- [ ] Metrics for error rates
- [ ] Business metrics instrumented
- [ ] Metric labels bounded (no user IDs, no paths with IDs)
- [ ] Alerts based on SLOs, not individual errors
- [ ] Alerts include runbooks
- [ ] Distributed tracing with correlation IDs
- [ ] Trace context propagated across services
