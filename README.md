## Create Your First Task!

1. git clone

2. go to folder `execution file`

3. enter`./taskman -w  first_task`  
   (alt: just stay at the top folder and enter `python3 taskman.py -w first_task`)

4. a task named `first_task` will be created for today, storing in a txt file named `tasks.txt`

   ```
   task first_task added to 20210703 with ind = 43
   (0.0041s)
   ```
tips: you can add alias to you `~/.bash_aliases` to use this more conveniently  
e.g. if you clone this to `~/github`, you can add `alias task="cd ~/github/taskman/'execution file' && ./taskman"` to `.bash_aliases`, after that, you can `task -w sometask` to create tasks

## Show Tasks
### Show all tasks
`./taskman -s `
### Show tasks of a specific date
`./taskman -s [date]`  
e.g. `./taskman -s 20210704` → show tasks in 2021.7.4
### Show tasks within X days
`./taskman -s [num]`  
e.g. `./taskman -s 3` → show tasks within 3 days

## Delete Tasks
`./taskman -d [index]`

## Create Tasks
`./taskman -w [contents] [date]`  
e.g. `./taskman -w do_homework 20210706`  

omitting `[date]` will automatically create for today 


## Show All the Commands

Any misuse of commands starting with `./taskman` will show all the available commands.  
e.g. 

1. `./taskman` 

2. ```
   Wrong command. Nothing happened.
   available commands:
       -s (num_of_days)     : show tasks in X day (show all if nothing passed)
       -d index (date)      : delete [index] (in [date])
       -w task_name (date)  : write [task_name] in [date (default to today)]
       -ds index (date)     : delete and show
       -ws task_name (date) : write and show
       -a index msg         : alter the description of the indexed task
       -u index msg         : update task i.e. append msg to the indexed task
       -cd index date       : change task to given date
   ```

## demo
assuming that you download the execution file in `/mnt/c/taskman`
![Image](https://i.imgur.com/t1igxsq.png)   
![Image](https://i.imgur.com/Y4tojok.png)
![Image](https://i.imgur.com/4jf6ZzK.png)
![Image](https://i.imgur.com/UYXB3jM.png)
![Image](https://i.imgur.com/2WV730s.png)