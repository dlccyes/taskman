import sys
import json

from datetime import date, datetime, timedelta

from random import randint

import time


# class
# load tasks
try: # if there's tasks.txt
    with open('tasks.txt', "r", encoding='utf-8') as tasks:
        taskdict = json.load(tasks)

except: # if no file
    with open('tasks.txt', 'w', encoding='utf-8') as tasks:
        json.dump({}, tasks)
    with open('tasks.txt', "r", encoding='utf-8') as tasks:
        taskdict = json.load(tasks)

today = date.today()
todaystr = today.strftime('%Y%m%d')

class ansi:
    bg_green = '\033[48;2;70;156;81m'
    bg_yellow = '\033[48;2;249;249;90m'
    bg_red = '\033[48;2;255;0;0m'
    bg_black = '\033[48;2;0;0;0m'

    fg_black = '\033[38;2;0;0;0m'
    fg_white = '\033[38;2;255;255;255m'
    fg_yellow = '\033[38;2;250;241;190m'
    fg_orange = '\033[38;2;255;202;154m'
    fg_green = '\033[38;2;50;216;81m'

    underline = '\033[4m'

    reset = '\033[0m'


available_commands = 'available commands:\n\
    -s (num_of_days)     : show tasks in X day (show all if nothing passed)\n\
    -d index (date)      : delete [index] (in [date])\n\
    -w task_name (date)  : write [task_name] in [date (default to today)]\n\
    -ds index (date)     : delete and show\n\
    -ws task_name (date) : write and show\n\
    -a index msg         : alter the description of the indexed task\n\
    -u index msg         : update task i.e. append msg to the indexed task\n\
    -cd index date       : change task to given date\
    '


class errormsg:
    nothingdeleted = f'{ansi.bg_yellow}{ansi.fg_black}No match. Nothing deleted.{ansi.reset}\n'
    wrongdate = f'{ansi.bg_yellow}{ansi.fg_black}Wrong date. Nothing deleted.{ansi.reset}\n'
    wrongcommand = f'{ansi.bg_yellow}{ansi.fg_black}Wrong command. Nothing happened.{ansi.reset}\n{ansi.fg_white}{available_commands}{ansi.reset}\n'
    nocommand = f'{ansi.bg_yellow}{ansi.fg_black}No command passed. Nothing happened.{ansi.reset}'
    notinteger = f'{ansi.bg_red}{ansi.fg_white}Please enter an integer{ansi.reset}\n'
    datedontexist = f'{ansi.bg_yellow}{ansi.fg_black}The date does not exist.{ansi.reset}\n'

weekday_dict = {0:'Mon.',1:'Tue.',2:'Wed.',3:'Thur.',4:'Fri.',5:'Sat.',6:'Sun.'}

def show():
    # global taskdict
    cont = True
    mode = 'show'
    if len(sys.argv) == 3: # task -s xxxx
        if sys.argv[2].isnumeric() == False:
            print(errormsg.notinteger)
            mode = 'err'
        else:
            if len(sys.argv[2]) == 8: #task -s 20210420
                mode = 'showdate'
            else:
                mode = 'show'
                #print(errormsg.datedontexist)
               # mode = 'err'
    else: # -ws -ds
        pass

    if mode == 'showdate':
        # datee = datetime.strptime(sys.argv[2], '%Y%m%d')
        datee = sys.argv[2]
        cont = True
        try:
            datee_date = datetime.strptime(datee, '%Y%m%d')
        except ValueError:
            print(errormsg.datedontexist)
            cont = False
        if cont == True:
            print(f'{ansi.underline}{datee} W{datee_date.isocalendar()[1]-7} {weekday_dict[datee_date.weekday()]}{ansi.reset}\n')
            try:
                for tasknum in list(taskdict[datee].keys()): #taskkdict[datee] is a dict 
                    print(f'    ({tasknum}) {taskdict[datee][tasknum]}\n')
            except KeyError: # if no date
                print('nothing\n')

    elif mode == 'show':
        # show past 
        dates = list(taskdict.keys())
        dates.sort()
        count = 0
        for datee in dates:
            datee_date = datetime.strptime(datee, '%Y%m%d')
            today_date = datetime.strptime(todaystr, '%Y%m%d')
            date_diff = (datee_date - today_date).days
            if sys.argv[1] == '-s' and len(sys.argv) == 3:
                if date_diff > int(sys.argv[2]):
                    break 
            if date_diff == 0:
                msg = f'{ansi.bg_red}{ansi.fg_white} 🖕🖕🖕 TODAY 🤯🤯 {ansi.reset}'
            elif date_diff > 0 and date_diff <= 3:
                msg = f'{ansi.bg_yellow}{ansi.fg_black} {date_diff} day {ansi.reset}'
            elif date_diff > 3:
                msg = f'{ansi.bg_green}{ansi.fg_black} {date_diff} day {ansi.reset}'
            else: # past
                msg = f'{ansi.bg_red}{ansi.fg_white} 😡😡😠😡😠 {date_diff} day 😠😡😠😡😡 {ansi.reset}'
            print(msg)
            print(f'{ansi.underline}{datee} W{datee_date.isocalendar()[1]-7} {weekday_dict[datee_date.weekday()]}{ansi.reset}\n')
            for tasknum in list(taskdict[datee].keys()): #taskkdict[datee] is a dict 
                print(f'    ({tasknum}) {taskdict[datee][tasknum]}\n')
            count += 1
    elif mode == 'err':
        pass

def alter(): 
    """alter the task description"""
    for datee in list(taskdict.keys()): # datee: keys of a dict i.e. date, where values are also dicts
        if list(taskdict[datee]).count(sys.argv[2]) > 0: # taskdict[datee]: keys i.e. indexes → found the date
            taskmsg = taskdict[datee][sys.argv[2]]
            taskmsg_altered = sys.argv[3]
            taskdict[datee][sys.argv[2]] = taskmsg_altered
            print(f'task {ansi.fg_yellow}{taskmsg}{ansi.reset} from {ansi.underline}{datee}{ansi.reset} altered to {ansi.fg_yellow}{taskmsg_altered}{ansi.reset}')
            break
    
    with open('tasks.txt', "w", encoding='utf-8') as tasks:
        json.dump(taskdict, tasks)

def update(): 
    """append text to the task description"""
    for datee in list(taskdict.keys()): # datee: keys of a dict i.e. date, where values are also dicts
        if list(taskdict[datee]).count(sys.argv[2]) > 0: # taskdict[datee]: keys i.e. indexes → found the date
            taskmsg = taskdict[datee][sys.argv[2]]
            taskmsg_updated = taskmsg + f' {sys.argv[3]}'
            taskdict[datee][sys.argv[2]] = taskmsg_updated
            print(f'task {ansi.fg_yellow}{taskmsg}{ansi.reset} from {ansi.underline}{datee}{ansi.reset} altered to {ansi.fg_yellow}{taskmsg_updated}{ansi.reset}')
            break
    
    with open('tasks.txt', "w", encoding='utf-8') as tasks:
        json.dump(taskdict, tasks)

def changeDate():
    input_idx = sys.argv[2]
    input_date = sys.argv[3]
    for datee in list(taskdict.keys()): # datee: keys of a dict i.e. date, where values are also dicts
        if list(taskdict[datee]).count(input_idx) > 0: # taskdict[datee]: keys i.e. indexes → found the date
            taskmsg = taskdict[datee][input_idx]
            taskdict[datee].pop(input_idx)
            if(input_date not in taskdict):
                taskdict[input_date] = {}
            taskdict[input_date][input_idx] = taskmsg
            print(f'task {ansi.fg_yellow}{taskmsg}{ansi.reset} from {ansi.underline}{datee}{ansi.reset} altered to {ansi.underline}{input_date}{ansi.reset}')
            break

    with open('tasks.txt', "w", encoding='utf-8') as tasks:
        json.dump(taskdict, tasks)

def delete():
    # global taskdict
    try:
        if sys.argv[2] == '.': #wtf is this
            taskdict.pop(sys.argv[3])
        elif len(sys.argv) == 4: # if have argv 3 i.e. date is given, basically obsolete
            targetdate = taskdict[sys.argv[3]]
            try:
                taskdict[sys.argv[3]].pop(sys.argv[2])
            except:
                print(errormsg.nothingdeleted)
        else: # if no argv 3 i.e. no date given → search through all the dates
            for datee in list(taskdict.keys()): # datee: keys of a dict i.e. date, where values are also dicts
                if list(taskdict[datee]).count(sys.argv[2]) > 0: # taskdict[datee]: keys i.e. indexes → found the date
                    target = taskdict[datee].pop(sys.argv[2]) # found & pop
                    print(f'task {ansi.fg_yellow}{target}{ansi.reset} from {ansi.underline}{datee}{ansi.reset} deleted')
                    if len(taskdict[datee]) == 0: # delete the date if vacuum 
                        taskdict.pop(datee)
                        # print(f'date {ansi.fg_yellow}{datee}{ansi.reset} deleted')    
                    break
                elif datee == list(taskdict.keys())[-1]:
                    print(errormsg.nothingdeleted)
    except KeyError:
        print(errormsg.wrongdate)
    with open('tasks.txt', "w", encoding='utf-8') as tasks:
        json.dump(taskdict, tasks)

def write():
    # global taskdict
    cont = True
    if len(sys.argv) == 3:
        taskdate = todaystr
    elif len(sys.argv) == 4:
        try:
            taskdate = datetime.strptime(sys.argv[3], '%Y%m%d')
            taskdate = taskdate.strftime('%Y%m%d')
        except:
            print('small pp :(') # not a date
            cont = False
    else:
        print('idiot 🥵🥵') # too many inputs
        cont = False

    if cont == True:
        try: # if date already existed then nothing happened
            temp = taskdict[taskdate]
        except: # if the date isn't initiated i.e. date doesn't existed
            taskdict[taskdate] = {}

        indexlist = [ind for datee in list(taskdict.keys()) for ind in list(taskdict[datee].keys())]  
        index = randint(10,99) # generate random index, for formatting concern, only generate two-digit
        while str(index) in indexlist: # avoid index collision
            index = randint(10,100)
        taskdict[taskdate][index] = sys.argv[2]
        
        with open('tasks.txt', "w", encoding='utf-8') as tasks:
            json.dump(taskdict, tasks)
        print(f'task {ansi.fg_yellow}{sys.argv[2]}{ansi.reset} added to {ansi.underline}{taskdate}{ansi.reset} with ind = {index}')
    else:
        pass




t0 = time.time()
try:
    if sys.argv[1] == '-s': # show
        show()
    elif sys.argv[1] == '-d': # delete # argv 2: index to delete, argv 3: date (or no)
        delete()
    elif sys.argv[1] == '-w': # write
        write()
    elif sys.argv[1] == '-ds': # delete and show
        delete()
        show()
    elif sys.argv[1] == '-ws': # write and show
        write()
        show()
    elif sys.argv[1] == '-a':
        alter()
    elif sys.argv[1] == '-u':
        update()
    elif sys.argv[1] == '-cd':
        changeDate()
    else:
        print(errormsg.wrongcommand)

except IndexError:
    print(errormsg.wrongcommand)

# time.sleep(1)
te = time.time()
print(f'({round(te-t0,4)}s)')
