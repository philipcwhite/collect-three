# collect-three
A simple Python application server for collecting, viewing, and alerting, utilizing the OpenTelemetry Framework


8-23-2021 Initial project has been uploaded.  This included the collector that receives otel OTLP protobuf data, a SQL script to create the database, and two testing scripts to create packets and send them.  The collector can also receive data directly from the otel collector if otlp is used as the exporter.  More directions will follow.
