from base64 import b64encode, b64decode
from httpx import Client

with open("sample.docx", "rb") as f:
    sample = f.read()
    sample_b64 = b64encode(sample).decode("utf-8")

with Client(base_url="http://localhost:8000") as client:
    response = client.post(
        "/conversions/pdf",
        json={
            "filename": "sample.docx",
            "content": sample_b64,
        },
    )
    if response.status_code == 200:
        print("File converted successfully.")
    else:
        print("Error:", response.json())
    
with open("sample.pdf", "wb") as f:
    f.write(b64decode(response.json()["content"]))
    print("File saved as sample.pdf.")
