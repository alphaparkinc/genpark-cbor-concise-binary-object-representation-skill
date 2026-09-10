from client import CBORCodec

def main():
    print("=== Testing CBOR (RFC 8949) Codec ===")
    cbor = CBORCodec()
    b_str = cbor.encode("hello")
    print("Encoded 'hello':", list(b_str))
    assert cbor.decode(b_str) == "hello"

    b_lst = cbor.encode([10, "hi"])
    print("Encoded [10, 'hi']:", list(b_lst))
    assert cbor.decode(b_lst) == [10, "hi"]
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
