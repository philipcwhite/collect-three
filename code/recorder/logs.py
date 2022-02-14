from opentelemetry.proto.logs.v1.logs_pb2 import LogRecord, InstrumentationLibraryLogs, ResourceLogs
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import ExportLogsServiceRequest
import opentelemetry.proto.collector.logs.v1.logs_service_pb2_grpc as logs_service_pb2_grpc
import time, grpc

# Instantiate Classes
my_exportlogsservicerequest = ExportLogsServiceRequest()
my_resourcelogs = ResourceLogs()
my_instrumentationlibrarylogs = InstrumentationLibraryLogs()
my_log = LogRecord()
my_resource_attribute = KeyValue()
my_log_attribute = KeyValue()

def create_resource_attribute(key, value):  
    '''Create Resource Attribute'''
    my_resource_attribute.key = key
    my_resource_attribute.value.string_value = value
    my_resourcelogs.resource.attributes.extend([my_resource_attribute])

def create_log_attribute(key, value):
    '''Create Log Attribute'''
    my_log_attribute.key = key
    my_log_attribute.value.string_value = value
    my_log.attributes.extend([my_log_attribute])
 
def create_log(log_name, log_severity, log_body, log_attributes, resource_attributes):
    '''Assembles metric for export'''
    for k, v in resource_attributes.items():
        create_resource_attribute(k, v)
    for k, v in log_attributes.items():
        create_log_attribute(k, v)
    my_log.name = log_name
    my_log.body.string_value = log_body
    my_log.severity_text = log_severity
    #my_log.severity_number = 9
    my_log.time_unix_nano = int(time.time()*1000000000)   
    my_instrumentationlibrarylogs.log_records.extend([my_log])  
    my_resourcelogs.instrumentation_library_logs.extend([my_instrumentationlibrarylogs])
    my_exportlogsservicerequest.resource_logs.extend([my_resourcelogs])
    return my_exportlogsservicerequest
 
def record(log_name, log_severity, log_body, log_attributes, resource_attributes):
    with grpc.insecure_channel('localhost:4317') as channel:
        stub = logs_service_pb2_grpc.LogsServiceStub(channel)
        response = stub.Export(create_log(log_name, log_severity, log_body, log_attributes, resource_attributes))
    print(response)

if __name__ == '__main__':
    record()
