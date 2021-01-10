

def testing_imports():
	import dictmagic

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

	flattened = dictmagic.flatten(original)

	should_be_same_as_original = dictmagic.unflatten(flattened)
	print('original:\t',original)
	print('flattened:\t',flattened)
	# print(should_be_same_as_original)

	assert str(original) == str(should_be_same_as_original)

	print('tests passed! but actually there arent any real tests yet! proceed with caution!')

if __name__ == "__main__":
	testing_imports()