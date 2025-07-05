# Moudles
from datetime import datetime, date
import os   
import time
import json

#======= Task =======

class Task:
    # Constructor
    def __init__(self):

        
        self.title = self.SetTitle()
        self.Date = date.today()
        self.deadline = self.SetDate().date()
        self.DayLeftTillDeadline = (self.deadline -self.Date).days
        self.done = False
        if self.DayLeftTillDeadline < 0 :
            self.DayLeftTillDeadline = 0
        if "(Late)" not in self.title :
            self.title += "(Late)"
 
    # Mark Done Task
    def MarkDone(self):
        self.done = True

    # Is deadline pass
    def IsLate(self):
        if self.deadline and not self.done:
            return date.today() > self.deadline
        return False

    # Refresh Task deadline 
    def RefreshDatesByCurrentDate(self) :
        self.Date = date.today()
        self.DayLeftTillDeadline = (self.deadline -self.Date).days
        if self.DayLeftTillDeadline < 0 :
            self.DayLeftTillDeadline = 0
        if "(Late)" not in self.title :
            self.title += "(Late)"
        
    # Set title
    def SetTitle(self) :
        return input("Enter Task Name :")

    # Set Date 
    def SetDate(self) :
        while True: 
            deadline = input("Enter DeadLine Date (yyyy-mm-dd): ")
    
            try:
                deadline = datetime.strptime(deadline, "%Y-%m-%d")
                break 
            except ValueError:
                print("Invalid date format! Please use the format yyyy-mm-dd.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        
        return deadline 

    # operator overloading for Print
    def __str__(self):
        statuse = "\u2717"
        if self.done:
            statuse = "\u2713"

        return f"Title : {self.title:<30} | DeadLine : {str(self.deadline):<8} | Days Left : {self.DayLeftTillDeadline:<5} | State : {statuse:<8}"

    # turn to dic
    def to_dict(self):
        return {
            "title": self.title,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "days left":self.DayLeftTillDeadline,
            "done": self.done
            
        }
# convert from dict
    @classmethod
    def from_dict(cls, d):
        obj = cls.__new__(cls)
        obj.title = d["title"]
        obj.deadline = datetime.strptime(d["deadline"], "%Y-%m-%d").date()
        obj.done = d["done"]
        obj.Date = date.today()
        obj.DayLeftTillDeadline = d["days left"]

        # Ensure we check if the task is late after loading from file
        if obj.DayLeftTillDeadline < 0 and "(Late)" not in obj.title:
            obj.title += " (Late)"
            obj.DayLeftTillDeadline = 0

        return obj

#======= To do list =======

class ToDoList:
    # Constructor
    def __init__(self):
        self.TaskList = []

    # Add Task
    def AddTask(self, TaskName):
        self.TaskList.append(TaskName)

    # Remove Task
    def RemoveTask(self, TaskName):
        self.TaskList.remove(TaskName)

    # Refresh Task list
    def RefreshLateTask(self):
        for task in self.TaskList:
            task.RefreshDatesByCurrentDate()
    
    # Edit Task
    def EditTask(self) :
       print("Select a Task to Edit")
       selected = MenuGenerator(self.TaskList)
       print("What would you like to edit ?")
       options = ["Title" , "Deadline" , "status"]
       select = MenuGenerator(options)
       TaskToEdit = self.TaskList[selected-1]
       if select == 1 :
          TaskToEdit.title = input("Enter a new title : ")
       elif select == 2 :
          TaskToEdit.deadline = TaskToEdit.SetDate().date()
          TaskToEdit.DayLeftTillDeadline = (TaskToEdit.deadline-TaskToEdit.Date).days
          TaskToEdit.RefreshDatesByCurrentDate()
       elif select == 3:
        while True:
            Mark = input("Enter Done or Not Done: ").lower()
            if Mark == "done":
                TaskToEdit.done = True
                break
            elif Mark == "not done":
                TaskToEdit.done = False
                break
            else:
                print("Invalid input. Please enter 'Done' or 'Not Done'.")

        print("Edit completed!")
   
    # Showing Tasks
    def ShowTasks(self):
        
        Refresh()
        print(f"{'Title':<38} | {'Deadline':<21} | {'Days Left':<17} | {'State':<16}")
        print("-" * 99)
        self.RefreshLateTask()
        for task in self.TaskList:
            if not "(Late)" in task.title:
                print(task)
        # print late task in the end of the list
        for task in self.TaskList :
            if "(Late)" in task.title :
                print(task)
  
    # save To file
    def SaveToFile(self, filename="Task.txt"):
        data = [task.to_dict() for task in self.TaskList]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
  
    # Load From the file
    def LoadFromFile(self, filename="Task.txt"):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    data = json.load(f)
                    self.TaskList = [Task.from_dict(d) for d in data]
                except json.JSONDecodeError:
                    self.TaskList = []

    def GetTasks(self):
        return self.TaskList
    

#======= helpful functions =======

#menu generator
def MenuGenerator(options):
    c = 1
    for selections in options:
        print(f"{c}.{selections}")
        c += 1
    selected = int(input(">Enter :"))
    return selected

# refresh terminal
def Refresh(count = 1):
    time.sleep(count)
    os.system("cls" if os.name == "nt" else "clear")

# Command Manager
def CommandManager(MyList) :
    
    selected = MenuGenerator(["Login", "Exit"])
    Refresh()
    # Start The app 
    if selected == 1:
        selected_task = -1
        while selected_task != 6:
            Refresh(1)
            options = [
                "Add Task",
                "Remove Task",
                "Show Task",
                "Mark a Task Done",
                "Edit a Task",
                "Exit",
            ]
            selected_task = MenuGenerator(options)
            # Add Task
            if selected_task == 1:
                MyList.AddTask(Task())
                print("Task Added")
                MyList.SaveToFile()
            # Remove Task
            elif selected_task == 2:
                tasks = [str(task) for task in MyList.GetTasks()]
                task_index = MenuGenerator(tasks)
                MyList.RemoveTask(MyList.GetTasks()[task_index - 1])
                print("Task successfully removed!")
                MyList.SaveToFile()
            # Show Task
            elif selected_task == 3:
                MyList.ShowTasks()
                back = input(">back")
                back = ""
            # Mark Task
            elif selected_task == 4:
                tasks = [str(task) for task in MyList.GetTasks()]
                task_index = MenuGenerator(tasks)
                MyList.GetTasks()[task_index - 1].MarkDone()
                print("Task is marked!")
                MyList.SaveToFile()
            # Edit Task
            elif selected_task == 5 :
               MyList.EditTask()
               MyList.SaveToFile()
    # Exit the app
    elif selected == 2:
        exit(0)


    

# main
def Main():
    MyList = ToDoList()
    MyList.LoadFromFile()
    MyList.RefreshLateTask()
    MyList.SaveToFile()
    CommandManager(MyList)
    MyList.SaveToFile()

Main()
