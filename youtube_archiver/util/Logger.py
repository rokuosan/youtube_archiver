class Logger:
    def debug(self, msg: str):
        if not msg.startswith('[debug] '):
            self.info(msg)
        else:
            print(msg)

    def info(self, msg):
        print(f"[info] {msg}")

    def warning(self, msg):
        pass

    def error(self, msg):
        pass
