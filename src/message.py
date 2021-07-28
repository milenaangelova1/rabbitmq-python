class Message:
    def __init__(self, param):
        self.__message = {
            "task": "task_{}",
            "param": param
        }
        
    def get_message(self):
        return self.__message