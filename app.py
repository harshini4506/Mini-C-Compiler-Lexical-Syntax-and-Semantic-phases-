import streamlit as st
import subprocess
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Mini C Compiler IDE",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-size: 16px;
        padding: 12px 24px;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    h1 {
        color: #2563eb;
        text-align: center;
    }
    h2 {
        color: #1e40af;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🔧 Mini C Compiler - Professional IDE")
st.markdown("**Lexical Analysis | Syntax Analysis | Semantic Analysis**")
st.divider()

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This is a professional Mini C Compiler IDE supporting:
    - ✓ Variable declarations (int, float, char)
    - ✓ Arithmetic operations
    - ✓ Control flow (if-else, for loops)
    - ✓ I/O operations (printf, scanf)
    - ✓ Symbol table management
    - ✓ Parse tree generation
    - ✓ Semantic analysis
    """)
    
    st.divider()
    st.header("📝 Sample Code")
    
    samples = {
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
    
    selected_sample = st.selectbox("Load Sample:", list(samples.keys()))
    sample_code = samples[selected_sample]

# Main content area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("💻 Code Editor")
    
    # Initialize session state
    if 'code' not in st.session_state:
        st.session_state.code = sample_code
    if 'load_sample' not in st.session_state:
        st.session_state.load_sample = False
    
    # Load sample if selected
    if st.session_state.load_sample:
        st.session_state.code = sample_code
        st.session_state.load_sample = False
    
    # Code editor
    code_input = st.text_area(
        "Enter your C code:",
        value=st.session_state.code,
        height=300,
        key="code_editor",
        help="Write your C code here. Supports basic C syntax.",
        label_visibility="collapsed"
    )
    
    col_load, col_clear = st.columns(2)
    with col_load:
        if st.button("📁 Load Sample", use_container_width=True):
            st.session_state.code = sample_code
            st.rerun()
    
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.code = ""
            st.rerun()

with col2:
    st.subheader("📊 Compilation Output")
    
    if st.button("▶ Compile Code", use_container_width=True, type="primary"):
        if not code_input.strip():
            st.error("⚠️ Please enter C code to compile")
        else:
            st.info("⏳ Compiling...")
            
            try:
                # Find compiler executable
                compiler_path = os.path.join(os.path.dirname(__file__), 'compiler.exe')
                
                if not os.path.exists(compiler_path):
                    st.error(f"❌ Compiler not found at: {compiler_path}")
                else:
                    # Run compiler
                    result = subprocess.run(
                        [compiler_path],
                        input=code_input,
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
                    
                    # Display results in tabs
                    tab1, tab2, tab3 = st.tabs(["🔤 Tokens", "⚠️ Syntax Errors", "🔍 Semantic Analysis"])
                    
                    with tab1:
                        if tokens_output:
                            st.success("✓ Tokens generated successfully")
                            st.code('\n'.join(tokens_output), language='text')
                        else:
                            st.info("No tokens output")
                    
                    with tab2:
                        if syntax_output:
                            if any('error' in line.lower() for line in syntax_output):
                                st.error("✗ Syntax errors found")
                                st.code('\n'.join(syntax_output), language='text')
                            else:
                                st.success("✓ No syntax errors detected")
                        else:
                            st.success("✓ No syntax errors detected")
                    
                    with tab3:
                        if semantic_output:
                            st.error("✗ Semantic errors found")
                            st.code('\n'.join(semantic_output), language='text')
                        else:
                            st.success("✓ No semantic errors detected")
                    
                    st.success("✓ Compilation finished successfully!")
                    
            except subprocess.TimeoutExpired:
                st.error("❌ Compilation timeout (exceeded 10 seconds)")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 12px;'>
    <p>🚀 Mini C Compiler IDE | Professional Lexical • Syntax • Semantic Analyzer</p>
    <p>Built with Streamlit | Deployed on Azure</p>
</div>
""", unsafe_allow_html=True)
