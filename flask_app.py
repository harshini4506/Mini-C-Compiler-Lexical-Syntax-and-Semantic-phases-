from flask import Flask, render_template, request, jsonify
import subprocess
import os
from pathlib import Path

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Color constants (matching Tkinter UI)
COLOR_BG = '#f0f4f8'
COLOR_PRIMARY = '#2563eb'
COLOR_SECONDARY = '#1e40af'
COLOR_SUCCESS = '#10b981'
COLOR_ERROR = '#ef4444'
COLOR_WARNING = '#f59e0b'
COLOR_TEXT_DARK = '#1f2937'
COLOR_TEXT_LIGHT = '#6b7280'
COLOR_BORDER = '#e5e7eb'
COLOR_SURFACE = '#ffffff'
COLOR_SURFACE_ALT = '#f9fafb'

# Sample code snippets
SAMPLES = {
    "Hello World": """int main() {
    printf("Hello World");
    return 0;
}""",
    "Variables": """int main() {
    int x;
    float y;
    x = 10;
    y = 20.5;
    printf("%d", x);
    return 0;
}""",
    "Arithmetic": """int main() {
    int a = 10;
    int b = 20;
    int sum = a + b;
    printf("%d", sum);
    return 0;
}""",
    "If-Else": """int main() {
    int x = 5;
    if (x > 0) {
        printf("positive");
    }
    return 0;
}""",
    "For Loop": """int main() {
    int i;
    for (i = 0; i < 5; i = i + 1) {
        printf("%d", i);
    }
    return 0;
}"""
}

@app.route('/')
def index():
    return render_template('index.html', samples=SAMPLES)

@app.route('/api/compile', methods=['POST'])
def compile_code():
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        
        if not code:
            return jsonify({
                'status': 'error',
                'message': '⚠ Please enter C code to compile'
            }), 400
        
        # Find compiler executable
        compiler_path = os.path.join(os.path.dirname(__file__), 'compiler.exe')
        
        if not os.path.exists(compiler_path):
            return jsonify({
                'status': 'error',
                'message': f'✗ Compiler not found at: {compiler_path}'
            }), 500
        
        # Run compiler
        result = subprocess.run(
            [compiler_path],
            input=code,
            text=True,
            capture_output=True,
            timeout=10
        )
        
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        # Parse output
        tokens_output = []
        syntax_output = []
        semantic_output = []
        current_section = 'tokens'
        
        for line in stdout.splitlines():
            if '******stage 1******' in line:
                current_section = 'tokens'
                continue
            if '******stage 3******' in line:
                current_section = 'syntax'
                continue
            if 'ERROR:' in line or 'semantic' in line.lower():
                semantic_output.append(line)
                continue
            if current_section == 'tokens':
                tokens_output.append(line)
            elif current_section == 'syntax':
                syntax_output.append(line)
            else:
                tokens_output.append(line)
        
        if stderr:
            syntax_output.append(stderr)
        
        if not syntax_output:
            syntax_output = ['✓ No syntax errors detected.']
        
        if not semantic_output:
            semantic_output = ['✓ No semantic errors detected.']
        
        return jsonify({
            'status': 'success',
            'message': '✓ Compilation finished successfully!',
            'tokens': '\n'.join(tokens_output) if tokens_output else 'No tokens output',
            'syntax': '\n'.join(syntax_output),
            'semantic': '\n'.join(semantic_output)
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'message': '✗ Compilation timeout (exceeded 10 seconds)'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'✗ Error: {str(e)}'
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        if not file.filename.endswith('.c'):
            return jsonify({'status': 'error', 'message': 'Only .c files allowed'}), 400
        
        content = file.read().decode('utf-8', errors='ignore')
        
        return jsonify({
            'status': 'success',
            'message': f'✓ Loaded: {file.filename}',
            'code': content
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'}), 500

@app.route('/api/samples/<sample_name>', methods=['GET'])
def get_sample(sample_name):
    if sample_name in SAMPLES:
        return jsonify({
            'status': 'success',
            'code': SAMPLES[sample_name]
        })
    return jsonify({'status': 'error', 'message': 'Sample not found'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
