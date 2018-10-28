import os
import stat
import time
import subprocess
should_run=1
i=1
list_cmd=list()
executable = stat.S_IEXEC 	#check all the list of executable in the current dir
for filename in os.listdir('.'):
        if os.path.isfile(filename):
                st = os.stat(filename)
                mode = st.st_mode
                if executable:
                        if(filename[0]!='.'):
                                if os.access(filename,os.X_OK):
                                        list_cmd.append(filename)	#adding all the list of exe files into a list
print(list_cmd)
while(should_run):
        try:    # try to handle exception if user inputs invalid inputs
                x=input("ubos>")        # taking input to execute excvp
                if (x=='selection'):    # checking if the user typed selection 
                        print("----------------------------------------")
                        print("Select from the list of Executables")
                        for j in list_cmd:      # print all the list of executable files in the current dir
                                print(i,"-->",j)        # prints all the list of executable files
                                i+=1
                        print("----------------------------------------")
                        choice = int(input("Please select a choice: ")) # input the choice for the selection
                        if(choice<1):                                   # checking for invalid choices 
                                print("Ivalid Choice selected")
                                continue                                # continue if the user types invalid inputs
                        else:
                                print("Selected to execute ",choice,"-->", list_cmd[choice-1])
                        print("----------------------------------------")
                        print("Exectuing Choice...",choice)
                        if('.py' in list_cmd[choice-1]):                # executable .py files
                                var=list()
                                var.append('python')
                                var.append(list_cmd[choice-1])
                                x=subprocess.Popen(var)
                                time.sleep(1)
		   		 x.terminate()
                        else:
                                var='./' + list_cmd[choice-1]           # handling .out files that are executable
                                subprocess.call(var)                    # calling subprocess to execute the command
                        x,i="",1
                        continue
                elif(x=="exit"):
                        break   #breaks the loop when the input command is exit
                else:
                        z=x.split(" ") # else the given command must be split based on spaces and loaded into list
                pid=os.fork()           # fork is created
                if(pid<0):
                        print("Fork Failed") #prints that the fork is failed if obtained pid <0
                if(pid==0):
                        subprocess.call(z)  #call the execvp and execute the command in the list z
                        print("Child Process Created") # prints that the child process is completed
                else:
                        os.waitpid(pid,0)               #wait till the parent process is completed
                        should_run=-1
                        print("Parent Process Created")
                        break
        except:
                print("Invalid Input")
                                                               
