from typing import Type
import unittest
import dictmagic

class TestDictmagic(unittest.TestCase):

	def basic(self):
		
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


	def duplication(self):
		
		for dup_key_repl in ['None', '', '_']:
			dupeDict_flat = { 'a' : 'val1', 'a/b' : 'val2' }

			dupeDict_unflat = { 'a' : { dup_key_repl : 'val1', 'b' : 'val2' } }

			test_unflat = dictmagic.unflatten(
				dupeDict_flat,
				except_dup_key = False,
				dup_key_repl = dup_key_repl,
			)

			self.assertEqual(str(dupeDict_unflat), str(test_unflat))
		
	def duplication_except(self):
		
		for dup_key_repl in [None, 'None', '', '_', -1]:
			dupeDict_flat = { 'a' : 'val1', 'a/b' : 'val2' }

			try:
				test_unflat = dictmagic.unflatten(dupeDict_flat, dup_key_repl = dup_key_repl)

				self.assertTrue(False, 'did not except on duplicate!')
			except KeyError:
				pass

	
	def nonstring_keys(self):
		original = {
			1010101 : 1,
			(1,1,2,3,5,8) : 2,
			'c' : {
				'x' : 42,
				'y' : 'a string',
				'z' : {
					None : [1, 2, 3],
					'qwerty' : 3.1415,
				}
			},
		}

		flat_expected = {
			'1010101' : 1,
			'(1,1,2,3,5,8)' : 2,
			'c/x' : 42,
			'c/y' : 'a string',
			'c/z/None' : [1, 2, 3],
			'c/z/qwerty' : 3.1415,
		}

		# when no exception
		flattened_noexcept = dictmagic.flatten(original, except_nonstr_key = False)
		self.assertEqual(str(flattened_noexcept), str(flat_expected))

		# reverting to unflattened would not work
		# if this feature is needed, probably import a safe YAML parser or something

		try:
			flattened_except = dictmagic.flatten(original, except_nonstr_key = True)

			self.assertTrue(False, 'did not except on duplicate!')
		except TypeError:
			pass



if __name__ == "__main__":
	unittest.main()