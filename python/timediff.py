from datetime import datetime

t1 = datetime.now()
# something to do
t2 = datetime.now()
delta = t2 - t1

combined = delta.seconds + delta.microseconds / 1E6 # Result


