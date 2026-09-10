import sys
import json
import base64
from client import CBORCodec

def main():
    cbor = CBORCodec()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "encode":
            b = cbor.encode(params.get("val"))
            res = {"bytes_b64": base64.b64encode(b).decode()}
        elif method == "decode":
            raw = base64.b64decode(params.get("bytes_b64", "").encode())
            res = {"val": cbor.decode(raw)}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
