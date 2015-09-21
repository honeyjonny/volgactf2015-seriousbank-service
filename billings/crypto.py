from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class BasePaddingProvider(object):
	"""Base class for PKCS7 padding"""
	def __init__(self, block_size):
		self.padd_factory = padding.PKCS7(block_size)

	def inpad(self, data):
		padder = self.padd_factory.padder()
		return padder.update(data) + padder.finalize()

	def unpad(self, pdata):
		unpadder = self.padd_factory.unpadder()
		return  unpadder.update(pdata) + unpadder.finalize()

class TripleDESPaddingProvider(BasePaddingProvider):
	"""PKCS7 Padding provider for 3DES encryption algorithm"""
	def __init__(self):
		super(TripleDESPaddingProvider, self).__init__(64)


class DESCryptor(Cipher):
	"""A wrapper on cryptography.Cipher primitive to construct 3DES crypto provider"""
	def __init__(self, key, iv):
		self.padding_provider = TripleDESPaddingProvider()

		alg = algorithms.TripleDES(key)
		mode = modes.CBC(iv)
		backend = default_backend()
		super(DESCryptor, self).__init__(alg, mode, backend)

	def encrypt(self, plaintext):
		"""Recives a plaintext and returns hex-representation of ciphertext encrypted with 3DES algorithm"""
		_encryptor = self.encryptor()
		padded_pt = self.padding_provider.inpad(plaintext)
		ciphertext = _encryptor.update(padded_pt)
		_encryptor.finalize()
		return ciphertext.encode('hex')


	def decrypt(self, ciphertext):
		"""Recives hex-string of ciphertext and try to decrypt it with 3DES algorithm"""
		_decryptor = self.decryptor()
		padded_pt = _decryptor.update(ciphertext.decode('hex'))
		_decryptor.finalize()
		plaintext = self.padding_provider.unpad(padded_pt)
		return plaintext