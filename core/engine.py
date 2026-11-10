current_target = None
current_node = None
cwd = "/"
credentials = {}
logged_user = None
counter_hack = False
latency = 0.0
last_target = None
alert_tier = {}


def connect(target):
    global current_target, current_node, cwd, logged_user, last_target
    current_target = target
    last_target = target
    current_node = None
    cwd = "/"
    logged_user = None


def disconnect():
    global current_target, current_node, cwd, logged_user
    current_target = None
    current_node = None
    cwd = "/"
    logged_user = None


def cool_down():
    global counter_hack, latency
    counter_hack = False
    latency = 0.0
