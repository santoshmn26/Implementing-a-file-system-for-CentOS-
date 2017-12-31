# Implementing-a-file-system-for-CentOS-
Implementing a file system in CentOS using python.

This project contains 3 files 
  1. Phase1: Simple project to execute shell commands using python.
  2. Phase2: Use Phase1 and Subprocess.call function to invoke Fork() and execvp().
  3. Phase3: Create a complete FCB file control block to manage files.

Phase-3 Creates a FCB that can manipulate file and execute commands on files such as
  1. put: insert a file into FCB
  2. get: get a file from FCB/copy file from FCB 
  3. putr: put remarks to a file in FCB
  4. rm: delete a file in FCB
  5. kill: delete the current FCB and all files inside the FCB
  6. vi: open a text editor with the given file name
  7. putc: put comments to the selected file
