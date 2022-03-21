import time
from recorder import trace
trace.record('test', int(time.time()*1000000000), int(time.time()*1000000000), {'hello':'world','foo':'bar'}, {'hello':'world','foo':'bar'})
