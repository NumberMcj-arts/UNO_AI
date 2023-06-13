from lib_wrapper import AbortedSessionWrapper
import json

session = AbortedSessionWrapper("zackerei")
status = session.get_status()
# Serializing json
json_object = json.dumps(status, indent=4)
 
# Writing to sample.json
with open("../../database/sample.json", "w") as outfile:
    outfile.write(json_object)
print(status)