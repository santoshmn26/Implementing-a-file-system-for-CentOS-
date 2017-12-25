In [1]: # modules imported for this project
import os.path
import datetime
import time
import os
import math	
############################################
In [2]: ```#Classes used 
	# 1. database used to store all the information about the file such as 
		1. filename
		2. size of file
		3. start number of the block
		4. Ending number of the block
		5. total number of blocks
		6. The FCB number
		7. Number of available blocks in the FCB
		8. FCB file number```
############################################
class database():
	def __init__(self):
		self.file_name=''
		self.file_size=None
		self.start_block=''
		self.end_block=''
		self.number_blocks=None
		self.pos=''
		self.fcb=[]
		self.start=None
		self.end=None
		self.database=[]
		self.update_flag=0
		self.availblock=0
		self.pfs_file=''
#######################################################
In [3]: # Functions used in this class
		1. update_fcb_block: Check the existing FCB if the file was altered update the FCB.
		2. Awesome_logic: Function used to create new FCB (PFS) file
		3. add_details: The main function where the details are stored in variable.
		4. save_details: The function where details are stored in the file 'database.txt'
		5. check_space: checking if there are any blocks free in the current FCB
		6. write_details: Adds the content of the input file to the FCB file
		7. show_dir: function used to handle the dir cmd
		8. remove_file: function used to handle r cmd
########################################################
	def update_fcb_block(self):
		check_string="EOF\n"
		d=open("database.txt",'r')
		with open("fcb_1.txt",'r+') as f:
			f.seek(0)
			f.truncate()
			for line in f.readlines():
				if(line.startswith(check_string)):
					for data in d.readlines():
						line=data
						f.write(line)
				f.write(line) 
	def awesome_logic(self,req_block):
		for i in range(1,4):
			file1="fcb_"+str(i)+".txt"
			if(os.path.isfile(file1)):
				pass
			else:
				o=open(file1,'w+')
				self.pfs_file=file1
				o.close()
				break
		self.start_block=1
		self.end_block=self.start_block+req_block-1
	def check_space(self,aspace):
		o=open("database.txt",'r')
		lines=o.readlines()
		line_info=''
		for line in lines:
			if(line.startswith("freespace")):
				line_info=line
				break
		line_info=line_info.split("\t")
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
			s=avail_list[i]
			e=avail_list[i+1]
			f=avail_list[i+2]
			loc=i
			free_mem=e-s+1
			if(aspace<=free_mem):
				done=1
				e1=s+aspace
				break
		if(done==1):
			if(e1>e):
				del avail_list[loc]
				del avail_list[loc]
				del avail_list[loc]
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

			
				
	def add_details(self,fileName,curblock,availblock,pfs_file):
		o=open("database.txt","r")
		lines=o.readlines()
		main_flag=0
		t=os.stat(fileName)
		self.file_size=t.st_size
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
		if(self.file_size<=256):
			self.number_blocks=1
			a_flag=self.check_space(1)
			if(a_flag==0):
				self.start_block=curblock
				self.end_block=curblock+self.number_blocks-1
			else:
				main_flag=1
		else:
			self.number_blocks=math.ceil(self.file_size/256)
			if(self.number_blocks>availblock):
				self.awesome_logic(self.number_blocks)
			else:
				a_flag=self.check_space(self.number_blocks)
				if(a_flag==0):
					self.start_block=curblock
					self.end_block=curblock+self.number_blocks-1
				else:
					main_flag=1
		if(main_flag==0):
			self.availblock=self.availblock-self.number_blocks
		self.save_details()
		self.write_details()
	def update_changes(self):
		check_string=self.file_name
		with open("database.txt",'r+') as k:
			t=k.read()
			k.seek(0)
			for line in t.split('\n'):
				rows_line=line.split("\t")
				if (rows_line[0]!= check_string):
					k.write(line)
			k.truncate()
		with open("database.txt",'a') as f:
			for data in self.database:
				f.write(str(data))
				f.write("\t")
			f.write("\n")
	def save_details(self):
		self.database=[]
		self.database.append(str(self.file_name))	#0
		self.database.append(str(self.file_size))	#1
		self.database.append(str(self.number_blocks))	#2
		self.database.append(str(self.start_block))	#3
		self.database.append(str(self.end_block))	#4
		self.database.append(str(self.pfs_file))	#5
		self.database.append(str(1))
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
			p=open(self.pfs_file,'r')
			y=p.read()
			y=y.replace("\0","")
			p.close()
			p=open(self.pfs_file,'w')
			p.write(y)
			p.close()
			s=os.stat(self.pfs_file)
			x=s.st_size	
			self.start=x
			self.end=self.start+self.file_size-1
#			print(self.start,self.end)
		self.database.append(self.start)
		self.database.append(self.end)			       			
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
			d=open("database.txt","r+")
			lines=d.readlines()
			d.seek(0)
			d.truncate()
			for line in lines:
				if(line.startswith("database")):
					d.write(new_database_data)
				else:
					d.write(line)
			d.close()
			

	def write_details(self,x=' '):
		if(x!=' '):
			file_name=x
		elif(self.update_flag!=1):
			o=open(self.file_name,'r')
			w=open(self.pfs_file,'a')
			for line in o.readlines():
				w.write(line)
			o.close()
			w.close()
			s=os.stat(self.pfs_file)
			size=s.st_size
			o=open(self.pfs_file,'r')
			lines=o.readlines()
			o.close()
			o= open(self.pfs_file,"w")
			for line in lines:
				o.write(line)
			for i in range(size,10240):
				o.write("\0")
	def update_file_size(self,x):
		self.write_details(x)
	def show_dir(self):
		o=open("database.txt",'r')
		temp=''
		lines=o.readlines()
		for line in lines:
			if(line.startswith("database")):
				pass
			elif(line.startswith("freespace")):
				pass
			elif(line.startswith("\n")):
				continue
			else:
				line=line.split("\t")
				if(len(line)>10):
					temp=line[10].replace("\n"," ")
					print(line[0],"\t",line[1]," bytes\t",line[9],"\t",temp)
				else:
					print(line[0],"\t",line[1]," bytes\t",line[9])
				
		o.close()

	def remove_file(self,filename):
		found=0
		o=open("database.txt",'r+')
		line_info=[]
		file_info=""
		for line in o.readlines():
			o.seek(0)
			if(line.startswith(filename)):
				file_info=line
				found=1
				break
		if(found==0):
			print("Error!! File does not exist in the FCB")
			return()
		o.close
		file_info=file_info.split("\t")	
		s=file_info[3]
		e=file_info[4]
		fcb_file=file_info[5]
		f=open(fcb_file,'r')
		r=f.read()
		f.close()
		null_chars=''
		for i in range(int(file_info[7]),int(file_info[8])+1):
			null_chars=null_chars+"@"
		if(int(file_info[7])==0):
			final_res=null_chars+r[int(file_info[8]):]
		else:
			final_res=r[:int(file_info[7])-1]+null_chars+r[int(file_info[8]):]
		f=open(fcb_file,'w')
		f.write(final_res)
		f.close()
		f=open("database.txt",'r+')
		z=f.readlines()
		f.seek(0)
		f.truncate()
		for line in z:
			if(line.startswith("database")):
				f.write(line)
				continue
			elif(line.startswith("freespace")):
				f.write(line)
				continue
			elif(line.startswith(filename)):
				line=line.split("\t")
				new_free_block=line[2]	
			else:
				f.write(line)
		f.close()
		f=open("database.txt",'r+')
		z=f.readlines()
		f.seek(0)	
		f.truncate
		final_space=''
		for line in z:
			if(line.startswith("freespace")):
				x=line[::]
				x=x.split("\t")
				for i in x:
					if((i!="\t")&(i!="\n")):
						final_space=final_space+i+"\t"
				final_space=final_space+str(s)+"\t"+str(e)+"\t"+str(fcb_file[4])+"\t\n"
				f.write(final_space)
			elif(line.startswith("database")):
				line=line.split("\t")
				new_line="database\t"+line[1]+"\t"+str(int(line[2])+int(new_free_block))+"\t"
				f.write(new_line)
				f.write("\n")
			else:
				f.write(line)
		f.close()
	def kill_all(self,filename):
		f=open("database.txt",'r')
		lines=f.readlines()
		f.close()
		f=open("database.txt","w")
		for line in lines:
			if(line.startswith("database")):
				f.write(line)
		f.close()
		cmd_line="rm "+filename
		os.system(cmd_line)
		if(os.path.exists("fcb_2.txt")==True):
			os.system("rm fcb_2.txt")
		x=input("NOTE:No PFS loaded!, enter open PFS file_name to continue:\nPFS>")
		x=x.split(" ")
		if(x[0]!="open"):
			exit(0)
		fcb_file=x[1]+".txt"
		o=open(fcb_file,'w+')
		o=open("database.txt",'w')
		o.write("database\t1\t39\t\nfreespace\t\n")
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
				fcb_file=line[5]
		f.close()
		f=open(fcb_file,'r')
		full_string=f.read()
	#	print(full_string[start:end])
		f.close()
		try:
			f=open(path,'w+')
			f.write(full_string[start:end])
			f.close()
		except:
			print("Error copying file\nFile already exists")
	def run_vi(self,filename):
		res="vi "+str(filename)
		os.system(res)
	def append_newdata(self,filename,content):
		o=open("database.txt",'r')
		lines=o.readlines()
		file_info=[]
		for line in lines:
			if(line.startswith(filename)):
				line=line.split("\t")
				file_info=line
		o.close()
		x=''
		for c in content:
			x=x+c
		o=open(file_info[5],'r')
		full_file=o.read()
		s=int(file_info[7])
		e=int(file_info[8])
		string_content=''
		for i in content:
			string_content=string_content+i
		new_end=len(string_content)+int(file_info[8])
		res=full_file[:s]+full_file[s:e]+x+full_file[e:]
		o.close()
		new_line=''
		for data in range(len(file_info)):
			if(data == 8):
				new_line=new_line+str(new_end)+"\t"
			elif(data==9):
				new_line=new_line+file_info[data]
			elif(file_info[data]=="\n"):
				new_line=new_line+"\t"
				continue
			else:
				new_line=new_line+file_info[data]+"\t"
		o=open("database.txt",'r+')
		flag=0
		for line in lines:
			if(line.startswith("database")):
				o.write(line)
				continue
			elif(line.startswith("freespace")):
				o.write(line)
				continue
			if(line.startswith(filename)):
				o.write(new_line)
				flag=1
				continue
			if(flag==1):
				line=line.split("\t")
				new_start=int(line[7])+len(string_content)
				new_end=int(line[8])+len(string_content)
				new_line=''
				for data in range(len(line)):
					if(line[data]=="\n"):
						o.write("\n")
						break
					elif(data==9):
						new_line=new_line+line[data]+"\t"
					elif(data==7):
						new_line=new_line+str(new_start)+"\t"
					elif(data==8):
						new_line=new_line+str(new_end)+"\t"
					else:
						new_line=new_line+line[data]+"\t"
				o.write(new_line)
			else:
				o.write(line)
		o.write("\n")
		o.close()
		o=open(file_info[5],'r+')
		lines=o.readlines()
		o.write(res)
		o.close()
		k=os.stat(file_info[5])
		size=k.st_size
		o=open(file_info[5],'w')
		o.write(res)
		for i in range(size,10240):
			o.write("\n")
		o.close()
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
				fcb_file=line[5]
				for i in line:
					if(i!="\n"):
						new_line=new_line+i+"\t"
				new_line=new_line+remarks_string
				f.write(str(new_line))
				f.write("\n")
			else:
				f.write(line)
		f.close()
		o=open(fcb_file,"a")
		o.write(remarks_string)
		o.close()
		self.update_file_size(remarks_string)

should_run=1
x=input("PFS>")
x=x.split(" ")
if(x[0]!="open"):
	print("ERROR NO PFS file")
	exit(1)
else:
	pfs_file=x[1]+".txt"
	if(os.path.isfile(pfs_file)):
		pass
	else:
		o=open("fcb_1.txt","w+")
		o.close()
		f=open("database.txt","w+")
		f.write("database\t1\t39\t\nfreespace\t\n")
		f.close()
list_of_objects=[]
obj=database()
while(should_run==1):
	x=input("PFS>")
	if(x=="dir"):
		obj.show_dir()
	x=x.split(" ")
	if(x[0]=="exit"):
		should_run=0
	if(x[0]=="rm"):
		filename=x[1]+".txt"
		if(os.path.exists(filename)):
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
		obj.append_remarks(filename,remarks)
	elif(x[0]=="run"):
		filename=x[1]+".txt"
		if(os.path.exists(filename)==False):
			print("Invalid File, File does not exists in the FCB")
			continue
		obj.run_vi(filename)
	elif(x[0]=="putc"):
		filename=x[1]+".txt"
		if(os.path.exists(filename)==False):
			print("Invalid File, File does not exists in the FCB")
		content=x[2:]
		obj.append_newdata(filename,content)
