from opentelemetry.proto.trace.v1.trace_pb2 import Span, ResourceSpans, InstrumentationLibrarySpans, TracesData
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
import opentelemetry.proto.collector.trace.v1.trace_service_pb2_grpc as trace_service_pb2_grpc
import time, grpc, os

class Trace:
    def __init__(self, name = None, start_time = None, end_time = None, span_attributes = None, resource_attributes = None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.span_attributes = span_attributes
        self.resource_attributes = resource_attributes
        self.resource_spans = ResourceSpans() # Span Resource Attributes
        self.instrumentation_library_spans = InstrumentationLibrarySpans() # Group for multiple spans [list]
        self.span = Span() # Creates the span and parameters in span: trace_id, span_id, kind, name, start_time_unix_nano, end_time_unix_nano, attributes 
        self.trace_data = TracesData() # Top Level Traces
        self.key_value = KeyValue()
        self.otlp_endpoint = 'localhost:4317'
        
        if 'OTLP_ENDPOINT' in os.environ:
            self.otlp_endpoint = os.environ["OTLP_ENDPOINT"]

    def create_key_value(self, key, value):  
        '''Create Key Value Pair'''
        self.key_value.key = key
        self.key_value.value.string_value = value
        return self.key_value

    def create_trace(self):
        # Create Span
        self.span.trace_id = b'12345'
        self.span.span_id = b'12345'
        self.span.parent_span_id = b'1234'
        self.span.kind = 1 #SPAN_KIND_INTERNAL
        self.span.name = self.name
        self.span.start_time_unix_nano = self.start_time #int(time.time()*1000000000)
        self.span.end_time_unix_nano = self.end_time 
   
        # Add Span Attributes
        if not self.span_attributes is None:
            for k, v in self.span_attributes.items():
                self.span.attributes.extend([self.create_key_value(k, v)])

        # Create Instrumentation Library
        self.instrumentation_library_spans.instrumentation_library.name = 'OpenTelemetry Custom'
        self.instrumentation_library_spans.instrumentation_library.version = '0.1'
      
        # Add Spans to Instrumentation Library Spans
        self.instrumentation_library_spans.spans.extend([self.span])

        # Add Resource Attributes to my_resource_spans
        if not self.resource_attributes is None:
            for k, v in self.resource_attributes.items():
                self.resource_spans.resource.attributes.extend([self.create_key_value(k, v)])
        self.resource_spans.instrumentation_library_spans.extend([self.instrumentation_library_spans])
        self.trace_data.resource_spans.extend([self.resource_spans])
        return self.trace_data

    def record(self):
        with grpc.insecure_channel(self.otlp_endpoint) as channel:
            try:
                stub = trace_service_pb2_grpc.TraceServiceStub(channel)
                response = stub.Export(self.create_trace())
            except:
                print("Error connecting to GRPC Endpoint.")
            finally:
                print("Data Sent.")
