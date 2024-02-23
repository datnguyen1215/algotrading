import { HttpInstrumentation } from '@opentelemetry/instrumentation-http';
import {
  ConsoleSpanExporter,
  SimpleSpanProcessor,
  NodeTracerProvider
} from '@opentelemetry/sdk-trace-node';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { Resource } from '@opentelemetry/resources';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import settings from '@src/settings';

const provider = new NodeTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]:
      settings.observability.tracing.service.name,
    [SemanticResourceAttributes.SERVICE_VERSION]:
      settings.observability.tracing.service.version
  })
});

const consoleExporter = new ConsoleSpanExporter();
const otlpExporter = new OTLPTraceExporter({
  url: settings.observability.tracing.endpoint
});
provider.addSpanProcessor(new SimpleSpanProcessor(consoleExporter));
provider.addSpanProcessor(new SimpleSpanProcessor(otlpExporter));
provider.register({
  instrumentations: [new HttpInstrumentation()]
});

export default provider;
