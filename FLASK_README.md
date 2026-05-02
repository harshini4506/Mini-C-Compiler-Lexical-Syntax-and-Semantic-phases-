# 🔧 Mini C Compiler - Flask Web Version

A professional Mini C Compiler IDE built with **Flask + HTML + CSS + JavaScript**.

## 🎯 Features

- ✅ **Professional UI** - Responsive design matching Tkinter version
- ✅ **Code Editor** - With line numbers and syntax area
- ✅ **Real-time Compilation** - Instant compilation feedback
- ✅ **Three Analysis Panels** - Tokens, Syntax Errors, Semantic Analysis
- ✅ **File Upload** - Load .c files from disk
- ✅ **Sample Code** - Pre-loaded C code examples
- ✅ **Status Updates** - Live compilation status
- ✅ **Responsive Design** - Works on desktop and tablet

## 📋 Requirements

- Python 3.7+
- Flask 2.3+
- `compiler.exe` (pre-compiled compiler)

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Compiler
Ensure `compiler.exe` is in the project root directory.

### Step 3: Run Flask App
```bash
python flask_app.py
```

### Step 4: Open Browser
Navigate to: **http://localhost:5000**

## 📁 Project Structure

```
.
├── flask_app.py              # Main Flask application
├── requirements.txt          # Python dependencies
├── compiler.exe              # Pre-compiled compiler
├── templates/
│   └── index.html           # Main HTML page
└── static/
    ├── style.css            # Styling (matches Tkinter design)
    └── script.js            # Interactive JavaScript
```

## 🎨 Design Highlights

- **Color Scheme**: Professional blue, green, red theme
- **Layout**: Two-panel design (Editor + Output)
- **Responsiveness**: Adapts to different screen sizes
- **Accessibility**: Keyboard shortcuts and helpful tooltips

## 🎮 Usage

1. **Write Code**: Type or paste C code in the editor
2. **Load Sample**: Select a sample from the dropdown
3. **Compile**: Click the "Compile" button
4. **View Results**: Check tokens, syntax errors, and semantic feedback

## 📊 API Endpoints

### POST `/api/compile`
Compiles C code and returns analysis results.

**Request:**
```json
{
    "code": "int main() { return 0; }"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "✓ Compilation finished successfully!",
    "tokens": "...",
    "syntax": "...",
    "semantic": "..."
}
```

### POST `/api/upload`
Uploads a .c file.

### GET `/api/samples/<name>`
Gets sample code by name.

## 🐛 Troubleshooting

**Problem: "compiler.exe not found"**
- Ensure `compiler.exe` is in the project directory

**Problem: Port 5000 already in use**
```bash
# Use a different port
python -c "from flask_app import app; app.run(port=5001)"
```

**Problem: "Flask not installed"**
```bash
pip install Flask
```

## 🔄 Deployment

### Local Development
```bash
python flask_app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn flask_app:app
```

### Docker
```bash
docker build -t mini-c-compiler .
docker run -p 5000:5000 mini-c-compiler
```

## 📝 Keyboard Shortcuts

- **Tab** - Insert tab in editor
- **Enter** - New line
- **Click Compile** - Compile code

## 🎓 Supported C Features

- Variable declarations (int, float, char)
- Arithmetic operations (+, -, *, /)
- Control flow (if-else, for loops)
- I/O operations (printf, scanf)
- Symbol table management
- Parse tree generation

## 📞 Support

- See **DEPLOYMENT.md** for deployment options
- See **QUICKSTART.md** for quick reference
- Check **README.md** for project details

## ✅ Testing

Test the compiler with sample code:
```c
int main() {
    int x = 10;
    printf("%d", x);
    return 0;
}
```

---

**Happy Compiling! 🚀**
