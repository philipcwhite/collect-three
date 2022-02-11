# This is very early code.  Just throwing up here for preservation.
# I will be adding an attribute function and making this work with the record module.

from google.protobuf.json_format import MessageToJson

from opentelemetry.proto.logs.v1.logs_pb2 import LogRecord, InstrumentationLibraryLogs, ResourceLogs #, LogsData
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import ExportLogsServiceRequest
import opentelemetry.proto.collector.logs.v1.logs_service_pb2_grpc as logs_service_pb2_grpc
import time, grpc

# Instantiate Classes
my_exportlogsservicerequest = ExportLogsServiceRequest()
my_resourcelogs = ResourceLogs()
my_instrumentationlibrarylogs = InstrumentationLibraryLogs()
my_log = LogRecord()
my_keyvalue = KeyValue()
 
def create_resource_attribute(key, value):  
    # Create Resource attribute
    my_keyvalue.key = key
    my_keyvalue.value.string_value = value
    my_resourcelogs.resource.attributes.extend([my_keyvalue])
 
def create_log(name, body, severity, attributes):
    '''Assembles metric for export'''
    for k, v in attributes.items():
        create_resource_attribute(k, v)

    my_log.name = name
    #my_attribute = KeyValue()
    # Create attribute function
    #my_attribute.key = "body"
    #my_attribute.value.string_value = "message"
    #my_log.attributes.extend([my_attribute])
    
    my_log.body.string_value = "Message"
    my_log.severity_text = severity
    my_log.severity_number = 9
    my_log.time_unix_nano = int(time.time()*1000000000)   
    my_instrumentationlibrarylogs.log_records.extend([my_log])  
    my_resourcelogs.instrumentation_library_logs.extend([my_instrumentationlibrarylogs])
    my_exportlogsservicerequest.resource_logs.extend([my_resourcelogs])
    return my_exportlogsservicerequest
 
def record():
    with grpc.insecure_channel('localhost:4317') as channel:
        stub = logs_service_pb2_grpc.LogsServiceStub(channel)
        response = stub.Export(create_log('name', 'body', 'Info', {"hello":"world", "awesome":"sauce"}))
    print(response)

if __name__ == '__main__':
    record()
