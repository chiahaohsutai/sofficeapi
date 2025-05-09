from contextlib import contextmanager
from typing import Generator
import os

from box import Box
from unoserver.client import UnoClient

PORTS = os.environ.get("SOFFICE_PORTS")
assert PORTS, "SOFFICE_PORTS not set in .env file"

PORTS = PORTS.split(",")
workers = [Box({"client": UnoClient(port=p), "load": 0}) for p in PORTS]


@contextmanager
def uno_worker(size: int) -> Generator[UnoClient, None, None]:
    worker = min(workers, key=lambda x: x.load)
    worker.load += size
    try:
        yield worker.client
    finally:
        worker.load -= size


def convert_file(file: bytes, convert_to: str) -> bytes:
    with uno_worker(len(file)) as uno_client:
        return uno_client.convert(indata=file, convert_to=convert_to, outpath=None)
