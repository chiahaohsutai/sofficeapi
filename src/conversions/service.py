import asyncio
from contextlib import contextmanager
from datetime import datetime as dt
from datetime import timezone
from os import environ
from subprocess import Popen, TimeoutExpired
from typing import Generator

from unoserver.client import UnoClient

XMLRPC_PORTS = environ.get("XMLRPC_PORTS", "2000,2001,2002,2003")
SOFFICE_PORTS = environ.get("SOFFICE_PORTS", "3000,3001,3002,3003")

SOFFICE_PYTHOPATH = environ.get("SOFFICE_PYTHONPATH")
assert SOFFICE_PYTHOPATH, "MIssing SOFFICE_PYTHONPATH environment variable"

PORTS = XMLRPC_PORTS.split(",")
WORKERS = [{"client": UnoClient(port=p), "load": 0} for p in PORTS]


@contextmanager
def least_loaded_uno_worker(size: int) -> Generator[UnoClient, None, None]:
    worker = min(WORKERS, key=lambda x: x["load"])
    worker["load"] += size
    try:
        yield worker["client"]
    finally:
        worker["load"] -= size


def convert_file(file: bytes, convert_to: str) -> bytes:
    with least_loaded_uno_worker(len(file)) as worker:
        return worker.convert(indata=file, convert_to=convert_to, outpath=None)


class LibreOfficeInstance:

    def __init__(
        self,
        xmlrpc_port: int = 2003,
        soffice_port: int = 2002,
        conversion_timeout: int = 60,
    ):
        self.xmlrpc_port = xmlrpc_port
        self.soffice_port = soffice_port
        self.conversion_timeout = conversion_timeout
        self.process = None
        self.last_heartbeat = dt.now(timezone.utc)

    def start(self):
        self.process = Popen(
            [
                SOFFICE_PYTHOPATH,
                "-m",
                "unoserver.server",
                "--port",
                str(self.xmlrpc_port),
                "--uno-port",
                str(self.soffice_port),
                "--conversion-timeout",
                str(self.conversion_timeout),
                "--quiet",
            ]
        )
        self.last_heartbeat = dt.now(timezone.utc)

    def is_alive(self):
        if self.process is None:
            return False
        return self.process.poll() is None

    def restart(self):
        self._terminate_process()
        self.start()

    def stop(self):
        self._terminate_process()
        self.process = None

    def _terminate_process(self):
        if self.process is None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=30)
        except TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=30)
        except Exception:
            pass


class LibreOfficeManager:
    def __init__(
        self,
        xmlrpc_ports: list[int],
        soffice_ports: list[int],
        check_interval: int = 10,
        conversion_timeout: int = 60,
    ):
        self.instances = [
            LibreOfficeInstance(xmlrpc_port, uno_port, conversion_timeout)
            for xmlrpc_port, uno_port in zip(xmlrpc_ports, soffice_ports)
        ]
        self.check_interval = check_interval
        self._monitor_task = None

    async def start_all(self):
        for instance in self.instances:
            instance.start()
        self._monitor_task = asyncio.create_task(self._monitor_instances())

    def stop_all(self):
        if self._monitor_task is not None:
            self._monitor_task.cancel()
        for instance in self.instances:
            instance.stop()

    async def _monitor_instances(self):
        while True:
            for instance in self.instances:
                if not instance.is_alive():
                    instance.restart()
            await asyncio.sleep(self.check_interval)
