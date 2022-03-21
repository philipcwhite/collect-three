from opentelemetry.proto.trace.v1.trace_pb2 import Span, ResourceSpans, InstrumentationLibrarySpans ,TracesData
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
import opentelemetry.proto.collector.trace.v1.trace_service_pb2_grpc as trace_service_pb2_grpc
import time, grpc

# Instantiate Classes
my_resource_spans = None
my_instrumentation_library_spans = None
my_span = None
my_resource_attribute = None
my_span_attribute = None
my_trace_data = None

my_resource_spans = ResourceSpans() #Span Resource Attributes
my_instrumentation_library_spans = InstrumentationLibrarySpans() #Group for multiple spans [list]
my_span = Span() # Creates the span and parameters in span: trace_id, span_id, kind, name, start_time_unix_nano, end_time_unix_nano, attributes 
my_resource_attribute = KeyValue() #Trace Key Value Pair
my_span_attribute = KeyValue() #Span Resource Attributes
my_trace_data = TracesData() # Top Level Traces

def create_resource_attribute(key, value):  
    '''Create Resource Attribute'''
    my_resource_attribute.key = key
    my_resource_attribute.value.string_value = value
    my_resource_spans.resource.attributes.extend([my_resource_attribute])

def create_span_attribute(key, value):  
    '''Create Resource Attribute'''
    my_span_attribute.key = key
    my_span_attribute.value.string_value = value
    my_span.attributes.extend([my_span_attribute])

def create_instrumentation_library_spans(trace_name, start_time_unix_nano, end_time_unix_nano, span_attributes):
    # Create Span
    my_span.trace_id = b'12345'
    my_span.span_id = b'12345'
    my_span.parent_span_id = b'1234'
    my_span.kind = 1 #SPAN_KIND_INTERNAL
    my_span.name = trace_name
    my_span.start_time_unix_nano = start_time_unix_nano #int(time.time()*1000000000)
    my_span.end_time_unix_nano = end_time_unix_nano 
   
    # Add Span Attributes
    if not span_attributes is None:
        for k, v in span_attributes.items():
            create_span_attribute(k, v)

    # Create Instrumentation Library
    my_instrumentation_library_spans.instrumentation_library.name = 'otel'
    my_instrumentation_library_spans.instrumentation_library.version = '1234'
    
    # Add Spans to Instrumentation Library Spans
    my_instrumentation_library_spans.spans.extend([my_span])


def create_trace(trace_name, start_time_unix_nano, end_time_unix_nano, span_attributes, resource_attributes):
    # Add Instrumentation Library Info/Spans
    create_instrumentation_library_spans(trace_name, start_time_unix_nano, end_time_unix_nano, span_attributes)
    
    # Add Resource Attributes to my_resource_spans
    if not resource_attributes is None:
        for k, v in resource_attributes.items():
            create_resource_attribute(k, v)
    my_resource_spans.instrumentation_library_spans.extend([my_instrumentation_library_spans])
    my_trace_data.resource_spans.extend([my_resource_spans])
    #print(my_trace_data)
    #print(my_trace_data.SerializeToString())
    return my_trace_data

def record(trace_name, start_time_unix_nano, end_time_unix_nano, span_attributes = None, resource_attributes = None):
    with grpc.insecure_channel('localhost:4317') as channel:
        try:
            stub = trace_service_pb2_grpc.TraceServiceStub(channel)
            response = stub.Export(create_trace(trace_name, start_time_unix_nano, end_time_unix_nano, span_attributes, resource_attributes))
        except:
            print("Error connecting to GRPC Endpoint.")
        finally:
            print("Data Sent.")
            my_span.Clear()
            my_span_attribute.Clear()
            my_resource_attribute.Clear()

if __name__ == '__main__':
    record()

#create_trace(trace_name='test', start_time_unix_nano = int(time.time()*1000000000), end_time_unix_nano = int(time.time()*1000000000), span_attributes={'hello':'world','foo':'bar'}, resource_attributes={'hello':'world','foo':'bar'})
