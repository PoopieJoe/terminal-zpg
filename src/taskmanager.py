class Task:
    def __init__(
        self,
        name,
        entity = None,
        supertask = None,
        subtasks = {},
        description = None
    ):
        self.name = name
        self.description = description
        self.supertask = supertask
        if self.supertask != None:
            self.entity = supertask.entity
            self.supertask.addsubtask(self)
        else:
            self.entity = entity
        self.subtasks = subtasks
        return

    def addsubtask(
        self,
        activity
    ):
        activity.entity = self.entity # override child entity
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