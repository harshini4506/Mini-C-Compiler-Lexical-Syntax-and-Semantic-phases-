// Mini C Compiler - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const codeEditor = document.getElementById('codeEditor');
    const lineNumbers = document.getElementById('lineNumbers');
    const compileBtn = document.getElementById('compileBtn');
    const clearBtn = document.getElementById('clearBtn');
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    const sampleSelect = document.getElementById('sampleSelect');
    const statusMessage = document.getElementById('statusMessage');
    const filePathDiv = document.getElementById('filePath');
    
    const tokensOutput = document.getElementById('tokensOutput');
    const syntaxOutput = document.getElementById('syntaxOutput');
    const semanticOutput = document.getElementById('semanticOutput');
    
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    // Update line numbers
    function updateLineNumbers() {
        const lines = codeEditor.value.split('\n').length;
        let lineNums = '';
        for (let i = 1; i <= lines; i++) {
            lineNums += i + '\n';
        }
        lineNumbers.textContent = lineNums;
    }

    // Sync scrolling between editor and line numbers
    codeEditor.addEventListener('scroll', function() {
        lineNumbers.scrollTop = codeEditor.scrollTop;
    });

    // Update line numbers on input
    codeEditor.addEventListener('input', updateLineNumbers);
    codeEditor.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 1;
            updateLineNumbers();
        }
    });

    // Initialize line numbers
    updateLineNumbers();

    // Tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');
        });
    });

    // Upload file
    uploadBtn.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        if (this.files.length === 0) return;
        
        const file = this.files[0];
        const formData = new FormData();
        formData.append('file', file);

        setStatus('📁 Uploading file...', 'info');

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                codeEditor.value = data.code;
                updateLineNumbers();
                filePathDiv.textContent = `Loaded: ${file.name}`;
                setStatus(`✓ ${data.message}`, 'success');
            } else {
                setStatus(`✗ ${data.message}`, 'error');
            }
        })
        .catch(error => {
            setStatus(`✗ Error: ${error.message}`, 'error');
        });
    });

    // Clear editor
    clearBtn.addEventListener('click', function() {
        codeEditor.value = '';
        filePathDiv.textContent = '';
        updateLineNumbers();
        setStatus('✓ Editor cleared.', 'info');
    });

    // Load sample
    sampleSelect.addEventListener('change', function() {
        if (this.value === '') return;

        setStatus('📝 Loading sample...', 'info');

        fetch(`/api/samples/${this.value}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    codeEditor.value = data.code;
                    updateLineNumbers();
                    filePathDiv.textContent = `Sample: ${this.value}`;
                    setStatus(`✓ Loaded sample: ${this.value}`, 'success');
                } else {
                    setStatus(`✗ Error loading sample`, 'error');
                }
            })
            .catch(error => {
                setStatus(`✗ Error: ${error.message}`, 'error');
            });
    });

    // Compile code
    compileBtn.addEventListener('click', function() {
        const code = codeEditor.value.trim();

        if (!code) {
            setStatus('⚠ Please enter C code to compile.', 'warning');
            return;
        }

        setStatus('⏳ Compiling...', 'info');
        compileBtn.disabled = true;

        fetch('/api/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            compileBtn.disabled = false;

            if (data.status === 'success') {
                tokensOutput.value = data.tokens || '// No tokens';
                syntaxOutput.value = data.syntax || '// No syntax errors';
                semanticOutput.value = data.semantic || '// No semantic errors';
                
                // Switch to tokens tab
                document.querySelector('[data-tab="tokens"]').click();
                
                setStatus(`✓ ${data.message}`, 'success');
            } else {
                setStatus(`✗ ${data.message}`, 'error');
            }
        })
        .catch(error => {
            compileBtn.disabled = false;
            setStatus(`✗ Error: ${error.message}`, 'error');
        });
    });

    // Set status message
    function setStatus(message, type = 'info') {
        statusMessage.textContent = message;
        statusMessage.className = 'status-message';
        
        if (type === 'success') {
            statusMessage.classList.add('success');
        } else if (type === 'error') {
            statusMessage.classList.add('error');
        } else if (type === 'warning') {
            statusMessage.classList.add('warning');
        }
    }

    // Initialize with default message
    setStatus('✓ Ready to compile. Upload or write your C code.', 'info');
});
