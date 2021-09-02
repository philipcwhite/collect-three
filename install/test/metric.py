from google.protobuf.json_format import MessageToJson
from opentelemetry.proto.metrics.v1.metrics_pb2 import Metric, ResourceMetrics, InstrumentationLibraryMetrics, NumberDataPoint
from opentelemetry.proto.common.v1.common_pb2 import KeyValue
from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceRequest
import random, time 
 
# Instantiate Classes
my_exportmetricsservicerequest = ExportMetricsServiceRequest()
my_resourcemetrics = ResourceMetrics()
my_instrumentationlibrarymetrics = InstrumentationLibraryMetrics()
my_metric = Metric()
my_number = NumberDataPoint()
my_keyvalue = KeyValue()
 
 
# Create Metric
my_metric.name = 'otel.cpu.percent'
my_metric.description = 'CPU Percent'
my_metric.unit = '%'
my_metric.sum.aggregation_temporality = 2 # Cumulative
my_number.time_unix_nano = int(time.time()*1000000000)
my_number.as_int = random.randint(0,100)
 
 
# Create Resource Tag
my_keyvalue.key = 'host.name'
my_keyvalue.value.string_value = 'white05'
 
 
# Create packet
my_metric.sum.data_points.extend([my_number])
my_instrumentationlibrarymetrics.metrics.extend([my_metric])
my_resourcemetrics.resource.attributes.extend([my_keyvalue])
my_resourcemetrics.instrumentation_library_metrics.extend([my_instrumentationlibrarymetrics])
my_exportmetricsservicerequest.resource_metrics.extend([my_resourcemetrics])
 
 
# Write packets to files
with open("metric.pb", "wb") as f:
    f.write(my_exportmetricsservicerequest.SerializeToString())
with open("metric.protobuf", "w") as f:
    f.write(str(my_exportmetricsservicerequest))
with open("metric.json", "w") as f:
    f.write(str(MessageToJson(my_exportmetricsservicerequest)))
