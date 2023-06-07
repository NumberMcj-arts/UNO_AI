from lib_wrapper import AbortedSessionWrapper

session = AbortedSessionWrapper("zackerei")
session.start_new_session(['arthur', 'hans', 'johannes'], ['harald'], 7)