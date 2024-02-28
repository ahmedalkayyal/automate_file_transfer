
import ftplib
import os
import shutil
import schedule
import logging
from datetime import datetime


ftp_host = 'localhost'
ftp_username = 'abcd'
ftp_password = 'abcd123'


local_dir = r"C:\Users\ASUS\Desktop\testftp"
internal_dir = r"C:\Users\ASUS\Desktop\myserver"


LOG_FILENAME = os.path.join(local_dir, 'file_transfer.log')
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

def transfer_files():
    try:
       
        choice = input("Do you want to transfer files from the FTP server? (yes/no): ")
        if choice.lower() != 'yes':
            logging.info("File transfer process cancelled by user.")
            return
        
        
        with ftplib.FTP(ftp_host, ftp_username, ftp_password) as ftp:
            print("Connected to FTP server successfully.")
            
            files = ftp.nlst()
            print("Files in the FTP directory:")
            for file in files:
                print(file)

                logging.info(f"{datetime.now()} - File listed: {file}")
                
            local_log_file = open(LOG_FILENAME, 'rb')

            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

           
            for file in files:
                with open(os.path.join(local_dir, file), 'wb') as local_file:
                     ftp.retrbinary('RETR ' + file, local_file.write)
                    
            
            num_files_moved = 0
            print("\nFiles to be moved:")
            for file in files:
                print(file)
                num_files_moved += 1
                
            print(f"\nTotal number of files to be moved: {num_files_moved}\n")
           
            for file in files:
                shutil.move(os.path.join(local_dir, file), internal_dir)
                logging.info(f"{datetime.now()} - File transferred: {file}")
        
            print(f"{num_files_moved} files moved successfully.")
            logging.info(f"{num_files_moved} files moved successfully.")
            
            ftp.storbinary('STOR file_transfer.log', local_log_file)
            local_log_file.close()

    except Exception as e:
        logging.error(f"Error transferring files: {e}")

transfer_files()

schedule.every().day.at("12:00").do(transfer_files)

try:
    while True:
        schedule.run_pending()
except KeyboardInterrupt:
    logging.info("File transfer process stopped.")
    
    
#Ahmed Alkayyal
# The ftplib, os, shutil, schedule, and logging libraries to automate the transfer of files between an FTP server and an internal directory. 
# The script prompts the user for input, connects to a local FTP server (in this case 'localhost') using the specified username and password, lists files in the FTP directory, 
# downloads them to a local directory, and then moves them to an internal directory.

# For scheduling, the script uses the schedule library to run the file transfer function daily at 12:00. It also handles exceptions and 
# logs detailed error messages using the logging library.


# This automation solution is designed to work within a Windows 11 environment, with the possibility of using IIS, FileZilla server app,
# and WinSCP app to manage the FTP server and file transfer operations efficiently. It provides a straightforward and effective way to manage file transfers 
# and logging with Python.