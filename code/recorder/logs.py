from opentelemetry.proto.logs.v1.logs_pb2 import LogRecord, InstrumentationLibraryLogs, ResourceLogs, LogsData
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
import opentelemetry.proto.collector.logs.v1.logs_service_pb2_grpc as logs_service_pb2_grpc
import time, grpc

# Instantiate Classes
my_logs_data = None
my_resourcelogs = None
my_instrumentationlibrarylogs = None
my_log = None
my_resource_attribute = None
my_log_attribute = None

my_logs_data = LogsData()
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
 
def create_log(log_severity, log_body, log_attributes, resource_attributes):
    '''Assembles log for export'''
    if not resource_attributes is None:
        for k, v in resource_attributes.items():
            create_resource_attribute(k, v)
    if not log_attributes is None:
        for k, v in log_attributes.items():
            create_log_attribute(k, v)
    my_log.body.string_value = log_body
    my_log.severity_text = log_severity
    #my_log.severity_number = 9
    my_log.time_unix_nano = int(time.time()*1000000000)   
    my_instrumentationlibrarylogs.log_records.extend([my_log])  
    my_resourcelogs.instrumentation_library_logs.extend([my_instrumentationlibrarylogs])
    my_logs_data.resource_logs.extend([my_resourcelogs])
    return my_logs_data
 
def record(log_severity, log_body, log_attributes = None, resource_attributes = None):
    with grpc.insecure_channel('localhost:4317') as channel:
        try:
            stub = logs_service_pb2_grpc.LogsServiceStub(channel)
            response = stub.Export(create_log(log_severity, log_body, log_attributes, resource_attributes))
        except:
            print("Error connecting to GRPC Endpoint.")
        finally:
            print("Data Sent.")
            my_log.Clear()
            my_log_attribute.Clear()
            my_resource_attribute.Clear()

if __name__ == '__main__':
    record()
