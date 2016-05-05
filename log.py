import time


class logger:
    def __init__(self):
        pass

    def write(self, message):
        with open("./order.log", 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\t" + message + '\n')
