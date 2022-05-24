import time

time_node = time.time()


def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def runtime():
    global time_node
    end = time.time()
    diff = end - time_node
    time_node = end
    return diff
