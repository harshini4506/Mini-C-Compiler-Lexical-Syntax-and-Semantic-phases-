import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, font
import subprocess
import os

# Modern UI Theme Colors
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

# ==================== Compiler UI Helpers ====================

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("C files", "*.c")])
    if file_path:
        file_path_var.set(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            editor_text.delete('1.0', tk.END)
            editor_text.insert(tk.END, f.read())
        update_line_numbers()
        status_label.config(text=f"✓ Loaded: {os.path.basename(file_path)}", fg=COLOR_SUCCESS)


def update_line_numbers(event=None):
    line_count = int(editor_text.index('end-1c').split('.')[0])
    line_numbers.config(state='normal')
    line_numbers.delete('1.0', tk.END)
    line_numbers.insert('1.0', '\n'.join(str(i) for i in range(1, line_count + 1)))
    line_numbers.config(state='disabled')
    editor_text.yview_moveto(line_numbers.yview()[0])


def sync_scroll(*args):
    editor_text.yview(*args)
    line_numbers.yview(*args)


def on_editor_scroll(*args):
    line_numbers.yview_moveto(args[0])
    editor_text.yview_moveto(args[0])


def clear_editor():
    editor_text.delete('1.0', tk.END)
    update_line_numbers()
    status_label.config(text="✓ Editor cleared.", fg=COLOR_TEXT_LIGHT)
    file_path_var.set("")


def run_compiler():
    code = editor_text.get('1.0', tk.END).strip()
    if not code:
        status_label.config(text="⚠ Please write or upload C code before compiling.", fg=COLOR_WARNING)
        return

    compiler_path = os.path.join(os.path.dirname(__file__), 'compiler.exe')
    if not os.path.exists(compiler_path):
        status_label.config(text="✗ compiler.exe not found in project folder.", fg=COLOR_ERROR)
        return

    status_label.config(text="⏳ Compiling...", fg=COLOR_TEXT_LIGHT)
    root.update_idletasks()

    try:
        result = subprocess.run([compiler_path], input=code, text=True, capture_output=True)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

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

        if not tokens_output:
            tokens_output = [stdout or 'No compiler output available.']

        if stderr:
            syntax_output.append(stderr)

        if not syntax_output:
            syntax_output = ['✓ No syntax errors detected.']

        if not semantic_output:
            semantic_output = ['✓ No semantic errors detected.']

        tokens_panel.config(state='normal')
        tokens_panel.delete('1.0', tk.END)
        tokens_panel.insert(tk.END, '\n'.join(tokens_output).strip())
        tokens_panel.config(state='disabled')

        syntax_panel.config(state='normal')
        syntax_panel.delete('1.0', tk.END)
        syntax_panel.insert(tk.END, '\n'.join(syntax_output).strip())
        syntax_panel.config(state='disabled')

        semantic_panel.config(state='normal')
        semantic_panel.delete('1.0', tk.END)
        semantic_panel.insert(tk.END, '\n'.join(semantic_output).strip())
        semantic_panel.config(state='disabled')

        status_label.config(text="✓ Compilation finished successfully!", fg=COLOR_SUCCESS)
    except Exception as exc:
        status_label.config(text=f"✗ Error running compiler: {exc}", fg=COLOR_ERROR)


# ==================== Main Window ====================

root = tk.Tk()
root.title('Mini C Compiler - Professional IDE')
root.geometry('1400x900')
root.configure(bg=COLOR_BG)
root.minsize(1280, 750)

# Fonts - Enhanced typography
heading_font = font.Font(family='Segoe UI', size=32, weight='bold')
section_font = font.Font(family='Segoe UI', size=16, weight='bold')
body_font = font.Font(family='Segoe UI', size=10)
code_font = font.Font(family='Courier New', size=13)
small_font = font.Font(family='Segoe UI', size=9)
badge_font = font.Font(family='Segoe UI', size=9, weight='bold')

# Overlay Shapes - Gradient effect
bg_canvas = tk.Canvas(root, bg=COLOR_BG, highlightthickness=0)
bg_canvas.place(relwidth=1, relheight=1)
bg_canvas.create_oval(-150, -100, 350, 300, fill='#dbeafe', outline='')
bg_canvas.create_oval(1050, -150, 1450, 250, fill='#ede9fe', outline='')
bg_canvas.create_oval(900, 580, 1350, 1000, fill='#fef3c7', outline='')

main_frame = tk.Frame(root, bg=COLOR_SURFACE, bd=0)
main_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.96, relheight=0.96)
main_frame.config(highlightbackground='#d1d5db', highlightthickness=1)

# Header
header_frame = tk.Frame(main_frame, bg=COLOR_SURFACE)
header_frame.pack(fill='x', pady=(28, 16), padx=32)

title_frame = tk.Frame(header_frame, bg=COLOR_SURFACE)
title_frame.pack(side='left', anchor='n')

title_label = tk.Label(title_frame, text='🔧 Mini C Compiler', font=heading_font, bg=COLOR_SURFACE, fg=COLOR_PRIMARY)
title_label.pack(anchor='w')

subtitle_label = tk.Label(title_frame, text='Professional Lexical | Syntax | Semantic Analyzer', font=body_font, bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT)
subtitle_label.pack(anchor='w', pady=(10, 0))

header_actions = tk.Frame(header_frame, bg=COLOR_SURFACE)
header_actions.pack(side='right', anchor='n')

file_path_var = tk.StringVar()
file_label = tk.Label(header_actions, textvariable=file_path_var, font=small_font, bg=COLOR_SURFACE, fg='#64748b')
file_label.pack(anchor='e', pady=(0, 12))

button_row = tk.Frame(header_actions, bg=COLOR_SURFACE)
button_row.pack(anchor='e', pady=(0, 0))

def create_button_hover(btn, normal_bg, hover_bg):
    def on_enter(e):
        btn.config(bg=hover_bg)
    def on_leave(e):
        btn.config(bg=normal_bg)
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)

upload_button = tk.Button(button_row, text='📁 Upload', command=select_file, bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_DARK, font=small_font, relief='flat', padx=20, pady=11, activebackground='#e5e7eb', activeforeground=COLOR_TEXT_DARK)
upload_button.pack(side='left', padx=(0, 14))
create_button_hover(upload_button, COLOR_SURFACE_ALT, '#e5e7eb')

clear_button = tk.Button(button_row, text='🗑️ Clear', command=clear_editor, bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_DARK, font=small_font, relief='flat', padx=20, pady=11, activebackground='#e5e7eb', activeforeground=COLOR_TEXT_DARK)
clear_button.pack(side='left', padx=(0, 14))
create_button_hover(clear_button, COLOR_SURFACE_ALT, '#e5e7eb')

compile_button = tk.Button(button_row, text='▶ Compile', command=run_compiler, bg=COLOR_PRIMARY, fg='white', font=font.Font(family='Segoe UI', size=10, weight='bold'), relief='flat', padx=24, pady=11, activebackground=COLOR_SECONDARY, activeforeground='white')
compile_button.pack(side='left')
create_button_hover(compile_button, COLOR_PRIMARY, COLOR_SECONDARY)

divider = tk.Frame(main_frame, bg=COLOR_BORDER, height=1)
divider.pack(fill='x', padx=32, pady=(16, 20))

# Workspace
workspace_frame = tk.Frame(main_frame, bg=COLOR_SURFACE)
workspace_frame.pack(fill='both', expand=True, padx=32, pady=(0, 24))
workspace_frame.columnconfigure(0, weight=1)
workspace_frame.columnconfigure(1, weight=1)

# Code Editor Panel
editor_panel = tk.Frame(workspace_frame, bg=COLOR_SURFACE)
editor_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 16), pady=0)

editor_header = tk.Frame(editor_panel, bg=COLOR_SURFACE)
editor_header.pack(fill='x', pady=(0, 16))

editor_title = tk.Label(editor_header, text='💻 Code Editor', font=section_font, bg=COLOR_SURFACE, fg=COLOR_TEXT_DARK)
editor_title.pack(anchor='w')

editor_subtitle = tk.Label(editor_header, text='Write your C code with syntax highlighting support.', font=body_font, bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT)
editor_subtitle.pack(anchor='w', pady=(8, 0))

editor_canvas = tk.Frame(editor_panel, bg='#f9fafb', bd=1, relief='solid', highlightbackground=COLOR_BORDER, highlightthickness=1)
editor_canvas.pack(fill='both', expand=True)

line_numbers = tk.Text(editor_canvas, width=5, padx=10, pady=12, bg='#f3f4f6', fg='#9ca3af', bd=0, state='disabled', font=code_font)
line_numbers.pack(side='left', fill='y')

editor_text = tk.Text(editor_canvas, wrap='none', font=code_font, bg=COLOR_SURFACE, fg=COLOR_TEXT_DARK, insertbackground=COLOR_PRIMARY, bd=0, padx=16, pady=12)
editor_text.pack(side='left', fill='both', expand=True)

editor_scroll = ttk.Scrollbar(editor_canvas, orient='vertical', command=sync_scroll)
editor_scroll.pack(side='right', fill='y')
editor_text.configure(yscrollcommand=lambda *args: (editor_scroll.set(*args), line_numbers.yview_moveto(args[0])))
line_numbers.configure(yscrollcommand=editor_scroll.set)

editor_text.bind('<KeyRelease>', update_line_numbers)
editor_text.bind('<<Paste>>', update_line_numbers)
editor_text.bind('<MouseWheel>', update_line_numbers)
editor_text.bind('<Button-1>', update_line_numbers)

# Output Panel
output_panel = tk.Frame(workspace_frame, bg=COLOR_SURFACE)
output_panel.grid(row=0, column=1, sticky='nsew', padx=(16, 0), pady=0)

output_header = tk.Frame(output_panel, bg=COLOR_SURFACE)
output_header.pack(fill='x', pady=(0, 16))

output_title = tk.Label(output_header, text='📊 Analysis Output', font=section_font, bg=COLOR_SURFACE, fg=COLOR_TEXT_DARK)
output_title.pack(anchor='w')

output_subtitle = tk.Label(output_header, text='View compilation results and feedback across 3 stages.', font=body_font, bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT)
output_subtitle.pack(anchor='w', pady=(8, 0))

style = ttk.Style()

# Custom notebook styling
style.theme_use('clam')
style.configure('TNotebook', background=COLOR_SURFACE, borderwidth=0, padding=0)
style.configure('TNotebook.Tab', padding=[16, 12], background=COLOR_SURFACE_ALT, foreground=COLOR_TEXT_LIGHT, font=('Segoe UI', 10, 'bold'), borderwidth=0)
style.map('TNotebook.Tab', 
    background=[('selected', COLOR_SURFACE), ('!selected', COLOR_SURFACE_ALT)], 
    foreground=[('selected', COLOR_PRIMARY), ('!selected', COLOR_TEXT_LIGHT)],
    relief=[('selected', 'flat')])
style.configure('TNotebook.Label', background=COLOR_SURFACE, foreground=COLOR_TEXT_DARK)

output_notebook = ttk.Notebook(output_panel)
output_notebook.pack(fill='both', expand=True)

output_notebook.add(ttk.Frame(output_notebook), text='🔤 Tokens')
output_notebook.add(ttk.Frame(output_notebook), text='⚠️ Syntax Errors')
output_notebook.add(ttk.Frame(output_notebook), text='🔍 Semantic Analysis')

tokens_tab = output_notebook.nametowidget(output_notebook.tabs()[0])
syntax_tab = output_notebook.nametowidget(output_notebook.tabs()[1])
semantic_tab = output_notebook.nametowidget(output_notebook.tabs()[2])

badge_frame = tk.Frame(tokens_tab, bg=COLOR_SURFACE)
badge_frame.pack(fill='x', padx=18, pady=(14, 12))

valid_badge = tk.Label(badge_frame, text='✓ Valid token', bg='#d1fae5', fg='#065f46', font=badge_font, padx=12, pady=6, relief='flat', bd=1, borderwidth=1, highlightthickness=0)
valid_badge.pack(side='left', padx=(0, 12))

error_badge = tk.Label(badge_frame, text='✗ Error', bg='#fee2e2', fg='#991b1b', font=badge_font, padx=12, pady=6, relief='flat', bd=1, borderwidth=1, highlightthickness=0)
error_badge.pack(side='left', padx=(0, 12))

warning_badge = tk.Label(badge_frame, text='⚠ Warning', bg='#fef3c7', fg='#92400e', font=badge_font, padx=12, pady=6, relief='flat', bd=1, borderwidth=1, highlightthickness=0)
warning_badge.pack(side='left')

panel_style = {'bg': COLOR_SURFACE, 'fg': COLOR_TEXT_DARK, 'font': code_font, 'bd': 0, 'insertbackground': COLOR_PRIMARY, 'wrap': 'none'}

tokens_panel = scrolledtext.ScrolledText(tokens_tab, **panel_style)
tokens_panel.pack(fill='both', expand=True, padx=16, pady=(0, 16))

syntax_panel = scrolledtext.ScrolledText(syntax_tab, **panel_style)
syntax_panel.pack(fill='both', expand=True, padx=16, pady=(0, 16))

semantic_panel = scrolledtext.ScrolledText(semantic_tab, **panel_style)
semantic_panel.pack(fill='both', expand=True, padx=16, pady=(0, 16))

tokens_panel.insert(tk.END, '// Compile results will appear here...')
syntax_panel.insert(tk.END, 'Waiting for compilation...')
semantic_panel.insert(tk.END, 'Waiting for compilation...')

tokens_panel.config(state='disabled')
syntax_panel.config(state='disabled')
semantic_panel.config(state='disabled')

status_frame = tk.Frame(main_frame, bg=COLOR_SURFACE_ALT, bd=1, relief='solid', highlightbackground=COLOR_BORDER, highlightthickness=1)
status_frame.pack(fill='x', padx=32, pady=(0, 20))

status_label = tk.Label(status_frame, text='✓ Ready to compile. Upload or write your C code.', font=small_font, bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT)
status_label.pack(side='left', padx=18, pady=14)

footer_label = tk.Label(main_frame, text='🚀 Professional Mini C Compiler IDE | Lexer • Parser • Semantic Analyzer', font=small_font, bg=COLOR_SURFACE, fg='#9ca3af')
footer_label.pack(pady=(0, 20))

root.mainloop()
