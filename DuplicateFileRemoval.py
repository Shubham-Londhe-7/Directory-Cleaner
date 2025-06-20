
import sys
import time
import os
import hashlib
import schedule
import smtplib
from email.message import EmailMessage

def CalculateCheckSum(path, BlockSize = 1024):
    fobj = open(path,"rb")

    hobj = hashlib.md5()

    buffer = fobj.read(BlockSize)
    while(len(buffer) > 0):
        hobj.update(buffer)
        buffer = fobj.read(BlockSize)

    fobj.close()

    return hobj.hexdigest()


def FindDuplicate(DirectoryName):
    flag = os.path.isabs(DirectoryName)

    if(flag == False):
        DirectoryName = os.path.abspath(DirectoryName)

    flag = os.path.exists(DirectoryName)

    if(flag == False):
        print("The path is invalid")
        exit()

    flag = os.path.isdir(DirectoryName)

    if(flag == False):
        print("Path is valid but target is not directory")
        exit()
    
    Duplicate = {}

    for FolderName, SubFolderNames, FileNames in os.walk(DirectoryName): 
        TotalCount = 0                                                               
        for fname in FileNames:
            TotalCount = TotalCount + 1
            fname = os.path.join(FolderName,fname)
            checkSum = CalculateCheckSum(fname)
            
            if checkSum in Duplicate:
                Duplicate[checkSum].append(fname)
            else:
                Duplicate[checkSum] = [fname] 
    
    return Duplicate, TotalCount

def DirectoryLog():
    if(os.path.exists("Marvellous")):
        timestamp = time.ctime()

        FileName = "MarvellousLog_%s.log" %(timestamp)
        FileName = FileName.replace(" ","_")
        FileName = FileName.replace(":","_")
        FileName = os.path.join("Marvellous",FileName)
        
        fobj = open(FileName,"w")

        Border = "-"*80

        fobj.write(Border+"\n")
        fobj.write("This is a log file of Marvellous Automation Script \n")
        fobj.write("This is a directory cleaner script used to delete duplicate files \n")
        fobj.write(Border+"\n")
        fobj.write("\n\n\n\n")

        fobj.close()
        return FileName

    else:
        os.mkdir("Marvellous")
        timestamp = time.ctime()

        FileName = "MarvellousLog_%s.log" %(timestamp)
        FileName = FileName.replace(" ","_")
        FileName = FileName.replace(":","_")
        FileName = os.path.join("Marvellous",FileName)
        
        fobj = open(FileName,"w")

        Border = "-"*80

        fobj.write(Border+"\n")
        fobj.write("This is a log file of Marvellous Automation Script \n")
        fobj.write("This is a directory cleaner script used to delete duplicate files \n")
        fobj.write(Border+"\n")
        fobj.write("\n\n\n\n")

        fobj.close()
        return FileName

def DeleteDuplicateSendMail(Path, Email):
    MyDict, TotalFiles = FindDuplicate(Path)
    Result = list(filter(lambda X : len(X) > 1, MyDict.values()))
    
    LogFile = DirectoryLog()
    fobj = open(LogFile,"a")
    Border = "-"*80
    timestamp = time.ctime()

    Count = 0
    Cnt = 0
    Number = 0
    fobj.write("Scanning started at : "+timestamp+"\n")
    fobj.write("Names of deleted files are : \n")
    for value in Result:
        for subValue in value:
            Count += 1
            if(Count > 1):
                fobj.write(subValue)
                fobj.write("\n")
                os.remove(subValue)
                Cnt += 1
        Count = 0
    fobj.write("Total files scanned : "+str(TotalFiles)+"\n")
    fobj.write("Total deleted file : ")
    fobj.write(str(Cnt))
    fobj.write("\n\n\n\n")
    fobj.write(Border+"\n")
    fobj.write("This file is created at : "+timestamp +"\n")
    fobj.write(Border+"\n")
    fobj.close()
    print("Total deleted file :",Cnt)

    SendMail(Email,LogFile)


def SendMail(recaiver_mail, Attachment):
    sender_mail = "roronoagreatestswordsman@gmail.com"
    sender_password = "ijaz httg zodv edda"

    body = "These are name of deleted files"
    # Create email
    msg = EmailMessage()
    msg['Subject'] = "Deleted Duplicate Files"
    msg['From'] = sender_mail
    msg['To'] = recaiver_mail
    msg.set_content(body)

    # Attach file
    fobj = open(Attachment, 'rb')
    msg.add_attachment(fobj.read(), maintype='application', subtype='octet-stream', filename=fobj.name)

    # Send email
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(sender_mail, sender_password)
    smtp.send_message(msg)
    smtp.quit()

    print("Email sent successfully!")




def main():
    Border = "-"*63
    print(Border)
    print("------------------- Marvellous Automation ---------------------")
    print(Border)

    if(len(sys.argv) == 2):
        if((sys.argv[1] == "--h") or (sys.argv[1] == "--H")):
            print("This application is used to perform directory cleaning by deleting duplicate files and send email")
            print("This is the directory automation script")
        
        elif((sys.argv[1] == "--u") or (sys.argv[1] == "--U")):
            print("Use the given script as")
            print("python AddLogFileSendMail.py  DirectoryPath  TimeInterval(in minutes)  ReceiverEmail")
            print("Please provide valid absolute path")

    elif(len(sys.argv) == 4):
        schedule.every(int(sys.argv[2])).minutes.do(DeleteDuplicateSendMail, sys.argv[1], sys.argv[3])

        while True:
            schedule.run_pending()
            time.sleep(1)

    
    else:
        print("Invalid number of command line arguments")
        print("Use the given flags as :")
        print("--h : Used to display the help")
        print("--u : Used to display the usage")


    print(Border)
    print("---------------- Thank you for using our script ---------------")
    print("------------------- Marvellous Infosystems --------------------")
    print(Border)

if __name__ == "__main__":
    main()