# Secure Git Automation Tool Using Python and Cron
A Python-based automation tool that securely detects, commits, and pushes Git changes on a scheduled basis while preventing accidental exposure of sensitive files.

---

## 📌 Overview

Maintaining consistent Git commits can become repetitive and error-prone when working on projects regularly. While automation can reduce manual effort, unsafe automation may introduce risks such as committing sensitive files or pushing unintended changes.
This project focuses on **secure and controlled Git automation**, prioritizing safety, visibility, and reliability over aggressive unattended execution.

---

## 🎯 Key Objectives

- Automate Git commit and push operations safely
- Prevent accidental commits of sensitive files
- Maintain clean and meaningful commit history
- Allow safe testing using dry-run mode
- Provide visibility through structured logging
- Enable scheduled execution using cron
  
---

## 🛠 Tech Stack

- **Python 3**
- **Git & GitHub**
- **Kali Linux**
- **Cron (Linux Scheduler)**
- **SSH-based GitHub Authentication**
  
---

## ⚙️ How It Works (High-Level)

1. Reads configuration values from `config.json`
2. Detects Git changes using:
   ```bash
   git status --porcelain
3.Filters out potentially sensitive files
4.Limits the number of files processed per run
5.Supports dry-run mode for safe previews
6.Commits and pushes changes using SSH
7.Logs all actions for visibility and debugging

---

✨ Features

* Automated detection of file additions, modifications, and deletions
* Config-driven behavior without modifying source code
* Sensitive file protection using pattern-based detection
* Commit rate limiting per execution
* Dry-run mode for safe testing
* Scheduled execution via cron
* Secure SSH authentication (no passwords or tokens)
* Structured logging with timestamps
* Supports nested directories

---

🔐 Security Considerations

* Sensitive files (e.g. .env, .pem, files containing password, token, key) are automatically skipped
* Dry-run mode prevents accidental commits during testing
* SSH authentication avoids hardcoded credentials
* Logging provides transparency and auditability

---

🚀 Usage
1. Configuration
```
Create a config.json file:
{
  "project_dir": "/path",
  "max_changes_per_run": #,
  "log_file": "/path"
}
```

2. Run Manually
```
python3 gith_auto_commit.py
```
4. Dry-Run Mode (Recommended)
```
python3 gith_auto_commit.py --dry-run
```
Shows what would happen without making any changes.

4. Schedule with Cron

Edit crontab:
```
crontab -e
```

Example (run daily at 11 PM):
```
0 23 * * * /usr/bin/python3 /home/asad/Documents/gith_auto_commit.py >> /home/asad/github.log 2>&1
```
---

🧪 Testing Summary

* Verified detection of file creation, modification, and deletion
* Tested sensitive file blocking with multiple naming variations
* Validated commit limits per execution
* Confirmed dry-run behavior
* Verified cron execution and logging

---

⚠️ Limitations

* Sensitive detection is filename-based (not content-based)
* Designed for single-user repositories
* No cryptographic file integrity monitoring
* Cron environment dependency
* Limited automatic error recovery

---

🔮 Future Improvements

* Content-based secret scanning
* Notification support (email / alerts)
* Enhanced error handling and retry logic
* Cross-platform support
* CI/CD or GitHub Actions integration

---

📚 What I Learned

* Secure automation design principles
* Git internals and secret scanning behavior
* SSH authentication for non-interactive environments
* Cron job debugging and logging
*Balancing automation with security controls

---

👤 Author

**Asad Sayyad**
Cybersecurity learner focused on Linux, Git, networking, automation, and secure system design.

GitHub: [https://github.com/AsadSayyad92](https://github.com/AsadSayyad92)

---

⭐ If you find this helpful, feel free to star the repository.
