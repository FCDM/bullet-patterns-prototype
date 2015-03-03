class DanMaklParserError(Exception):
	"""Exception raised during parsing of a DanMakl file."""

	def __init__(self, msg, file_name):
		super(DanMaklParserError, self).__init__(
			("Unable to parse DanMakl file %s. " + msg) % file_name)