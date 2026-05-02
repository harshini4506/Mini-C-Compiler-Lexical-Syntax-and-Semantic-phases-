# 🚀 Render Deployment Guide

This guide provides step-by-step instructions to deploy the Mini C Compiler on Render.

---

## **Step 1: Render Web Service Form - Field Values**

When creating a new Web Service on Render, use these exact values:

| Field | Value |
|-------|-------|
| **GitHub Repository** | `harshini4506/Mini-C-Compiler-Lexical-Syntax-and-Semantic-phases-` |
| **Service Name** | `mini-c-compiler` |
| **Instance Type** | `Free` (or Starter for production) |
| **Region** | `Oregon (US West)` or closest to you |
| **Build & Deploy** | Leave default |
| **Environment** | `Production` |

---

## **Step 2: Critical Build Configuration**

### **Build Command** (if Render asks for it)
```bash
apt-get update && apt-get install -y flex bison gcc build-essential
```

### **Start Command** (should auto-fill from Procfile)
```bash
gunicorn app:app --bind 0.0.0.0:10000
```

---

## **Step 3: Port Configuration**

- **Expose Port**: `10000`
- **Environment Variable** (Optional):
  ```
  FLASK_ENV=production
  PORT=10000
  ```

---

## **Step 4: Understanding the Deployment Pipeline**

### **What Happens When You Deploy:**

1. **Render pulls your GitHub repository**
2. **Dockerfile builds the container:**
   - Base: `python:3.9-slim`
   - Installs: `gcc`, `build-essential`, `flex`, `bison`
   - Copies `requirements.txt` and runs `pip install`
   - Copies entire project
3. **Flask app starts via Gunicorn:**
   - Listens on `0.0.0.0:10000`
4. **First request triggers `ensure_compiler_binary()`:**
   - Checks if `compiler` or `compiler.exe` exists
   - Lists available files (DEBUG output visible in logs)
   - Compiles `y.tab.c + lex.yy.c → compiler` binary
   - Caches binary for future requests

---

## **Step 5: Deployment Checklist**

Before clicking "Deploy":

✅ **Repository files present:**
- [ ] `y.tab.c` (generated parser code)
- [ ] `lex.yy.c` (generated lexer code)
- [ ] `parser.y` (grammar definition)
- [ ] `lexer.l` (lexer definition)
- [ ] `app.py` (Flask backend)
- [ ] `requirements.txt` (Python dependencies)
- [ ] `Dockerfile` (container configuration)
- [ ] `Procfile` (startup command)
- [ ] `templates/index.html` (web UI)
- [ ] `static/style.css` + `static/script.js`

✅ **Dockerfile includes:**
```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential flex bison \
    && rm -rf /var/lib/apt/lists/*
```

✅ **app.py uses relative paths:**
```python
# ✓ Correct (relative)
"y.tab.c"
"lex.yy.c"

# ✗ Wrong (hardcoded /app/)
"/app/y.tab.c"
```

---

## **Step 6: Monitoring Deployment**

### **Watch the Build Logs:**

Look for these SUCCESS indicators:
```
[DEBUG] Working directory: /opt/render/project/src
[DEBUG] Files present: ['y.tab.c', 'lex.yy.c', ...]
[DEBUG] Building compiler with: gcc -std=c99 -w y.tab.c lex.yy.c -lm -o compiler
[DEBUG] Build returncode: 0
[DEBUG] Compiler successfully built at: /opt/render/project/src/compiler
```

### **Common ERROR Messages & Fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `y.tab.c: No such file` | File not in repo | Ensure `y.tab.c` is committed and pushed |
| `bison: command not found` | Render doesn't have bison | Dockerfile already includes it (check it was pushed) |
| `lex.yy.c: No such file` | File not in repo | Ensure `lex.yy.c` is committed and pushed |
| `gcc: command not found` | gcc not installed | Dockerfile already includes it (check it was pushed) |

---

## **Step 7: Test the Deployment**

Once deployed (Render shows green "Live" status):

1. **Visit your service URL:**
   ```
   https://mini-c-compiler.onrender.com
   ```

2. **Test compilation:**
   - Click "Load Sample" → "Hello World"
   - Click "Compile"
   - Verify output appears in Tokens/Syntax/Semantic tabs

3. **Sample test code:**
   ```c
   int main() {
       int x = 5;
       printf("%d", x);
       return 0;
   }
   ```

---

## **Step 8: Troubleshooting**

### **Deployment Fails During Build:**

1. Click "View Logs" in Render dashboard
2. Look for `[DEBUG]` output in the logs
3. Check for missing `y.tab.c` or `lex.yy.c`
4. Verify `Dockerfile` was pushed with `flex bison`

### **App Starts but Compilation Fails:**

1. Check app logs (Runtime section)
2. Look for `[DEBUG]` output showing file listing
3. Verify `app.py` using relative paths (`"y.tab.c"` not `"/app/y.tab.c"`)

### **Port Binding Issues:**

- Render uses port `10000` by default
- `Procfile` must specify `--bind 0.0.0.0:10000`
- Flask app must bind to all interfaces (`0.0.0.0`)

---

## **Step 9: After Successful Deployment**

- Share your live URL: `https://mini-c-compiler.onrender.com`
- Test with more complex C code (functions, while loops, etc.)
- Monitor logs for any compilation errors
- Scale to paid tier if needed (free tier sleeps after inactivity)

---

## **Key Differences: Local vs Render**

| Aspect | Local (Windows) | Render (Linux) |
|--------|-----------------|----------------|
| **Binary name** | `compiler.exe` | `compiler` |
| **Working dir** | `C:\...\project` | `/opt/render/project/src` |
| **Path separator** | `\` | `/` |
| **Build tools** | WinFlexBison | apt-get (flex/bison) |
| **GCC flags** | `-w -std=c99` | `-w -std=c99` |
| **Port** | Any (local) | `10000` (fixed) |

---

## **Important: File Inventory Check**

Run this command locally to verify all required files are committed:

```bash
git ls-files | grep -E "\.c$|\.h$|\.l$|\.y$|\.py$|requirements.txt|Dockerfile|Procfile"
```

**Expected output:**
```
app.py
lex.yy.c
lexer.l
parser.y
requirements.txt
y.tab.c
y.tab.h
Dockerfile
Procfile
templates/index.html
static/script.js
static/style.css
```

If any file is missing, add and commit it:
```bash
git add <missing-file>
git commit -m "Add missing deployment file"
git push origin main
```

---

## **Final Deployment Command (Summary)**

1. Ensure all files are pushed to GitHub
2. Open Render dashboard
3. Click "New +" → "Web Service"
4. Select your GitHub repository
5. Fill in form with values from **Step 1**
6. **Leave defaults** for Build Command & Start Command (they come from Dockerfile & Procfile)
7. Click "Deploy Web Service"
8. Wait for deployment to complete (~5-10 minutes)
9. Click "Live" link to test

---

## **Post-Deployment Monitoring**

- **Build Logs**: Check during deployment (look for `[DEBUG]` output)
- **Runtime Logs**: Check after deployment if app has issues
- **Metrics**: Monitor CPU/Memory in Render dashboard
- **Uptime**: Free tier goes dormant after 15 min inactivity (paid tiers are always on)

---

**You're ready to deploy! 🎉**
