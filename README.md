# sofficeapi

sofficeapi is a lightweight, serverless-ready API that converts common office document formats (like DOCX, XLSX, and PPTX) to PDF using LibreOffice in headless mode, managed via unoserver, and exposed through a simple FastAPI interface.

**Features**
* ✅ Convert documents to PDF (DOCX, XLSX, PPTX, etc.)
* ✅ RESTful API interface for simple integration
* ✅ Lightweight and suitable for serverless deployment
* ✅ Docker-ready and easy to deploy

**How It Works**
1.	FastAPI handles incoming HTTP requests.
2.	Files are passed to unoserver, which uses LibreOffice in headless mode.
3.	The converted file (e.g., PDF) is returned in the response or saved to disk.

**Requirements**
* Python 3.9+
* LibreOffice (with soffice CLI)
* unoserver
* Docker (optional, for containerization)
