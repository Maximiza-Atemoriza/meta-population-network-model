import hashlib

C64KB = 65536

def hash_file(file, chunk_size=C64KB):
    sha1 = hashlib.sha1()

    with open(file, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()
