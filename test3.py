from lib_wrapper import AbortedSessionWrapper

session = AbortedSessionWrapper("zackerei")
status = session.get_status()
print(status)