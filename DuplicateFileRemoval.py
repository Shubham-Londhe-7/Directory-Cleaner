"""
====================================================================
Duplicate File Cleaner with Email Automation
--------------------------------------------------------------------
Author  : Shubham Londhe
Purpose : 
    - Scan directory recursively
    - Identify duplicate files using MD5 checksum
    - Delete duplicate copies (keep one original)
    - Generate timestamped log file
    - Send deletion report via email
    - Execute automatically at scheduled intervals

Usage :
    python AddLogFileSendMail.py <DirectoryPath> <TimeInterval(min)> <ReceiverEmail>
====================================================================
"""

import sys
import time
import os
import hashlib
import schedule
import smtplib
from email.message import EmailMessage


# ---------------------------------------------------------------
# Calculate MD5 checksum of file (used to detect duplicates)
# ---------------------------------------------------------------
def CalculateCheckSum(path, BlockSize=1024):
    fobj = open(path, "rb")
    hobj = hashlib.md5()

    # Read file in chunks to support large files
    buffer = fobj.read(BlockSize)
    while len(buffer) > 0:
        hobj.update(buffer)
        buffer = fobj.read(BlockSize)

    fobj.close()
    return hobj.hexdigest()


# ---------------------------------------------------------------
# Traverse directory and group files by checksum
# ---------------------------------------------------------------
def FindDuplicate(DirectoryName):

    # Convert relative path to absolute
    if not os.path.isabs(DirectoryName):
        DirectoryName = os.path.abspath(DirectoryName)

    # Validate path
    if not os.path.exists(DirectoryName):
        print("Invalid path")
        exit()

    if not os.path.isdir(DirectoryName):
        print("Path is not a directory")
        exit()

    Duplicate = {}
    TotalCount = 0

    # Walk through directory recursively
    for FolderName, SubFolderNames, FileNames in os.walk(DirectoryName):
        for fname in FileNames:
            TotalCount += 1
            fname = os.path.join(FolderName, fname)

            # Generate checksum
            checkSum = CalculateCheckSum(fname)

            # Group files by checksum
            if checkSum in Duplicate:
                Duplicate[checkSum].append(fname)
            else:
                Duplicate[checkSum] = [fname]

    return Duplicate, TotalCount


# ---------------------------------------------------------------
# Create timestamped log file
# ---------------------------------------------------------------
def DirectoryLog():

    if not os.path.exists("Logs"):
        os.mkdir("Logs")

    timestamp = time.ctime()
    FileName = "Log_%s.log" % (timestamp)
    FileName = FileName.replace(" ", "_").replace(":", "_")
    FileName = os.path.join("Logs", FileName)

    fobj = open(FileName, "w")

    Border = "-" * 80
    fobj.write(Border + "\n")
    fobj.write("Duplicate File Cleaner Automation Log\n")
    fobj.write(Border + "\n\n")

    fobj.close()
    return FileName


# ---------------------------------------------------------------
# Delete duplicates and send email report
# ---------------------------------------------------------------
def DeleteDuplicateSendMail(Path, Email):

    MyDict, TotalFiles = FindDuplicate(Path)

    # Filter only duplicates (checksum with more than 1 file)
    Result = list(filter(lambda X: len(X) > 1, MyDict.values()))

    LogFile = DirectoryLog()
    fobj = open(LogFile, "a")

    Border = "-" * 80
    timestamp = time.ctime()

    Count = 0
    DeletedCount = 0

    fobj.write("Scanning started at : " + timestamp + "\n")
    fobj.write("Deleted files list:\n")

    # Keep first file, delete remaining
    for value in Result:
        for subValue in value:
            Count += 1
            if Count > 1:
                fobj.write(subValue + "\n")
                os.remove(subValue)
                DeletedCount += 1
        Count = 0

    # Log summary
    fobj.write("Total files scanned : " + str(TotalFiles) + "\n")
    fobj.write("Total deleted files : " + str(DeletedCount) + "\n\n")
    fobj.write(Border + "\n")
    fobj.write("Log created at : " + timestamp + "\n")
    fobj.write(Border + "\n")

    fobj.close()

    print("Total deleted files:", DeletedCount)

    # Send email with log attachment
    SendMail(Email, LogFile)


# ---------------------------------------------------------------
# Send email with log attachment
# ---------------------------------------------------------------
def SendMail(receiver_mail, Attachment):

    # ⚠️ Replace with environment variables in production
    sender_mail = "your_email@gmail.com"
    sender_password = "your_app_password"

    body = "Attached is the duplicate file deletion report."

    msg = EmailMessage()
    msg['Subject'] = "Duplicate File Cleaner Report"
    msg['From'] = sender_mail
    msg['To'] = receiver_mail
    msg.set_content(body)

    # Attach log file
    fobj = open(Attachment, 'rb')
    msg.add_attachment(fobj.read(),
                       maintype='application',
                       subtype='octet-stream',
                       filename=fobj.name)

    # Send mail
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(sender_mail, sender_password)
    smtp.send_message(msg)
    smtp.quit()

    print("Email sent successfully!")


# ---------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------
def main():

    Border = "-" * 63
    print(Border)
    print("----------- Duplicate File Cleaner Automation -----------")
    print(Border)

    # Help flags
    if len(sys.argv) == 2:

        if sys.argv[1].lower() == "--h":
            print("Deletes duplicate files and emails report.")

        elif sys.argv[1].lower() == "--u":
            print("Usage:")
            print("python AddLogFileSendMail.py <DirectoryPath> <TimeInterval(min)> <ReceiverEmail>")

    # Normal execution
    elif len(sys.argv) == 4:

        schedule.every(int(sys.argv[2])).minutes.do(
            DeleteDuplicateSendMail, sys.argv[1], sys.argv[3])

        while True:
            schedule.run_pending()
            time.sleep(1)

    else:
        print("Invalid arguments. Use --h or --u")

    print(Border)
    print("--------------- Script Execution Finished ---------------")
    print(Border)


if __name__ == "__main__":
    main()
