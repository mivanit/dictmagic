import unittest
import dictmagic

class TestDictmagic(unittest.TestCase):

	def testing_basic(self):
		
		original = {
			'a' : 1,
			'b' : 2,
			'c' : {
				'x' : 42,
				'y' : 'a string',
				'z' : {
					'asdf' : [1, 2, 3],
					'qwerty' : 3.1415,
				}
			},
		}

		flat_expected = {
			'a' : 1,
			'b' : 2,
			'c/x' : 42,
			'c/y' : 'a string',
			'c/z/asdf' : [1, 2, 3],
			'c/z/qwerty' : 3.1415,
		}

		flattened = dictmagic.flatten(original)
		self.assertEqual(str(flattened), str(flat_expected))
		should_be_same_as_original = dictmagic.unflatten(flattened)
		self.assertEqual(str(original), str(should_be_same_as_original))
		self.assertEqual(str(original), str(dictmagic.unflatten(flat_expected)))


	def testing_duplication(self):
		
		for dup_key_repl in ['None', '', '_']:
			dupeDict_flat = { 'a' : 'val1', 'a/b' : 'val2' }

			dupeDict_unflat = { 'a' : { dup_key_repl : 'val1', 'b' : 'val2' } }

			test_unflat = dictmagic.unflatten(
				dupeDict_flat,
				except_dup_key = False,
				dup_key_repl = dup_key_repl,
			)

			self.assertEqual(str(dupeDict_unflat), str(test_unflat))
		
	def testing_duplication_except(self):
		
		for dup_key_repl in [None, 'None', '', '_', -1]:
			dupeDict_flat = { 'a' : 'val1', 'a/b' : 'val2' }

			try:
				test_unflat = dictmagic.unflatten(dupeDict_flat, dup_key_repl = dup_key_repl)

				self.assertTrue(False, 'did not except on duplicate!')
			except KeyError:
				pass


if __name__ == "__main__":
	unittest.main()