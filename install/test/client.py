import logging
import grpc

import opentelemetry.proto.collector.metrics.v1.metrics_service_pb2_grpc as metrics_service_pb2_grpc
from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceRequest

my_ExportMetricsServiceRequest = ExportMetricsServiceRequest()
f = open("metric.pb", "rb")
my_ExportMetricsServiceRequest.ParseFromString(f.read())

def run():
    with grpc.insecure_channel('localhost:7777') as channel:
        stub = metrics_service_pb2_grpc.MetricsServiceStub(channel)
        response = stub.Export(my_ExportMetricsServiceRequest)
    print(response)

if __name__ == '__main__':
    logging.basicConfig()
    run()
