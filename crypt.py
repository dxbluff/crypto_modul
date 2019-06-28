import os, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt_file(key: bytes, in_filename: str, out_filename=None, chunksize=64*1024) -> None:
	""" Encrypts a file using AES (CBC mode) with the
		given key.

	key:
    		The encryption key - a bytes object that must be
    		either 16, 24 or 32 bytes long. Longer keys
		are more secure.

	in_filename:
		Name of the input file

	out_filename:
		If None, '<in_filename>.enc' will be used.

	chunksize:
		Sets the size of the chunk which the function
		uses to read and encrypt the file. Larger chunk
		sizes can be faster for some files and machines.
		chunksize must be divisible by 16.
	"""
	if not out_filename:
		out_filename = in_filename + ".enc"

	iv = bytes(random.getrandbits(8) for _ in range(16))
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	filesize = os.path.getsize(in_filename)

	with open(in_filename, "rb") as infile:
		with open(out_filename, "wb+") as outfile:
			outfile.write(filesize.to_bytes(8, "big"))
			outfile.write(iv)

			for chunk in iter(lambda: infile.read(chunksize), b""):
				if len(chunk) % 16 != 0:
					chunk += b"\x00" * (15 - (len(chunk) % 16))
					chunk += b"\x01" * (16 - (len(chunk) % 16))
				outfile.write(encryptor.encrypt(chunk))
	return


def decrypt_file(key: bytes, in_filename: str, out_filename=None, chunksize=24*1024) -> None:
	""" Decrypts a file using AES (CBC mode) with the
		given key.

	key:
    		The encryption key - a bytes object that must be
    		either 16, 24 or 32 bytes long. Longer keys
		are more secure.

	in_filename:
		Name of the input file

	out_filename:
		If None, '<in_filename>' without extension will be used.

	chunksize:
		Sets the size of the chunk which the function
		uses to read and encrypt the file. Larger chunk
		sizes can be faster for some files and machines.
		chunksize must be divisible by 16.	
	"""
	if not out_filename:
		out_filename = os.path.splitext(in_filename)[0]

	with open(in_filename, 'rb') as infile:
		origsize = int.from_bytes(infile.read(8), "big")
		iv = infile.read(16)
		decryptor = AES.new(key, AES.MODE_CBC, iv)

		with open(out_filename, 'wb+') as outfile:
			for chunk in iter(lambda: infile.read(chunksize), b""):
				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(origsize)


def hash(data: bytes) -> bytes:
	""" Returns 32 bytes long hash of a given data
	"""
	return SHA256.new(data=data).digest()


if __name__ == "__main__":
	key = "Privet suki"
	key = hash(key.encode())
	print("key:", key)
	print("key len", len(key))
	encrypt_file(key, "disk.img")
	decrypt_file(key, "disk.img.enc", "disk.img.bak")
	print(hash(b"token") == hash(b"token"))
	
