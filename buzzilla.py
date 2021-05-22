from urllib.request import urlopen
from html.parser import HTMLParser
import collections


# words parser class
class WordsParser(HTMLParser):
	# tags to search text within
	search_tags = ['p', 'div', 'span', 'a', 'h1', 'h2', 'h2', 'h3', 'h4']

	# current tag
	current_tag = ''

	# common word list
	common_words = {}

	# handle starting tag
	def handle_starttag(self, tag, attr):
		# store current tag
		self.current_tag = tag

	# handle tag's data
	def handle_data(self, data):
		# make sure current tag matches search tags
		if self.current_tag in self.search_tags:
			# loop over word list within current tag
			for word in data.strip().split():
				# convert word to lowercase and filter characters
				common_word = word.lower()
				common_word = common_word.replace('.', '')
				common_word = common_word.replace(':', '')
				common_word = common_word.replace(',', '')
				common_word = common_word.replace('"', '')
				common_word = common_word.replace('?', '')
				common_word = common_word.replace('-', '')

				# filter words
				if (
						len(common_word) > 1 and
						# common_word not in ['של', 'עוד', 'את'] and
						common_word[0].isalpha()
						and '/' not in common_word
				):
					word_len = len(common_word)

					try:
						# try to update count of a given word if available
						if self.common_words.get(word_len) is None:
							self.common_words[word_len] = {}
						self.common_words[word_len][common_word] += 1

					except:
						# store current common word
						self.common_words[word_len].update({common_word: 1})


# main driver
if __name__ == '__main__':
	# target URL to scrape
	urls = ['https://he.wikipedia.org/', 'https://www.ynet.co.il/', 'http://www.talniri.co.il/']
	for url in urls:

		# make HTTP GET request to the target URL
		response = urlopen(url)
		# print(response.getcode())

		# extract HTML document from response
		html = response.read().decode('utf-8', errors='ignore')

		# create words parser instance
		words_parser = WordsParser()

		# feed HTML to words parser
		words_parser.feed(html)

		# count common words with counter
	for k in sorted(WordsParser.common_words.keys()):
		words_count = collections.Counter(WordsParser.common_words[k])

		# extract [number] of most common words
		most_common = words_count.most_common(1)

		# loop over most common words
		for word, count in most_common:
			print('length', len(word), ':', word)
