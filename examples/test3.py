a = '''Фото: @kirillovmr f
ef

ef

'''
author_caption = '''Спасибо за фото {}
⠀
Отмечай на фото @rich_kherson или ставь хештег #rich_kherson и попадай к нам в ленту!
⠀
#херсон #kherson #украина #top_kherson_people #лето'''

alt_caption = '''Солнечный привет от @rich_kherson !
⠀
Отмечай на фото @rich_kherson или ставь хештег #rich_kherson и попадай к нам в ленту!
⠀
#херсон #kherson #украина #top_kherson_people #лето'''

# Return @username or -1
def return_author(your_text):
    if your_text.find("@") != -1:
        index1 = your_text.find("@")
        new_text = your_text[index1:]
        index = []
        if new_text.find(" ") != -1:
            index.append(new_text.find(" ")) # simple space
        if new_text.find("⠀") != -1:
            index.append(new_text.find("⠀")) # insta space
        if new_text.find("\n") != -1:
            index.append(new_text.find("\n"))# enter

        if(len(index) > 0):
            index = sorted(index)
            new_text = new_text[:index[0]]
        return new_text
    else:
        return -1

# Return edited caption
def edit_caption(your_text):
    author = return_author(your_text)
    if author != -1:
        caption = author_caption.format(author)
    else:
        caption = alt_caption
    return caption

print(edit_caption(a))
