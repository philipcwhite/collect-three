from opentelemetry.proto.logs.v1.logs_pb2 import LogRecord, InstrumentationLibraryLogs, ResourceLogs, LogsData
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
import opentelemetry.proto.collector.logs.v1.logs_service_pb2_grpc as logs_service_pb2_grpc
import time, grpc, os

class Log:
    def __init__(self, severity = None, body = None, log_attributes = None, resource_attributes = None): 
        self.severity = severity
        self.body = body
        self.log_attributes = log_attributes
        self.resource_attributes = resource_attributes
        self.instrumentation_library_logs = InstrumentationLibraryLogs()
        self.log_record = LogRecord()
        self.logs_data = LogsData()
        self.resource_logs = ResourceLogs()
        self.key_value = KeyValue()
        self.otlp_endpoint = 'localhost:4317'
        
        if 'OTLP_ENDPOINT' in os.environ:
            self.otlp_endpoint = os.environ["OTLP_ENDPOINT"]
    
    def create_key_value(self, key, value):  
        '''Create Key Value Pair'''
        self.key_value.key = key
        self.key_value.value.string_value = value
        return self.key_value
 
    def create_log(self):
        '''Assembles metric for export'''
        if not self.resource_attributes is None:
            for k, v in self.resource_attributes.items():
                self.resource_logs.resource.attributes.extend([self.create_key_value(k, v)])
        if not self.log_attributes is None:
            for k, v in self.log_attributes.items():
                self.log_record.attributes.extend([self.create_key_value(k, v)])
        self.log_record.body.string_value = self.body
        self.log_record.severity_text = self.severity
        #self.log_record.severity_number = 9
        self.log_record.time_unix_nano = int(time.time()*1000000000)   
        self.instrumentation_library_logs.log_records.extend([self.log_record])  
        self.resource_logs.instrumentation_library_logs.extend([self.instrumentation_library_logs])
        self.logs_data.resource_logs.extend([self.resource_logs])
        return self.logs_data
 
    def record(self):
        with grpc.insecure_channel(self.otlp_endpoint) as channel:
            stub = logs_service_pb2_grpc.LogsServiceStub(channel)
            try:
                stub = logs_service_pb2_grpc.LogsServiceStub(channel)
                response = stub.Export(self.create_log())
            except:
                print("Error connecting to GRPC Endpoint.")
            finally:
                print("Data Sent.")
