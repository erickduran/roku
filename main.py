from src.lexical.lexical_analyser import LexicalAnalyser


def main():
	analyser = LexicalAnalyser()
	analyser.load_categories('src/lexical/lexical_categories.json')
	analyser.parse_input('test_source.fang')


if __name__ == '__main__':
	main()
