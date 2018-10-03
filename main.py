# main.py
# lexical_analyser.py
"""This is main class for running the roku language compiler.

- TODO

"""
from src.lexical.lexical_analyser import LexicalAnalyser


def main():
	analyser = LexicalAnalyser()
	analyser.load_categories('src/lexical/lexical_categories.json')
	tuples = analyser.parse_input('tests/test_source.fang')

	# just for dev
	for i, element in enumerate(tuples):
		if isinstance(element, tuple):
			print(str(i) + ' token: ' + element[0] + ' value: ' + element[1])
		else:
			print(str(i) + ' token: ' + element)
		

if __name__ == '__main__':
	main()
