from unoserver.client import UnoClient

uno_client = UnoClient()

def convert_file(file: bytes, convert_to: str) -> bytes:
    return uno_client.convert(indata=file, convert_to=convert_to, outpath=None)
