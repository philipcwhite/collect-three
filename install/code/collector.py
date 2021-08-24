from google.protobuf.json_format import MessageToJson
from concurrent import futures
import grpc, pymysql, logging

from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceResponse
from opentelemetry.proto.collector.metrics.v1 import metrics_service_pb2_grpc
from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import ExportLogsServiceResponse
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2_grpc
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceResponse
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2_grpc


class Data:
    def __init__(self):
        self.con = pymysql.connect(host = 'localhost', user = 'monitoring', password = 'password', db = 'monitoring', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.con.cursor()
    def __del__(self): self.con.close()
    def insert_metrics_json(self, packet):
        sql = "insert into metrics (packet) values(%s)"
        self.cursor.execute(sql, packet)
        self.con.commit()
    def insert_logs_json(self, packet):
        sql = "insert into logs (packet) values(%s)"
        self.cursor.execute(sql, packet)
        self.con.commit()
    def insert_trace_json(self, packet):
        sql = "insert into traces (packet) values(%s)"
        self.cursor.execute(sql, packet)
        self.con.commit()

class MetricsServiceServicer(metrics_service_pb2_grpc.MetricsServiceServicer):
    def Export(self, request, context):
        packet=MessageToJson(request)
        print(packet)
        D = Data()
        D.insert_metrics_json(packet)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return ExportMetricsServiceResponse()

class LogsServiceServicer(logs_service_pb2_grpc.LogsServiceServicer):
    def Export(self, request, context):
        packet=MessageToJson(request)
        print(packet)
        D = Data()
        D.insert_logs_json(packet)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return ExportLogsServiceResponse()

class TraceServiceServicer(trace_service_pb2_grpc.TraceServiceServicer):
    def Export(self, request, context):
        packet=MessageToJson(request)
        print(packet)
        D = Data()
        D.insert_trace_json(packet)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return ExportTraceServiceResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metrics_service_pb2_grpc.add_MetricsServiceServicer_to_server(MetricsServiceServicer(), server)
    logs_service_pb2_grpc.add_LogsServiceServicer_to_server(LogsServiceServicer(), server)
    trace_service_pb2_grpc.add_TraceServiceServicer_to_server(TraceServiceServicer(), server)
    server.add_insecure_port('[::]:7777')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
