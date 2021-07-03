## Create Your First Task!

1. git clone

2. go to folder `execution file`

3. enter`./taskman -w  first_task`

4. a task names `first_task` will be created for today

   ```
   task first_task added to 20210703 with ind = 43
   (0.0041s)
   ```

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
   ```