# pro_venv — Python Project Scaffold (Portable)

![Build](https://github.com/TamerOnLine/pro_venv/actions/workflows/test-pro_venv.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/TamerOnLine/pro_venv?style=flat-square)
![License](https://img.shields.io/github/license/TamerOnLine/pro_venv?style=flat-square)

A one‑shot, **portable** scaffold for Python projects. It prepares a virtual environment, installs requirements, generates a safe launcher, and configures VS Code — all from **the project root**. Drop it into any project and run.

---

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration (`setup-config.json`)](#configuration-setup-configjson)
- [Generated Project Structure](#generated-project-structure)
- [GitHub Actions (Optional)](#github-actions-optional)
- [VS Code Integration](#vs-code-integration)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Arabic / العربية](#arabic--العربية)

---

## Features
- **Zero-friction setup**: create `venv/`, upgrade `pip`, install from `requirements.txt` (auto‑created if missing).
- **Safe launcher**: `main.py` re‑executes inside the virtual environment, then runs your entry (`app.py` by default).
- **Editor ready**: generates `.vscode/settings.json`, `.vscode/launch.json`, and a `project.code-workspace`.
- **Reproducibility**: writes `env-info.txt` (Python version + installed packages).
- **Optional CI**: generate a minimal GitHub Actions workflow in one command.
- **Portable by design**: intended to live at project root and Just Work™ on Windows/Linux/macOS.

---

## Quick Start
> Run all commands from **the project root**.

```bash
# first-time setup
python pro_venv.py

# later — start your app via the safe launcher
python main.py
```
> You don’t need to manually activate `venv`. The launcher handles it automatically.

---

## Usage
**First run** creates or updates the following:
- `venv/` and toolchain (upgrades `pip`).
- `requirements.txt` (created if absent; left untouched otherwise).
- `main.py` (safe launcher) and `app.py` (starter entry point — replace with your app).
- `.vscode/` configs and `project.code-workspace`.
- `env-info.txt` snapshot of the environment.

### Typical workflows
- **Change the app entry**: edit `setup-config.json` → set `"main_file": "my_app.py"`.
- **Pin Python version**: set `"python_version": "3.12"` (or another installed version).
- **Regenerate CI**: run `python pro_venv.py --ci create` (see below).

---

## Configuration (`setup-config.json`)
On first run, the script creates `setup-config.json` with sane defaults:

```json
{
  "project_name": "<folder-name>",
  "main_file": "app.py",
  "entry_point": "main.py",
  "requirements_file": "requirements.txt",
  "venv_dir": "venv",
  "python_version": "3.12"
}
```

**Notes**
- `main_file` is the file launched by `main.py` **after** ensuring the venv is active.
- `entry_point` is the launcher itself; keep as `main.py` unless you have a reason to change it.
- `requirements_file` can be any path (e.g. `requirements/dev.txt`).
- `venv_dir` can be renamed (e.g. `.venv`).

---

## Generated Project Structure
```
.
├── pro_venv.py
├── setup-config.json
├── requirements.txt
├── main.py           # safe launcher (re-executes inside venv)
├── app.py            # starter app — replace with your code
├── env-info.txt      # snapshot of env and packages
├── venv/             # created automatically
└── .vscode/
    ├── settings.json
    └── launch.json
```

---

## GitHub Actions (Optional)
Generate a minimal CI workflow that runs the scaffold on push/PR:

```bash
python pro_venv.py --ci create            # create if missing
python pro_venv.py --ci force             # overwrite if exists
python pro_venv.py --ci create --ci-python 3.12  # pick a Python version
```
This writes `.github/workflows/test-pro_venv.yml`.

---

## VS Code Integration
- The scaffold writes `.vscode/settings.json` and `.vscode/launch.json` so **Run** just works.
- The Python interpreter path is set to the venv inside the project, ensuring consistent launches.
- You can freely customize debug configurations in `launch.json` (e.g., args, env, cwd).

**Tip**: Keep `.vscode/` out of version control if project collaborators prefer their own editor settings.

---

## Troubleshooting
**“Python not found”**
- Ensure the specified `python_version` is installed on your system.

**Pip installation problems / SSL**
- Check network/SSL settings and upgrade `pip` manually if needed: `python -m pip install --upgrade pip`.

**Windows Execution Policy**
- If terminal refuses to run scripts, start a shell as Administrator and:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

**Running from outside project root**
- The launcher is designed for project-root execution. If you enforce a root check, run from the correct directory.

---

## FAQ
**Do I need to activate the venv manually?**  
No. `main.py` re-executes inside the venv and then runs `app.py` (or your `main_file`).

**Can I rename `venv` to `.venv`?**  
Yes — update `venv_dir` in `setup-config.json` and re-run the script.

**Can I use a different entry than `app.py`?**  
Yes — set `main_file` to your desired module (e.g., `src/server.py`).

**Will it modify my existing `requirements.txt`?**  
No. If present, it’s used as-is.

---

## Contributing
PRs and issues are welcome. Please keep changes minimal and portable.

---

## License
MIT. See `LICENSE`.

---

## Arabic / العربية
**pro_venv** أداة تجهيز سريعة ومحمولة لمشاريع بايثون. تُنشئ بيئة افتراضية، تُثبّت الحزم، وتولّد مُشغِّلاً آمنًا وملفات VS Code — من جذر المشروع.

### المزايا
- إعداد فوري مع `venv/` وتحديث `pip` وتثبيت من `requirements.txt`.
- مُشغّل آمن (`main.py`) يضمن العمل داخل البيئة قبل تشغيل ملفك الرئيسي (`app.py`).
- ملفات VS Code جاهزة (`.vscode/…`) ومساحة عمل.
- ملف `env-info.txt` لتوثيق البيئة.
- خيار توليد CI بسيط.

### البدء السريع
```bash
python pro_venv.py   # أول تشغيل
python main.py       # تشغيل التطبيق لاحقًا عبر المُشغِّل الآمن
```

### الإعداد (`setup-config.json`)
- `main_file`: الملف الذي سيُشغَّل بعد تفعيل البيئة (افتراضيًا `app.py`).
- `venv_dir`: اسم مجلد البيئة (مثل `.venv`).
- `python_version`: إصدار بايثون المطلوب.

### CI اختياري
```bash
python pro_venv.py --ci create            
python pro_venv.py --ci force             
python pro_venv.py --ci create --ci-python 3.12
```

### المشاكل الشائعة
- تأكد من وجود الإصدار المطلوب من بايثون.
- على ويندوز، قد تحتاج لتغيير سياسة التنفيذ كما هو موضح أعلاه.

> للمساهمة أو الترخيص: انظر الأقسام أعلاه.
