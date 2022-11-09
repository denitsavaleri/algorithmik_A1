class ImageHash:
	"""
	Hash encapsulation. Can be used for dictionary keys and comparisons.
	"""

	def __init__(self, binary_array):
		# type: (NDArray) -> None
		self.hash = binary_array  # type: NDArray

	def __str__(self):
		return _binary_array_to_hex(self.hash.flatten())

	def __repr__(self):
		return repr(self.hash)

	def __sub__(self, other):
		# type: (ImageHash) -> int
		if other is None:
			raise TypeError('Other hash must not be None.')
		if self.hash.size != other.hash.size:
			raise TypeError('ImageHashes must be of the same shape.', self.hash.shape, other.hash.shape)
		return numpy.count_nonzero(self.hash.flatten() != other.hash.flatten())

	def __eq__(self, other):
		# type: (object) -> bool
		if other is None:
			return False
		return numpy.array_equal(self.hash.flatten(), other.hash.flatten())  # type: ignore

	def __ne__(self, other):
		# type: (object) -> bool
		if other is None:
			return False
		return not numpy.array_equal(self.hash.flatten(), other.hash.flatten())  # type: ignore

	def __hash__(self):
		# this returns a 8 bit integer, intentionally shortening the information
		return sum([2**(i % 8) for i, v in enumerate(self.hash.flatten()) if v])

	def __len__(self):
		# Returns the bit length of the hash
		return self.hash.size

def dhash(image, hash_size=8):
	# type: (Image.Image, int) -> ImageHash
	"""
	Difference Hash computation.

	following http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

	computes differences horizontally

	@image must be a PIL instance.
	"""
	# resize(w, h), but numpy.array((h, w))
	if hash_size < 2:
		raise ValueError('Hash size must be greater than or equal to 2')

	image = image.convert('L').resize((hash_size + 1, hash_size), ANTIALIAS)
	pixels = numpy.asarray(image)
	# compute differences between columns
	diff = pixels[:, 1:] > pixels[:, :-1]
	return ImageHash(diff)
