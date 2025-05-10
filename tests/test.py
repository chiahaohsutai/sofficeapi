import asyncio
from base64 import b64decode, b64encode
from datetime import datetime as dt
from datetime import timezone
from os import path
from pathlib import Path

from httpx import AsyncClient, Timeout

cwd = path.dirname(path.abspath(__file__))
sample_path = path.join(cwd, "samples", "sample.docx")

with open(sample_path, "rb") as f:
    sample = f.read()
    sample_b64 = b64encode(sample).decode("utf-8")


async def convert(client: AsyncClient, filename: str, content: str, persist: bool):
    payload = {"filename": filename, "content": content}
    response = await client.post("/conversions/pdf", json=payload)

    if response.status_code == 200:
        print(f"Conversion successful for {filename}.")
        now = dt.now(timezone.utc).isoformat()

        if persist:
            name = f"converted_{Path(filename).stem}_{now}.pdf"
            with open(name, "wb") as f:
                f.write(b64decode(response.json()["content"]))
                print(f"File saved as {name}")
    else:
        print(f"Error converting {filename}: {response.json()}")


async def main():
    timeout = Timeout(30.0, connect=30.0)
    async with AsyncClient(base_url="http://localhost:8000", timeout=timeout) as client:
        tasks = []
        for i in range(30):
            task = convert(client, f"sample_{i}.docx", sample_b64, False)
            tasks.append(task)

        await asyncio.gather(*tasks)


# Run the async main function to start the test
if __name__ == "__main__":
    asyncio.run(main())
