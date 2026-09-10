class CBORCodec:
    """
    CBOR (RFC 8949) Binary Codec.
    Encodes and decodes self-describing compact binary structures.
    """
    def encode(self, val):
        if isinstance(val, int):
            if val >= 0:
                if val < 24:
                    return bytes([val])
                elif val <= 0xFF:
                    return bytes([24, val])
                else:
                    return bytes([25]) + val.to_bytes(2, "big")
            else:
                neg = -1 - val
                return bytes([0x20 | (neg if neg < 24 else 24)])
        elif isinstance(val, str):
            b = val.encode("utf-8")
            if len(b) < 24:
                return bytes([0x60 | len(b)]) + b
            return bytes([0x78, len(b)]) + b
        elif isinstance(val, list):
            header = bytes([0x80 | len(val)]) if len(val) < 24 else bytes([0x98, len(val)])
            return header + b"".join(self.encode(x) for x in val)
        return b""

    def decode(self, data):
        major = data[0] >> 5
        add = data[0] & 0x1F
        if major == 0:
            return add if add < 24 else data[1]
        elif major == 3:
            slen = add if add < 24 else data[1]
            start = 1 if add < 24 else 2
            return data[start:start+slen].decode("utf-8")
        elif major == 4:
            count = add
            idx = 1
            res = []
            for _ in range(count):
                sub_major = data[idx] >> 5
                sub_add = data[idx] & 0x1F
                if sub_major == 0:
                    res.append(sub_add)
                    idx += 1
                elif sub_major == 3:
                    res.append(data[idx+1:idx+1+sub_add].decode("utf-8"))
                    idx += 1 + sub_add
            return res
        return None
