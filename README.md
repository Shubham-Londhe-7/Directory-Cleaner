# Duplicate File Cleaner Automation

## 📌 Overview

Duplicate File Cleaner Automation is a Python-based directory
maintenance tool that automatically scans folders, detects duplicate
files using MD5 checksum comparison, deletes redundant copies while
preserving one original file, generates detailed log reports, and sends
email notifications with log attachments at scheduled intervals.

This project demonstrates practical implementation of file handling,
hashing algorithms, scheduling, logging, automation, and SMTP-based
email integration.

------------------------------------------------------------------------

## 🚀 Features

-   Recursive directory scanning
-   Duplicate detection using MD5 hashing
-   Automatic deletion of duplicate copies
-   Timestamped log file generation
-   Email notification with log attachment
-   Scheduled execution using Python scheduler
-   Command-line interface support

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   Python 3
-   hashlib (MD5 hashing)
-   os (file system operations)
-   schedule (automation scheduling)
-   smtplib (email sending)
-   email.message (email construction)

------------------------------------------------------------------------

## 📂 Project Structure

    Duplicate-File-Cleaner/
    │
    ├── DuplicateFileRemoval.py
    └── README.md

------------------------------------------------------------------------

## ▶️ Usage

### Install dependencies

``` bash
pip install schedule
```

### Run script

``` bash
python DuplicateFileRemoval.py <DirectoryPath> <TimeInterval(min)> <ReceiverEmail>
```

### Example

``` bash
python DuplicateFileRemoval.py D:/TestFolder 10 example@gmail.com
```

------------------------------------------------------------------------

## ⚙️ How It Works

1.  The script traverses the directory recursively.
2.  Each file's MD5 checksum is calculated.
3.  Files with identical checksums are grouped as duplicates.
4.  The script keeps one original file and deletes remaining copies.
5.  A log file is generated with scan and deletion details.
6.  The log file is emailed to the specified receiver.
7.  The process repeats automatically based on schedule interval.

------------------------------------------------------------------------

## 🔒 Security Note

Do NOT store email credentials directly in code. Use environment
variables for production usage.

------------------------------------------------------------------------

## 🎯 Learning Outcomes

-   File system traversal
-   Hashing algorithms
-   Automation scripting
-   Logging practices
-   Email integration
-   Scheduled task execution

------------------------------------------------------------------------

## 👨‍💻 Author

Shubham Londhe

------------------------------------------------------------------------
