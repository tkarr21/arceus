from PIL import Image, ImageOps


def coloring_img(img, type):
    color = None
    if type == 'normal':
        color = 'tan'
    elif type == 'fire':
        color = 'red'
    elif type == 'water':
        color = 'cornflowerblue'
    elif type == 'grass':
        color = 'seagreen'
    elif type == 'electric':
        color = 'goldenrod'
    elif type == 'ice':
        color = 'darkturquoise'
    elif type == 'fighting':
        color = 'brown'
    elif type == 'poison':
        color = 'DarkMagenta'
    elif type == 'ground':
        color = 'peru'
    elif type == 'flying':
        color = 'rosybrown'
    elif type == 'psychic':
        color = 'palevioletred'
    elif type == 'bug':
        color = 'olivedrab'
    elif type == 'rock':
        color = 'darkgoldenrod'
    elif type == 'ghost':
        color = 'rebeccapurple'
    elif type == 'dark':
        color = 'darkslategrey'
    elif type == 'dragon':
        color = 'mediumslateblue'
    elif type == 'steel':
        color = 'lightslategray'
    elif type == 'fairy':
        color = 'salmon'

    # applying grayscale method
    gray_image = ImageOps.grayscale(img)

    # background coloring and pasting gray
    background = Image.new('RGBA', gray_image.size, color)
    background.paste(gray_image, (0, 0), gray_image)

    img.show()
    gray_image.show()
    background.show()


def main():
    # creating an og_image object
    og_image = Image.open("./assets/pokemon/1.png")

    types = ['normal', 'fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison',
             'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dark', 'dragon', 'steel', 'fairy']

    coloring_img(og_image, types[9])


if __name__ == "__main__":
    main()
