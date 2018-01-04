Source code for FCB
import os.path 
import datetime
import time
import os
import math	

class database():			# main class to manage all values
	def __init__(self):
		self.file_name=''	# file name 
		self.file_size=None	# the size of the file
		self.start_block=''	# the first block the file occupies
		self.end_block=''	# the last block the file occupies
		self.number_blocks=None # the total number of blocks
		self.pos=''		# pos in the fcb file for the file
		self.no_of_lines=None	# total no of lines in the file
		self.fcb=[]		# to manage the total pfs created
		self.start=None		# starting of the file in the pfs
		self.end=None		# ending of the file in the pfs
		self.database=[]		# to manage the total number of files
		self.update_flag=0	# to manage changes in the file
		self.availblock=0	# to check if the blocks are available
		self.pfs_file=''		# which pfs file does the file belong 

	def awesome_logic(self):	# main logic to create new fcb files
		for i in range(1,4):
			file1="fcb_"+str(i)+".txt"	# adding the number to file
			if(os.path.isfile(file)): # checking if the file exists
				pass
			else:
				o=open(file1,'w+') # if file does not exists then creating a new file
				self.pfs_file=file1
				o.close()
#This check space function is used to check if there are any free blocks available in the current fcb
def check_space(self,aspace):
		o=open("database.txt",'r')
		lines=o.readlines() # reading all the lines in the file
		line_info='' 	
		for line in lines:
			if(line.startswith("freespace")): # this line holds the free space
				line_info=line
				break
		line_info=line_info.split("\t") # split the lines based on the “\t” tag
		temp_list=line_info[1:]
		if(len(temp_list)==0):
			return(0)
		avail_list=[]
		s,e,f,loc,e1,done=0,0,0,0,0,0
		for i in temp_list:
			if(i!="\n")&(i!=""):
				avail_list.append(int(i))
		new_list=[]
		for i in range(0,len(avail_list),3):
			s=avail_list[i]    # starting of the free address
			e=avail_list[i+1]	# ending of the free address
			f=avail_list[i+2]	# total free of the address
			loc=i
			free_mem=e-s+1		# free memory in the address
			if(aspace<=free_mem):	# check memory
				done=1	
				e1=s+aspace	# new end space
				break
		if(done==1):
			if(e1>e):
				del avail_list[loc] # delete the avail list
				del avail_list[loc]	# delete the next one
				del avail_list[loc] # delete the last one
			else:
				for i in range(len(avail_list)):
					if(i==loc):
						new_list.append(e1)
					else:
						new_list.append(avail_list[i])
				avail_list=new_list
		if(done==1):
			o=open("database.txt",'r+')
			lines=o.readlines()
			o.seek(0)
			o.truncate()
			for line in lines:
				if(line.startswith("freespace")):
					o.write("freespace\t")
					for i in avail_list:
						temp=str(i)+"\t"
						o.write(temp)
					o.write("\n")
				else:
					o.write(line)
			self.start_block=s
			if(e1>e):
				self.end_block=s
			else:
				self.end_block=e1-1
			return(1)			
		return(0)		
				
	# this is the main function that updates all the values to the file that are declared in the init block
	def add_details(self,fileName,curblock,availblock,pfs_file): 
		o=open("database.txt","r")
		lines=o.readlines() # read all the lines
		t=os.stat(fileName)
		self.file_size=t.st_size  # store the file size
		self.file_name=fileName
		for line in lines:
			if(line.startswith(fileName)):
				line=line.split("\t")
				if(int(line[1])!=int(self.file_size)):	
					self.update_changes()
					return(0)
				return(0)
		self.availblock=availblock
		self.pfs_file=pfs_file
		if(self.file_size<=256):  # does it require one block?
			self.number_blocks=1
			self.start_block=curblock
			self.end_block=curblock+self.number_blocks-1
		else:
			self.number_blocks=math.ceil(self.file_size/256) # more than one block use ceil function to round of number of blocks required.
			if(self.number_blocks>availblock):
				self.awesome_logic()
			else:
				self.start_block=curblock
				self.end_block=curblock+self.number_blocks-1
		self.availblock=self.availblock-self.number_blocks
		self.save_details()
		self.write_details()

	def update_changes(self): # update any changes made in the file before loading the pfs file
		check_string=self.file_name
		with open("database.txt",'r+') as k:
			t=k.read()
			k.seek(0)
			for line in t.split('\n'): split each value form the database into list for easier access
				rows_line=line.split("\t") # split is based on ‘\t’ as was store in the database file
				if (rows_line[0]!= check_string): # if found the required file
					k.write(line)
			k.truncate() # remake file
		with open("database.txt",'a') as f: # append the values to the file
			for data in self.database:
				f.write(str(data))
				f.write("\t")
			f.write("\n")
# save the details into the file database 
	def save_details(self):
		self.database=[]
		self.database.append(str(self.file_name))	#0
		self.database.append(str(self.file_size))	#1
		self.database.append(str(self.number_blocks))	#2
		self.database.append(str(self.start_block))	#3
		self.database.append(str(self.end_block))	#4
		self.database.append(str(self.pfs_file))	#5
		self.database.append(str(1))
# above numbers indicate the value of the list for easier access from the database file.
		#Calculating date	
		x=datetime.datetime.now()
		x=str(x)
		t,k=0,''
		if(int(x[11:13])==0):
			t=12
		elif(int(x[11:13])>12):
			t=int(x[11:13])-12
			k=" PM "
		elif(int(x[11:13])<=12):
			k=" AM "
			t=x[11:13]
		res_date=str(t)+x[13:16]+k+"Decemeber "+x[8:10]
		if(self.update_flag==0):
			p=open("fcb_1.txt",'r')
			y=p.read()
			y=y.replace("\0","")
			p.close()
			p=open("fcb_1.txt",'w')
			p.write(y)
			p.close()
			s=os.stat("fcb_1.txt")
			x=s.st_size	
			self.start=x
			self.end=self.start+self.file_size-1
#			print(self.start,self.end)
		self.database.append(self.start) # append the start value for the file info.
		self.database.append(self.end)	# append the end value for the file info.	       			
		self.database.append(res_date)
		if(self.update_flag!=1):
			d=open('database.txt',"a")
#			print("adding data!!!!")
			for data in self.database:
				d.write(str(data))
				d.write("\t")
			d.write("\n")
			d.close()
			new_database_data="database\t"+str(int(self.end_block)+1)+"\t"+str(self.availblock)+"\n"
# get the new line to add to the file
			d=open("database.txt","r+")
			lines=d.readlines()
			d.seek(0)
			d.truncate()
			for line in lines:
				if(line.startswith("database")): # update the database line with the new block values.
					d.write(new_database_data)
				else:
					d.write(line)
			d.close()
			
# this function writes are the variables to a file called database to manage the files
	def write_details(self,x=' '):
		if(x!=' '):
			file_name=x
		elif(self.update_flag!=1):
			o=open(self.file_name,'r')
			w=open("fcb_1.txt",'a')
			for line in o.readlines():
				w.write(line)
			o.close()
			w.close()
			s=os.stat("fcb_1.txt")
			size=s.st_size # get the file size of the file
			o=open("fcb_1.txt",'r')
			lines=o.readlines() # read the line in the file
			o.close()
			o= open("fcb_1.txt","w")
			for line in lines:
				o.write(line)
			for i in range(size,10240): # convert the file into 10240 size with the help of null characters.
				o.write("\0")
	def update_file_size(self,x): # after appending the remarks if the file size increases then update the file size to new size.
		self.write_details(x)

	def show_dir(self): # function to handle the dir command
		o=open("database.txt",'r')
		temp=''
		lines=o.readlines()
		for line in lines:
			if(line.startswith("database")): # ignore if the line starts with database
				pass
			elif(line.startswith("freespace")): # ignore if the line starts with freespace
				pass
			elif(line.startswith("\n")): # ignore if the line starts with ‘\n’
				continue
			else:
				line=line.split("\t") # else write all the contents into the file as a new file.
				if(len(line)>10):
					temp=line[10].replace("\n"," ")
					print(line[0],"\t",line[1]," bytes\t",line[9],"\t",temp)
				else:
					print(line[0],"\t",line[1]," bytes\t",line[9])
				
		o.close()

	def remove_file(self,filename):
		o=open("database.txt",'r+')
		line_info=[]
		file_info=""
		for line in o.readlines():
			o.seek(0)
			if(line.startswith(filename)):
				file_info=line
				break
		o.close
		file_info=file_info.split("\t")	
		s=file_info[3]  # the starting block number
		e=file_info[4]	# the ending block number
		f=open("fcb_1.txt",'r')
		r=f.read()
		f.close()
		null_chars=''
		for i in range(int(file_info[7]),int(file_info[8])+1):
			null_chars=null_chars+"@"
		if(int(file_info[7])==0):
			final_res=null_chars+r[int(file_info[8]):]
		else:
			final_res=r[:int(file_info[7])-1]+null_chars+r[int(file_info[8]):] 	# appends null chars to the file to manage the file size to be 10240
		f=open("fcb_1.txt",'w')
		f.write(final_res)
		f.close()
		f=open("database.txt",'r+')
		z=f.readlines()
		f.seek(0)
		f.truncate() # remake the entire file
		for line in z:
			if(line.startswith("database")): # write the database file back
				f.write(line)
				continue
			elif(line.startswith("freespace")): # write the freespace file back
				f.write(line)
				continue
			elif(line.startswith(filename)): 	# check if there is the file info 
				line=line.split("\t")
				new_free_block=line[2]	
			else:
				f.write(line)		# ELSE write the line
		f.close()
		f=open("database.txt",'r+')
		z=f.readlines()
		f.seek(0)	
		f.truncate
		final_space=''
		for line in z:
			if(line.startswith("freespace")): #update the freespcace file
				x=line[::]
				x=x.split("\t")
				for i in x:
					if((i!="\t")&(i!="\n")):
						final_space=final_space+i+"\t"
				final_space=final_space+str(s)+"\t"+str(e)+"\t\n"
				f.write(final_space)
			elif(line.startswith("database")):
				line=line.split("\t")
				new_line="database\t"+line[1]+"\t"+str(int(line[2])+int(new_free_block))+"\t"
	# new_line is the line to be added to the database.txt file to update the new file info
				f.write(new_line)
				f.write("\n")
			else:
				f.write(line)
		f.close()
# function to manage the kill command
	def kill_all(self,filename):
		f=open("database.txt",'r')
		lines=f.readlines()
		f.close()
		f=open("database.txt","w")
		for line in lines:
			if(line.startswith("database")):
				f.write(line)
		f.close()
		cmd_line="rm "+filename # system command to remove the file
		os.system(cmd_line)
		x=input("NOTE:No PFS loaded!, enter open PFS file_name to continue:\nPFS:") # if there is no pfs file to, we cannot manage the data hence open a new pfs file.
		x=x.split(" ")
		if(x[0]!="open"): check if the command is open else exit
			exit(0)
		fcb_file=x[1]+".txt"
		o=open(fcb_file,'w+')
		o=open("database.txt",'w') # rewrite the database with new blocks
		o.write("database\t1\t39\t\nfreespace\t\n") # initialize the free space
		o.close()
	def copy_file(self,filename):
		path="/home/santoshmn26/Project/"+filename
		f=open("database.txt",'r')
		lines=f.readlines()
		f.close()
		for line in lines:
			if(line.startswith(filename)):
				line=line.split("\t")
				start=int(line[7])
				end=int(line[8])
		f.close()
		f=open("fcb_1.txt",'r')
		full_string=f.read()
	#	print(full_string[start:end])
		f.close()
		try: # try to open the file 
			f=open(path,'w+')
			f.write(full_string[start:end])
			f.close()
		except: # executes if the file already exists in the copying path
			print("Error copying file\nFile already exists")

	def append_remarks(self,filename,remarks):
		remarks_string=''
		for i in remarks:
			remarks_string=remarks_string+i+" "
		f=open("database.txt",'r+')
		z=f.readlines()
		f.seek(0)
		f.truncate
		new_line=''
		for line in z:
			if(line.startswith(filename)):
				line=line.split("\t")
				fcb_no=line[5]
				for i in line:
					if(i!="\n"):
						new_line=new_line+i+"\t"
				new_line=new_line+remarks_string
				f.write(str(new_line))
				f.write("\n")
			else:
				f.write(line)
		f.close()
		o=open("fcb_1.txt","a")
		o.write(remarks_string)	# append the remarks_string to the file
		o.close()
		self.update_file_size(remarks_string)

should_run=1 # make it infinite loop to run until command ‘exit’
x=input("PFS>")
x=x.split(" ") 	# split the input to command and the text file name
if(x[0]!="open"):
	print("ERROR NO PFS file")
	exit(1)
else:
	pfs_file=x[1]+".txt"
	if(os.path.isfile(pfs_file)): 	# check if the pfs file exists 
		pass
	else:
		o=open("fcb_1.txt","w+") 	# file does not exists? Then create
		o.close()
		f=open("database.txt","w+") # 
		f.write("database\t1\t39\t\nfreespace\t\n")
		f.close()
list_of_objects=[] #objects for each file manages in this list
obj=database()
while(should_run==1): # infinite loop of commands
	x=input("PFS>")
	if(x=="dir"):    # manage command Dir to list all files
		obj.show_dir()
	x=x.split(" ")
	if(x[0]=="exit"):
		should_run=0
#all the below print statements are executed if the file name entered does not exists in the pfs
	if(x[0]=="rm"):   # manage the remove command
		filename=x[1]+".txt"
		if(os.path.exists(filename)): # check if the file exists to remove
			obj.remove_file(filename)
			continue
		else:
			print("Invalid File, File does not exists in the FCB")
	elif(x[0]=="kill"):
		filename=x[1]+".txt"
		if(os.path.exists(filename)==False):
			print("Invalid File,PFS File does not exists")
		else:
			obj.kill_all(filename)
	elif(x[0]=="get"):
		filename=x[1]+".txt"
		if(os.path.exists(filename)==False):
			print("Invalid File, File does not exists in the FCB")
		else:
			obj.copy_file(filename)
	elif(x[0]=="put"):
		filename=x[1]+".txt"
		if(os.path.exists(filename)==False):
			print("Invalid File, File does not exists in the FCB")
			continue
		o=open("database.txt")
		lines=o.readlines()
		for line in lines:
			line=line.split("\t")
			if(line[0]=="database"):
				curblock=int(line[1])
				availblock=int(line[2])
		o.close()
		x=obj.add_details(filename,curblock,availblock,pfs_file)
		list_of_objects.append(obj)
	elif(x[0]=="putr"):
		remarks=x[2:]
		filename = x[1]
		obj.append_remarks(filename,remarks) # call function to append remarks to database file.


