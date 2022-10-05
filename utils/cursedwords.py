
class CursedWords:

    def readerCursedWords(self) -> list:
        try:
            file_read = open('./utils/cursedwords.txt', 'r', encoding='utf-8')
            data = file_read.read()
            file_read.close()
            cursedwords_list = data.replace('\n', '').split(',')
            cursedwords_list.pop()
            return cursedwords_list
        except ValueError as e:
            print(e)
            return []

    def writeCursedWords(self, words: list, cursedwords: list) -> list:
        try:
            file_write = open('./utils/cursedwords.txt', 'a', encoding='utf-8')
            for word in words:
                if not (word in cursedwords):
                    file_write.write(word + ',\n')
                    cursedwords.append(word)
            file_write.close()
            return cursedwords
        except ValueError as e:
            print(e)
            return []
