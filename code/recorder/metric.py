from opentelemetry.proto.metrics.v1.metrics_pb2 import Metric, ResourceMetrics, InstrumentationLibraryMetrics, NumberDataPoint
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceRequest
import opentelemetry.proto.collector.metrics.v1.metrics_service_pb2_grpc as metrics_service_pb2_grpc
import time, grpc

# Instantiate Classes
my_exportmetricsservicerequest = ExportMetricsServiceRequest()
my_resourcemetrics = ResourceMetrics()
my_instrumentationlibrarymetrics = InstrumentationLibraryMetrics()
my_metric = Metric()
my_number = NumberDataPoint()
my_keyvalue = KeyValue()
 
def create_datapoint(name, description, unit, value): 
    # Create Datapoint, Default Gauge 
    my_metric.name = name
    my_metric.description = description
    my_metric.unit = unit
    #my_metric.sum.is_monotonic = False
    #my_metric.sum.aggregation_temporality = 2 # Delta 1 Cumulative 2
    my_number.time_unix_nano = int(time.time()*1000000000)
    my_number.as_int = value #random.randint(0,100)
    my_metric.sum.data_points.extend([my_number])
    my_metric.gauge.data_points.extend([my_number])

def create_resource_attribute(key, value):  
    # Create Resource attribute
    my_keyvalue.key = key
    my_keyvalue.value.string_value = value
    my_resourcemetrics.resource.attributes.extend([my_keyvalue])
 
def create_metric(name, description, unit, value, attributes):
    '''Assembles metric for export'''
    create_datapoint(name, description, unit, value) 
    for k, v in attributes.items():
        create_resource_attribute(k, v)
    my_instrumentationlibrarymetrics.metrics.extend([my_metric])
    my_resourcemetrics.instrumentation_library_metrics.extend([my_instrumentationlibrarymetrics])
    my_exportmetricsservicerequest.resource_metrics.extend([my_resourcemetrics])
    return my_exportmetricsservicerequest
 
def record(name, description, unit, value, attributes):
    with grpc.insecure_channel('localhost:4317') as channel:
        stub = metrics_service_pb2_grpc.MetricsServiceStub(channel)
        response = stub.Export(create_metric(name, description, unit, value, attributes))
        #response = stub.Export(create_metric('name', 'description', '$', 100, {"hello":"world", "awesome":"sauce"}))
    print(response)

if __name__ == '__main__':
    record()

#create_metric('name', 'description', '$', 100, {"hello":"world", "awesome":"sauce"})
