from src.constants import *
import src.events as events

class Task:
    def __init__(
        self,
        root,
        name,
        subtasks = [],
        supertask = None,
        description = None,
        mode = TASKMODES.PARALLEL
    ):
        self.root = root #taskmanager
        self.name = name
        self.description = description
        self.supertask = supertask
        if self.supertask != None:
            self.supertask.addsubtask(self)
        else:
            self.supertask = self.root
        self.mode = mode
        self.subtasks = subtasks
        self.complete = False
        return

    def addsubtask(
        self,
        activity
    ):
        activity.task = self
        activity.root = self.root
        self.subtasks.append(activity)
        return

    def checkCompleted( 
        self
    ):
        """recursively checks if task was completed between this and the last call. to check if the task was completed before, check .complete"""
        if self.complete == True:
            return False

        for subtask in self.subtasks:
            if not subtask.complete:
                subtask.checkCompleted()

        if all([subtask.complete for subtask in self.subtasks]):
            events.onTaskComplete(self)
            self.complete = True
        return self.complete



class Activity:
    def __init__(
        self,
        root,
        task
    ):
        self.root = root
        self.task = task
        if self.task != None:
            self.task.addsubtask(self)
        self.complete = False
        return
        
    def _getcontroller(self): return self.root.entity.controller

    def checkCompleted(
        self
    ):
        raise NotImplementedError

class GotoActivity(Activity):
    def __init__(
        self,
        root,
        task,
        destination
    ):
        Activity.__init__(self,root,task)
        self.destination = destination
        return

    def checkCompleted(
        self
    ):
        """Checks if task was completed between this and the last call. to check if the task was completed before, check .complete"""
        if self.complete == True:
            return False

        # check if pc is at destination
        pc = self._getcontroller().pc
        margin = 0.5
        if( self.destination[0]-margin < pc.pos[0] and self.destination[0]+margin > pc.pos[0]
            and self.destination[1]-margin < pc.pos[1] and self.destination[1]+margin > pc.pos[1]):
            events.onTaskComplete(self)
            self.complete = True
        return self.complete

    
class TaskManager:
    def __init__(
        self,
        entity,
        tasks = []
    ):
        self.entity = entity
        self.tasks = tasks
        return

    def addTask(
        self,
        task:Task,
        supertask:Task = None
    ):  
        if supertask == None:
            task.supertask = self
            task.root = self
            self.tasks.append(task)
        else:
            supertask.addsubtask(task)

    def checkTaskCompletion(
        self
    ):
        for task in self.tasks:
            task.checkCompleted()