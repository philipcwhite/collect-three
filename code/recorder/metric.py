from opentelemetry.proto.metrics.v1.metrics_pb2 import Metric as OTelMetric, ResourceMetrics, InstrumentationLibraryMetrics, NumberDataPoint, MetricsData
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
import opentelemetry.proto.collector.metrics.v1.metrics_service_pb2_grpc as metrics_service_pb2_grpc
import time, grpc, os

class Metric:
    def __init__(self, name = None, description = None, unit = None, value = None, resource_attributes = None):
        self.name = name
        self.description = description
        self.unit = unit
        self.value = value
        self.resource_attributes = resource_attributes
        self.metrics_data = MetricsData()
        self.resource_metrics = ResourceMetrics()
        self.instrumentation_library_metrics = InstrumentationLibraryMetrics()
        self.metric = OTelMetric()
        self.number_data_point = NumberDataPoint()
        self.key_value = KeyValue()
        self.otlp_endpoint = 'localhost:4317'
        
        if 'OTLP_ENDPOINT' in os.environ:
            self.otlp_endpoint = os.environ["OTLP_ENDPOINT"]
  
    def create_key_value(self, key, value):  
        '''Create Key Value Pair'''
        self.key_value.key = key
        self.key_value.value.string_value = value
        return self.key_value
 
    def create_metric(self):
        '''Assembles metric for export'''
        if not self.resource_attributes is None:
            for k, v in self.resource_attributes.items():
                self.resource_metrics.resource.attributes.extend([self.create_key_value(k, v)])
        self.metric.name = self.name
        self.metric.description = self.description
        self.metric.unit = self.unit
        self.number_data_point.time_unix_nano = int(time.time()*1000000000)
        self.number_data_point.as_int = self.value 
        self.metric.gauge.data_points.extend([self.number_data_point])
        self.instrumentation_library_metrics.metrics.extend([self.metric])
        self.resource_metrics.instrumentation_library_metrics.extend([self.instrumentation_library_metrics])
        self.metrics_data.resource_metrics.extend([self.resource_metrics])
        return self.metrics_data
 
    def record(self):
        with grpc.insecure_channel(self.otlp_endpoint) as channel:
            try:
                stub = metrics_service_pb2_grpc.MetricsServiceStub(channel)
                response = stub.Export(self.create_metric())
            except:
                print("Error connecting to GRPC Endpoint.")
            finally:
                print("Data Sent.")
