from .error import DanMaklParserError
from .component import ComponentParser
from .. import Bullet

class BulletParser:

	@staticmethod
	def parse(self, bullet_element, file_name):
		""" Build a bullet class from a bullet element in the DanMakl tree."""

		# Attempt to get the name of the bullet.
		try:
			name = bullet_element.attrib["name"]
		except KeyError:
			pass

		try:
			name = bullet_element.findall("name")[0].text
		except IndexError:
			raise DanMaklParserError(
				'"bullet" element must have attribute "name" or child "name".',
				file_name)

		components = bullet_element.findall("component")
		built_components = []
		for component in components:
			# Build the component. NOT YET IMPLEMENTED
			pass

		class _bullet(Bullet):

			COMPONENTS = components

		_bullet.__name__ = name
		return name, _bullet