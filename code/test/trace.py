import time
from recorder import Trace
trace = Trace('test', int(time.time()*1000000000), int(time.time()*1000000000), {'hello':'world','foo':'bar'}, {'hello':'world','foo':'bar'})
trace.record()
