import asyncio
from base64 import b64decode, b64encode
from datetime import datetime as dt
from datetime import timezone
from os import path

from httpx import AsyncClient, Timeout

cwd = path.dirname(path.abspath(__file__))
sample_path = path.join(cwd, "samples", "sample.docx")

with open(sample_path, "rb") as f:
    sample = f.read()
    sample_b64 = b64encode(sample).decode("utf-8")


async def send_conversion_request(
    client: AsyncClient, filename: str, content: str, persist: bool = False
):
    response = await client.post(
        "/conversions/pdf",
        json={
            "filename": filename,
            "content": content,
        },
    )
    if response.status_code == 200:
        print(f"Conversion successful for {filename}.")

        now = dt.now(timezone.utc).isoformat()
        if persist:
            with open(f"converted_{filename}_{now}.docx", "wb") as f:
                f.write(b64decode(response.json()["content"]))
        else:
            print(f"File not saved, but conversion was successful for {filename}.")

        print(f"File saved as converted_{filename}.pdf.")
    else:
        print(f"Error converting {filename}: {response.json()}")


async def main():
    timeout = Timeout(30.0, connect=30.0)
    async with AsyncClient(base_url="http://localhost:8000", timeout=timeout) as client:
        tasks = []

        for i in range(30):
            task = send_conversion_request(client, f"sample_{i}.docx", sample_b64)
            tasks.append(task)

        # Run all tasks concurrently
        await asyncio.gather(*tasks)


# Run the async main function to start the test
if __name__ == "__main__":
    asyncio.run(main())
