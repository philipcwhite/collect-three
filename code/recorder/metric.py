from opentelemetry.proto.metrics.v1.metrics_pb2 import Metric, ResourceMetrics, InstrumentationLibraryMetrics, NumberDataPoint, MetricsData
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
import opentelemetry.proto.collector.metrics.v1.metrics_service_pb2_grpc as metrics_service_pb2_grpc
import time, grpc

# Instantiate Classes
my_metrics_data = None
my_resourcemetrics = None
my_instrumentation_library_metrics = None
my_metric = None
my_number = None
my_resource_attribute = None

my_metrics_data = MetricsData()
my_resourcemetrics = ResourceMetrics()
my_instrumentation_library_metrics = InstrumentationLibraryMetrics()
my_metric = Metric()
my_number = NumberDataPoint()
my_resource_attribute = KeyValue()
 
def create_datapoint(metric_name, metric_description, metric_unit, metric_value): 
    '''Create Datapoint'''
    my_metric.name = metric_name
    my_metric.description = metric_description
    my_metric.unit = metric_unit
    #my_metric.sum.is_monotonic = False
    #my_metric.sum.aggregation_temporality = 2 # Delta 1 Cumulative 2
    my_number.time_unix_nano = int(time.time()*1000000000)
    my_number.as_int = metric_value #random.randint(0,100)
    my_metric.sum.data_points.extend([my_number])
    my_metric.gauge.data_points.extend([my_number])

def create_resource_attribute(key, value):  
    '''Create Resource Attribute'''
    my_resource_attribute.key = key
    my_resource_attribute.value.string_value = value
    my_resourcemetrics.resource.attributes.extend([my_resource_attribute])
 
def create_metric(metric_name, metric_description, metric_unit, metric_value, metric_attributes):
    '''Assembles metric for export'''
    create_datapoint(metric_name, metric_description, metric_unit, metric_value) 
    if not metric_attributes is None:
        for k, v in metric_attributes.items():
            create_resource_attribute(k, v)
    my_instrumentation_library_metrics.metrics.extend([my_metric])
    my_resourcemetrics.instrumentation_library_metrics.extend([my_instrumentation_library_metrics])
    my_metrics_data.resource_metrics.extend([my_resourcemetrics])
    return my_metrics_data
 
def record(metric_name, metric_description, metric_unit, metric_value, metric_attributes = None):
    with grpc.insecure_channel('localhost:4317') as channel:
        try:
            stub = metrics_service_pb2_grpc.MetricsServiceStub(channel)
            response = stub.Export(create_metric(metric_name, metric_description, metric_unit, metric_value, metric_attributes))
        except:
            print("Error connecting to GRPC Endpoint.")
        finally:
            print("Data Sent.")
            my_metric.Clear()
            my_number.Clear()
            my_resource_attribute.Clear() 

if __name__ == '__main__':
    record()
