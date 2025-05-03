from opentelemetry import trace, baggage, context
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

resource = Resource(attributes={SERVICE_NAME: "payment-service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

tracer = trace.get_tracer(__name__)

def process_payment(user_id):
    ctx = baggage.set_baggage("user_id", user_id)
    token = context.attach(ctx)

    with tracer.start_as_current_span("process_payment", context=ctx) as span:
        span.set_attribute("payment_method", "credit_card")

        span.set_attribute("user_id", baggage.get_baggage("user_id", context=ctx))
        print(f"Processed payment for user {user_id}")

    context.detach(token)

if __name__ == "__main__":
    process_payment("123457")

