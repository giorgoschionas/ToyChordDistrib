import hashlib

def sha1(msg):
    digest = hashlib.sha1(msg.encode())
    hex_digest= digest.hexdigest()
    return int(hex_digest, 16) % 65536

def between(n1, n2, n3):
    # TODO: added corner case when id == -1
    if n2 == -1:
        return False
    if n1 == -1:
        return True
    # Since it's a circle if n1=n3 then n2 is between
    if n1 < n3:
        return n1 < n2 < n3
    else:
        return n1 < n2 or n2 < n3