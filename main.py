from unoserver.client import UnoClient

uno_client = UnoClient()

in_file = "sample.docx"
out_file = "sample.pdf"

def main():
    uno_client.convert(inpath=in_file, outpath=out_file, convert_to="pdf")

if __name__ == "__main__":
    main()
