import xml.etree.ElementTree

from .error import DanMaklParserError
from .bullet import BulletParser

class DanMaklParser:

	def __init__(self, file_name):
		self._file_name = file_name
		self._tree = xml.etree.ElementTree(file_name)

		root = self._tree.getroot()
		if root.tag != "danmakl":
			raise DanMaklParserError(
				'Root tag must be "danmakl".', file_name)
		self._root = root

	def parse_definitions(self):
		"""Get all the bullet definitions in the DanMakl file."""

		bullets = {}

		for definitions in self._root.findall("definitions"):

			for child in definitions:
				# NOTE: Expect this to change in the future to support other definitions.
				if child.tag != "bullet":
					raise DanMaklParserError(
						'"definitions" element must contain only "bullet" children.',
						self._filename)

				name, bullet = BulletParser.parse(child, self._file_name)
				bullets[name] = bullet

		return bullets

	def parse_timeline(self):
		pass

	def _build_pattern(self, pattern_element):
		pass


