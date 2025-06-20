# 🧹 Marvellous Automation Script

This Python script is a **Directory Cleaner and Duplicate File Remover**, which identifies and deletes duplicate files from a specified directory and sends a log report via email. It can be scheduled to run at regular time intervals.

---

## 📄 Features

- Calculates MD5 checksums to detect duplicate files.
- Removes duplicate files automatically.
- Creates a detailed log of all operations performed.
- Sends the log as an email attachment to the provided email address.
- Can be scheduled to run repeatedly at specified intervals using command-line arguments.
- Provides help and usage instructions through command-line flags.

---

## 📦 Requirements

- Python 3.x
- Required libraries:
  - `schedule`
  - `smtplib`
  - `hashlib`
  - `email`
  - `os`, `time`, `sys`

To install missing libraries, use:
```bash
pip install schedule
```

---

## 🛠️ Script Files

- `AddLogFileSendMail.py` – Main script for duplicate file detection, deletion, logging, and email.
- `Marvellous/` – Folder where log files will be stored (auto-created if not present).

---

## 🧾 Usage

```bash
python AddLogFileSendMail.py <DirectoryPath> <TimeInterval(in minutes)> <ReceiverEmail>
```

### 🔁 Example
```bash
python AddLogFileSendMail.py /home/user/Documents 10 myemail@example.com
```

This command:
- Scans the `/home/user/Documents` directory every 10 minutes
- Deletes any duplicate files
- Logs the operations
- Emails the log to `myemail@example.com`

---

## 💡 Command Line Options

| Flag       | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| `--h` or `--H` | Displays help information about the script.                              |
| `--u` or `--U` | Displays usage instructions with an example.                             |

### Example:
```bash
python AddLogFileSendMail.py --h
python AddLogFileSendMail.py --u
```

---

## 📝 Notes

- Ensure that the sender's email (default: `roronoagreatestswordsman@gmail.com`) allows **less secure apps** or **app password** if using 2FA.
- The email credentials are hardcoded — it is recommended to use environment variables or a `.env` file for production use.
- Make sure the directory path is **absolute** (not relative).

---

## 📧 Email Configuration

The email is sent using:
- SMTP Server: `smtp.gmail.com`
- Port: `465` (SSL)
- From: `roronoagreatestswordsman@gmail.com`

**Update the script with your own email & app password for secure use.**

---

## 🏁 Output

- Duplicate files will be deleted.
- Log file will be created in the `Marvellous/` directory.
- Email will be sent with the log file attached.

---

## 👨‍💻 Developed By

**Shubham Londhe**  
_Automating your daily digital tasks._