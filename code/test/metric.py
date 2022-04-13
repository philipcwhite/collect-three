from recorder import Metric
metric = Metric('test_metric', 'description', '%', 100, {"resource_attribute":"test"})
metric.record()
