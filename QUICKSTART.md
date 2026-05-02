# 🚀 QUICK DEPLOYMENT STEPS FOR MINI C COMPILER

## ⭐ CHOOSE YOUR DEPLOYMENT METHOD:

---

## **METHOD 1: LOCAL DEPLOYMENT (EASIEST - 2 minutes)**

### Windows Users:
```powershell
# Step 1: Clone repository
git clone https://github.com/harshini4506/Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-.git
cd Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-

# Step 2: Verify Python is installed
python --version  # Should be 3.7+

# Step 3: Run the application
python ui.py
```

✅ The IDE will launch immediately!

---

## **METHOD 2: WEB DEPLOYMENT (CLOUD - Azure)**

### Prerequisites:
- Azure Account (Free tier available: https://azure.microsoft.com/en-us/free/)
- Azure CLI installed: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

### Steps:
```powershell
# Step 1: Login to Azure
az login

# Step 2: Create resource group
az group create --name mini-c-compiler --location eastus

# Step 3: Create App Service Plan (Free tier)
az appservice plan create --name mini-c-compiler-plan ^
  --resource-group mini-c-compiler --sku B1 --is-linux

# Step 4: Create Web App
az webapp create --resource-group mini-c-compiler ^
  --plan mini-c-compiler-plan ^
  --name mini-c-compiler-YOURNAME ^
  --runtime "PYTHON|3.9"

# Step 5: Configure GitHub deployment
az webapp deployment source config ^
  --name mini-c-compiler-YOURNAME ^
  --resource-group mini-c-compiler ^
  --repo-url https://github.com/harshini4506/Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases- ^
  --branch main --manual-integration

# Step 6: View your deployed app
az webapp browse --name mini-c-compiler-YOURNAME ^
  --resource-group mini-c-compiler
```

✅ Your app will be live at: `https://mini-c-compiler-YOURNAME.azurewebsites.net`

---

## **METHOD 3: DOCKER DEPLOYMENT (CONTAINERIZED - Advanced)**

### Prerequisites:
- Docker Desktop installed: https://www.docker.com/products/docker-desktop

### Steps:
```powershell
# Step 1: Navigate to project
cd Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-

# Step 2: Build Docker image
docker build -t mini-c-compiler:latest .

# Step 3: Run locally to test
docker run -p 8501:8501 mini-c-compiler:latest

# Step 4: Open browser
Start-Process "http://localhost:8501"
```

✅ Web app running at http://localhost:8501

---

## **DEPLOYMENT COMPARISON TABLE**

| Method | Time | Cost | Complexity | Access |
|--------|------|------|-----------|---------|
| **Local** | 2 min | Free | ⭐ Easy | Your PC |
| **Azure Web App** | 10 min | $10-50/mo | ⭐⭐ Medium | Global URL |
| **Docker Local** | 5 min | Free | ⭐⭐ Medium | Localhost |
| **Docker + Azure** | 15 min | $10-50/mo | ⭐⭐⭐ Hard | Global URL |

---

## 📋 FILES FOR DEPLOYMENT

Your project now includes:
- ✅ `DEPLOYMENT.md` - Full deployment guide
- ✅ `Dockerfile` - Container configuration
- ✅ `app.py` - Web version (Streamlit)
- ✅ `requirements.txt` - Python dependencies
- ✅ `.dockerignore` - Docker ignore file
- ✅ `ui.py` - Desktop version (Tkinter)

---

## 🐛 TROUBLESHOOTING

**Problem: "Python not found"**
```powershell
# Add Python to PATH
$pythonPath = "C:\Users\YourUsername\AppData\Local\Programs\Python\Python39"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$pythonPath", "User")
```

**Problem: "compiler.exe not found"**
- Ensure `compiler.exe` is in the project directory
- Check file exists: `ls -la compiler.exe`

**Problem: "Port already in use" (Docker)**
```powershell
docker run -p 9000:8501 mini-c-compiler:latest
# Access at http://localhost:9000
```

**Problem: Azure deployment failed**
```powershell
# Check deployment logs
az webapp log tail --name mini-c-compiler-YOURNAME ^
  --resource-group mini-c-compiler
```

---

## 📞 SUPPORT

- 📘 **Full Guide:** See `DEPLOYMENT.md`
- 🐙 **GitHub:** https://github.com/harshini4506/Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-
- 💬 **Issues:** GitHub Issues section
- 📧 **Docs:** Check project README.md

---

## ✅ VERIFICATION CHECKLIST

After deployment, verify:
- [ ] Application launches without errors
- [ ] Can load sample C code
- [ ] Compile button works
- [ ] Output panels display results
- [ ] No 404 or 500 errors

---

## 🎯 NEXT STEPS

1. Choose deployment method (recommendation: Start with LOCAL)
2. Follow the steps for your chosen method
3. Test the compiler with sample code
4. Share the deployed URL with others
5. Monitor logs for issues

---

**Happy Deploying! 🚀**
