from flask import Flask, render_template, request, jsonify
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
COMPILER_SOURCE_FILES = [BASE_DIR / "y.tab.c", BASE_DIR / "lex.yy.c"]
COMPILER_BINARY_NAME = "compiler.exe" if os.name == "nt" else "compiler"
COMPILER_BINARY_PATH = BASE_DIR / COMPILER_BINARY_NAME

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

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
}""",
}


def ensure_compiler_binary() -> Path:
    source_mtime = max(source.stat().st_mtime for source in COMPILER_SOURCE_FILES)
    if COMPILER_BINARY_PATH.exists() and COMPILER_BINARY_PATH.stat().st_mtime >= source_mtime:
        return COMPILER_BINARY_PATH

    missing_sources = [source.name for source in COMPILER_SOURCE_FILES if not source.exists()]
    if missing_sources:
        raise FileNotFoundError(
            "Missing compiler sources: " + ", ".join(missing_sources) + ". "
            "Render needs y.tab.c and lex.yy.c in the project root."
        )

    build_command = [
        "gcc",
        "-std=c99",
        "-w",
        str(COMPILER_SOURCE_FILES[0]),
        str(COMPILER_SOURCE_FILES[1]),
        "-lm",
        "-o",
        str(COMPILER_BINARY_PATH),
    ]

    build_result = subprocess.run(
        build_command,
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )

    if build_result.returncode != 0:
        error_text = build_result.stderr.strip() or build_result.stdout.strip() or "Failed to build compiler binary"
        raise RuntimeError(error_text)

    return COMPILER_BINARY_PATH


def run_compiler(code: str) -> dict:
    compiler_path = ensure_compiler_binary()

    result = subprocess.run(
        [str(compiler_path)],
        input=code,
        text=True,
        capture_output=True,
        timeout=10,
    )

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    tokens_output = []
    syntax_output = []
    semantic_output = []
    current_section = "tokens"

    for line in stdout.splitlines():
        if "******stage 1******" in line:
            current_section = "tokens"
            continue
        if "******stage 3******" in line:
            current_section = "syntax"
            continue
        if "ERROR:" in line or "semantic" in line.lower():
            semantic_output.append(line)
            continue
        if current_section == "tokens":
            tokens_output.append(line)
        elif current_section == "syntax":
            syntax_output.append(line)
        else:
            tokens_output.append(line)

    if stderr:
        syntax_output.append(stderr)

    if not tokens_output:
        tokens_output = [stdout or "No compiler output available."]

    if not syntax_output:
        syntax_output = ["✓ No syntax errors detected."]

    if not semantic_output:
        semantic_output = ["✓ No semantic errors detected."]

    return {
        "tokens": "\n".join(tokens_output).strip(),
        "syntax": "\n".join(syntax_output).strip(),
        "semantic": "\n".join(semantic_output).strip(),
    }


@app.route("/")
def index():
    return render_template("index.html", samples=SAMPLES)


@app.route("/api/compile", methods=["POST"])
def compile_code():
    try:
        data = request.get_json(force=True, silent=True) or {}
        code = data.get("code", "").strip()

        if not code:
            return jsonify({"status": "error", "message": "⚠ Please enter C code to compile"}), 400

        outputs = run_compiler(code)
        return jsonify({
            "status": "success",
            "message": "✓ Compilation finished successfully!",
            "tokens": outputs["tokens"] or "No tokens output",
            "syntax": outputs["syntax"],
            "semantic": outputs["semantic"],
        })
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "✗ Compilation timeout (exceeded 10 seconds)"}), 500
    except Exception as exc:
        return jsonify({"status": "error", "message": f"✗ Error: {exc}"}), 500


@app.route("/api/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"status": "error", "message": "No file selected"}), 400

        if not file.filename.endswith(".c"):
            return jsonify({"status": "error", "message": "Only .c files allowed"}), 400

        content = file.read().decode("utf-8", errors="ignore")
        return jsonify({
            "status": "success",
            "message": f"✓ Loaded: {file.filename}",
            "code": content,
        })
    except Exception as exc:
        return jsonify({"status": "error", "message": f"Error: {exc}"}), 500


@app.route("/api/samples/<sample_name>", methods=["GET"])
def get_sample(sample_name):
    if sample_name in SAMPLES:
        return jsonify({"status": "success", "code": SAMPLES[sample_name]})
    return jsonify({"status": "error", "message": "Sample not found"}), 404


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
