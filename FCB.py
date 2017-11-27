import os.path
import time
import os
import math
class database():
	def __init__(self):
		self.file_name=''
		self.file_size=None
		self.start_block=''
		self.end_block=''
		self.number_blocks=None
		self.pos=''
		self.no_of_lines=None
		self.fcb=[]
		self.start=None
		self.end=None
		self.eof=None
		self.database=[]
		self.update_flag=0
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
	def add_details(self,fileName,curblock,availblock):
		self.file_name=fileName
		z=os.stat(fileName)
		x=z.st_size
		self.file_size=x
		if(x<=256):
			self.number_blocks=1
			self.start_block=curblock
			self.end_block=curblock+self.number_blocks-1
		else:
			self.number_blocks=math.ceil(x/256)
			if(self.number_blocks>availblock):
				pass
			else:
				self.start_block=curblock
				self.end_block=curblock+self.number_blocks-1
		availblock=availblock-self.number_blocks
		self.fcb.append(availblock)
	#	self.update_fcb_block()
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
		self.database.append(str(self.file_name))
		self.database.append(str(self.file_size))
		self.database.append(str(self.number_blocks))
		self.database.append(str(self.start_block))
		self.database.append(str(self.end_block))
		self.database.append(str(self.pos))
		self.database.append(str(self.no_of_lines))
		self.database.append(str(1))
		k=open('database.txt',"r")
		match=0
		list_of_rows=[]
		for row in k.readlines():
			list_of_rows=row.split("\t")
			if(list_of_rows[0]==self.file_name):
				print("----------------------")
				if(str(list_of_rows[1])==str(self.file_size)):
					self.update_flag=1
					print("file exists")
					break
				else:	
					print("file exists needs update")
					self.update_flag=1
					self.update_changes()
					break

		if(self.update_flag==0):
			s=os.stat("fcb_1.txt")
			x=s.st_size	
			self.start=x
			self.end=self.start+self.file_size
			print(self.start,self.end)
			       		
		k.close()
		if(self.update_flag!=1):
			d=open('database.txt',"a")
			print("adding data!!!!")
			for data in self.database:
				d.write(str(data))
				d.write("\t")
			d.write("\n")
			d.close()


	def write_details(self):
		if(self.update_flag!=1):
			o=open(self.file_name,'r')
			w=open("fcb_1.txt",'a')
			for line in o.readlines():
				w.write(line)
			o.close()
			w.close()
			print("Successfully added to FCB")
		else:
			print("file already exists")
	


print("Executing file system FCB..")
time.sleep(0.8)
print("checking if a FCB file exists")
filename='fcb_1.txt'
if(os.path.isfile(filename)):
	print("FileFound")
	time.sleep(0.8)
	print("loading the FCB file")
	time.sleep(0.8)
else:
	print("File not found")
	time.sleep(0.8)
	print("Creating a new FCB file")
	time.sleep(0.8)
	#os.system("dd if=/dev/zero of=fcb_1.txt bs=1 count=1")
	c=open("fcb_1.txt",'w+')
	c.close()
	time.sleep(0.8)
	print("successfully created a new PCB file..")
list_of_objects=[]
obj=database()
filename='text3.txt'
curblock=1
availblock=40-curblock
obj.add_details(filename,curblock,availblock)
list_of_objects.append(obj)
print("File Name",'\t',"File Size,"'\t',"Blocks",'\t',"sBlock",'\t',"Eblock")
print(list_of_objects[0].file_name,'\t',list_of_objects[0].file_size,'\t','\t',list_of_objects[0].number_blocks,'\t','\t',list_of_objects[0].start_block,'\t','\t',list_of_objects[0].end_block)
