class Task:
    def __init__(
        self,
        name,
        supertask = None,
        subtasks = {},
        description = None
    ):
        self.name = name
        self.description = description
        self.supertask = supertask
        if self.supertask != None:
            self.supertask.addsubtask(self)
        self.subtasks = subtasks
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
        type:str,
        prerequisite,
        task:Task = None,
        **p
    ):
        self.__dict__.update(p)
        self.task = task
        if task != None:
            self.task.addsubtask(self)
        self.type = type
        self.prerequisite = prerequisite
        return