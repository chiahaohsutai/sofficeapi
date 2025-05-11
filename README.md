# sofficeapi

**sofficeapi** is a lightweight, FastAPI-based service that converts common office document formats (like DOCX, XLSX, and PPTX) to PDF using LibreOffice in headless mode. It leverages unoserver to communicate with LibreOffice and is designed for high availability, scalability, and ease of deployment.

This application manages multiple LibreOffice instances running in listener mode and dispatches conversion requests via unoserver. It also includes crash detection and automatic recovery, ensuring minimal downtime and reliable performance—even when LibreOffice becomes unstable.

**Features**

- Convert documents to PDF (DOCX, XLSX, PPTX, and more)
- RESTful API interface via FastAPI
- Automatic LibreOffice instance management with crash recovery
- Lightweight and serverless-friendly
- Docker-ready for easy containerization and deployment
- MyPy and Flake8 compliant

**How It Works**

1. FastAPI handles incoming HTTP requests and routing.
2. Each request is passed to a unoserver client, which interfaces with a running LibreOffice listener instance.
3. LibreOffice performs the conversion in headless mode and returns the result.
4. The converted file is returned as a Base64-encoded PDF in the response.
5. The system monitors all LibreOffice instances and automatically restarts any that crash or hang.

**Requirements**

- Python 3.9+
- LibreOffice (with soffice CLI)
- Docker (optional, for containerization)

## Local Installation

To run this API successfully, `unoserver` must be installed and run using the same Python interpreter that LibreOffice uses internally. If not, the `unoserver` command will fail to connect to LibreOffice. This typically means locating the Python interpreter bundled with LibreOffice and running `pip install unoserver` from that environment. For detailed instructions, refer to the `unoserver` [documentation](https://github.com/unoconv/unoserver).

After installing unoserver, you also need to set an environment variable named SOFFICE_PYTHONPATH. This variable should point to the path of the Python interpreter used by LibreOffice, which is required for the application to locate and use the correct environment during runtime.

```bash
# Add the required enviorment variables
export SOFFICE_PYTHONPATH=... # MacOS/Linux (Zsh/Bash)
$Env:SOFFICE_PYTHONPATH=...   # Windows (Powershell)

# Clone the repository and change directory to the project root
git clone <repository-url>
cd sofficeapi

# Create a new virtual environment
python -m venv .venv

# Activate the environment
. .venv/bin/activate   # MacOS/Linux (Zsh/Bash)
.venv/scripts/activate # Windows (Powershell)

# Install the project dependencies
pip install uv
uv sync --no-dev

# Start the web server
uv run fastapi run ./src/app.py
```

Visit the [Swagger](http://localhost:8000/api/docs#/) page to see all available endpoints and the required payloads for each enpoint
