# Mini C Compiler - Deployment Guide

## 📋 Table of Contents
1. [Local Deployment](#local-deployment)
2. [Cloud Deployment (Azure)](#cloud-deployment-azure)
3. [Docker Deployment](#docker-deployment)
4. [System Requirements](#system-requirements)

---

## Local Deployment

### Option 1: Direct Installation (Windows)

**Step 1: Clone the Repository**
```bash
git clone https://github.com/harshini4506/Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-.git
cd Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-
```

**Step 2: Install Python Dependencies**
```bash
pip install --upgrade pip
# No external Python dependencies required - uses only tkinter (built-in)
```

**Step 3: Verify Compiler Files**
Ensure these files exist in the directory:
- `compiler.exe` (Pre-compiled)
- `ui.py` (Main Python UI)
- `lexer.l` (Lexer specification)
- `parser.y` (Parser specification)

**Step 4: Run the Application**
```bash
python ui.py
```

✅ The IDE will launch with the professional interface!

---

### Option 2: Create a Batch Script (Windows Shortcut)

**Step 1: Create `run.bat` in project directory**
```batch
@echo off
cd /d "%~dp0"
python ui.py
pause
```

**Step 2: Run by double-clicking `run.bat`**

---

## Cloud Deployment (Azure)

### Option 1: Azure Web App (Streamlit Version)

**Step 1: Install Streamlit**
```bash
pip install streamlit
```

**Step 2: Create `app.py` for Streamlit**
```python
import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Mini C Compiler", layout="wide")
st.title("🔧 Mini C Compiler - Web Version")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💻 Code Editor")
    code = st.text_area("Enter C code:", height=400, value="""int main() {
    int x = 10;
    printf("%d", x);
    return 0;
}""")

with col2:
    st.subheader("📊 Output")
    if st.button("▶ Compile"):
        compiler_path = os.path.join(os.path.dirname(__file__), 'compiler.exe')
        if os.path.exists(compiler_path):
            result = subprocess.run([compiler_path], input=code, text=True, capture_output=True)
            st.text_area("Output:", value=result.stdout, height=400, disabled=True)
        else:
            st.error("compiler.exe not found")
```

**Step 3: Deploy to Azure**
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login to Azure
az login

# Create resource group
az group create --name mini-c-compiler --location eastus

# Create App Service Plan
az appservice plan create --name mini-c-compiler-plan --resource-group mini-c-compiler --sku B1 --is-linux

# Create Web App
az webapp create --resource-group mini-c-compiler --plan mini-c-compiler-plan --name mini-c-compiler-app --runtime "PYTHON|3.9"

# Configure deployment from GitHub
az webapp deployment source config --name mini-c-compiler-app --resource-group mini-c-compiler --repo-url https://github.com/harshini4506/Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases- --branch main --manual-integration

# View app
az webapp browse --name mini-c-compiler-app --resource-group mini-c-compiler
```

---

### Option 2: Azure Container Instance (Docker)

See [Docker Deployment](#docker-deployment) section below

---

## Docker Deployment

### Step 1: Create Dockerfile

Create `Dockerfile` in project root:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir streamlit

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Create .dockerignore

```
.git
.gitignore
__pycache__
*.pyc
.pytest_cache
.venv
venv
.idea
.vscode
*.egg-info
```

### Step 3: Build Docker Image

```bash
# Build the image
docker build -t mini-c-compiler:latest .

# Run locally to test
docker run -p 8501:8501 mini-c-compiler:latest
```

### Step 4: Deploy to Azure Container Registry

```bash
# Create container registry
az acr create --resource-group mini-c-compiler --name minicccompiler --sku Basic

# Login to registry
az acr login --name minicccompiler

# Tag image
docker tag mini-c-compiler:latest minicccompiler.azurecr.io/mini-c-compiler:latest

# Push to Azure
docker push minicccompiler.azurecr.io/mini-c-compiler:latest

# Create container instance
az container create \
  --resource-group mini-c-compiler \
  --name mini-c-compiler \
  --image minicccompiler.azurecr.io/mini-c-compiler:latest \
  --cpu 1 \
  --memory 1.5 \
  --registry-login-server minicccompiler.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 8501 \
  --environment-variables STREAMLIT_SERVER_PORT=8501
```

---

## System Requirements

### Minimum Requirements
- **OS:** Windows 7/8/10/11, macOS 10.14+, Ubuntu 16.04+
- **Python:** 3.7 or higher
- **RAM:** 512 MB
- **Disk Space:** 50 MB
- **Compiler:** Pre-compiled `compiler.exe` included

### Recommended Requirements
- **OS:** Windows 10/11 or Ubuntu 20.04+
- **Python:** 3.9+
- **RAM:** 2 GB
- **Disk Space:** 100 MB
- **Internet:** For cloud deployment

### Dependencies
```
Python 3.7+
tkinter (built-in with Python)
[Optional] Streamlit (for web deployment)
[Optional] Docker (for containerized deployment)
```

---

## Quick Start Comparison

| Deployment Method | Complexity | Cost | Access |
|---|---|---|---|
| **Local (Windows)** | ⭐ Easy | Free | Local only |
| **Local (Batch Script)** | ⭐ Easy | Free | Local only |
| **Azure Web App** | ⭐⭐⭐ Medium | $10-50/month | Global URL |
| **Docker Local** | ⭐⭐ Easy-Medium | Free | Local only |
| **Azure Container** | ⭐⭐⭐ Medium | $10-50/month | Global URL |

---

## Troubleshooting

### Issue: `compiler.exe not found`
**Solution:** Ensure `compiler.exe` is in the project directory

### Issue: Python not recognized
**Solution:** Add Python to PATH
```bash
# Windows - Run in PowerShell as Admin
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Python39", "User")
```

### Issue: Port already in use (Docker)
**Solution:** Use different port
```bash
docker run -p 9000:8501 mini-c-compiler:latest
```

### Issue: Azure deployment fails
**Solution:** Check Azure CLI installation
```bash
az --version
az login
```

---

## Support & Resources

- **GitHub:** https://github.com/harshini4506/Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-
- **Azure Docs:** https://docs.microsoft.com/en-us/azure/
- **Docker Docs:** https://docs.docker.com/
- **Python Docs:** https://docs.python.org/3/

---

## Next Steps

1. ✅ Choose deployment method based on your needs
2. ✅ Follow step-by-step instructions
3. ✅ Test the compiler with sample C code
4. ✅ Share the deployed URL with others
5. ✅ Monitor and maintain the deployment

---

**Happy Compiling! 🚀**
