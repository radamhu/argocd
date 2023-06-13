class Book:
    def __init__(self, title, author, edition):
        self.title = title
        self.title = author
        self.title = edition

    def __str__(self):
        return f'{self.author} {self.title}'


book_1 = Book('A legyek ura', 'William Golding', 2)

print(dir(book_1))
print(dir('alma'))
print('alma'.__dir__())

print(book_1)