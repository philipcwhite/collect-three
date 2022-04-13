# Example 1
from recorder import Log
log = Log()
log.severity = "Info"
log.body = "Test Message"
log.log_attributes = {"log_attribute":"test", "log_attribute2":"test2"}
log.resource_attributes = {"resource_attribute":"test","resource_attribute2":"test2"}
log.record()

# Example 2
#from recorder import Log
#log = Log("Info", "Body message", {"log_attribute":"test"}, {"resource_attribute":"test"})
#log.record()
