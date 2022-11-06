class Task:
    def __init__(
        self,
        supertask = None
    ):
        self.supertask = supertask
        if self.supertask != None:
            self.supertask.addsubtask(self)
        self.subtasks = {}
        return

    def addsubtask(
        self,
        activity
    ):
        self.subtasks.update(activity)
        return

class Activity:
    def __init__(
        self,
        task:Task,
        type:str,
        prerequisite,
        **p
    ):
        self.__dict__.update(p)
        self.task = task
        self.type = type
        self.prerequisite = prerequisite

        self.task.addsubtask(self)
        return