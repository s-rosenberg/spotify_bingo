import re
import os
import requests
import json
from random import sample
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass
from typing import Optional, List, Tuple
from typing_extensions import Self

PATH_IMAGES = 'images/'
FILE_DATA = 'data_spotify.json'
NON_ALPHANUMERIC_CHAR = re.compile(r'[^a-zA-Z\d]')
N_COLUMNS = 4 # fixed n columns
FONT_TYPE = 'fonts/ARIAL.TTF'
BG_COLOR_THUMBNAIL = (55,55,55)
TEXT_COLOR = (255,255,255)
BG_COLOR = (224, 240, 175)
SPACING_BETWEEN_THUMBNAILS = 50
SPACING = 10
HEIGHT = 2100
WIDTH = 1485
Y_OFFSET = HEIGHT // 3

@dataclass
class Song:
    title: str
    artist: str
    image: str

    def save_image_to_disk(self, return_image : bool = False) -> Optional[Image.Image]:
        
        filename = self.get_image_filename()
        
        if not os.path.exists(filename):
            response = requests.get(self.image, stream=True).raw
            img = Image.open(response)
            img.save(filename)
            if return_image:
                return img
            
    def get_image_filename(self, optional_add: Optional[str] = '') -> str:
        filename = NON_ALPHANUMERIC_CHAR.sub('',f'{self.title}{self.artist}')
        return f'{PATH_IMAGES}{filename}{"_" if optional_add != "" else ""}{optional_add}.jpg'
    
    def get_image(self) -> Image.Image:
        filename = self.get_image_filename()
        if os.path.exists(filename):
            return Image.open(filename)
        else:
            return self.save_image_to_disk(return_image=True)

    @classmethod
    def get_song_from_dict(cls, data:dict) -> Self:
        return cls(**data)

    def create_song_thumbnail(self, thumbnail_width: int, font_size: int) -> Image.Image:
        

        def get_thumbnail_height():
            return SPACING * 4 + thumbnail_width + font_size * 2 
        
        thumbnail = Image.new('RGB', (thumbnail_width, get_thumbnail_height()), BG_COLOR_THUMBNAIL)
        thumbnail_draw = ImageDraw.Draw(thumbnail)
        font = ImageFont.truetype(FONT_TYPE, font_size)
        image = self.get_image().resize((thumbnail_width - SPACING * 2, thumbnail_width - SPACING * 2))
        thumbnail.paste(image, (SPACING, SPACING))
        thumbnail_draw.text((SPACING, SPACING * 2 + image.height),self.artist, TEXT_COLOR, font)
        thumbnail_draw.text((SPACING, font_size + SPACING * 3 + image.height), self.title, TEXT_COLOR, font)
       
        return thumbnail

    
@dataclass
class Grid:
    songs: List[Song]
    width: int = WIDTH
    height: int = HEIGHT

    def get_max_text_len(self) -> int:
        all_words_len = []
        for song in self.songs:
            all_words_len.append(len(song.title))
            all_words_len.append(len(song.artist))
        
        return max(all_words_len)
    
    @classmethod
    def get_random_grid(cls, songs:List[Song], n_songs: int) -> Self:
        songs = sample(songs, n_songs)
        return cls(songs)
    
    def show_data(self) -> None:
        for song in self.songs:
            print(song)

    def create_image_grid(self) -> Image.Image:
        max_width = (self.width - SPACING_BETWEEN_THUMBNAILS * (N_COLUMNS - 1) - SPACING * 2) // N_COLUMNS
        font_size = self.get_font_size(max_width)
        card = Image.new('RGB', (self.width, self.height), BG_COLOR)

        for index, song in enumerate(self.songs):
            thumbnail = song.create_song_thumbnail(max_width, font_size + 2)
            thumbnail_width, thumbnail_height = thumbnail.size

            position_x, position_y = self.get_thumbnail_position(index, thumbnail_height, thumbnail_width)
            card.paste(thumbnail, (position_x, position_y))

        return card

    def get_thumbnail_position(self, index: int, height: int, width: int) -> Tuple[int, int]:
        
        n_column = index % N_COLUMNS
        n_row = index // N_COLUMNS

        x = SPACING + n_column * width + SPACING_BETWEEN_THUMBNAILS * n_column
        y = SPACING * n_row + n_row * height + SPACING * n_row + Y_OFFSET

        return x, y

    def get_font_size(self, max_width: int) -> int:
        max_text_len = self.get_max_text_len()
        text = 'A' * max_text_len
        font_size = 1
        font = ImageFont.truetype(FONT_TYPE, size=font_size)
        
        while font.getlength(text) < max_width:
            font_size += 1
            font = ImageFont.truetype(FONT_TYPE, size=font_size)
        
        return font_size

class YisusCard(Grid):
    def get_yisus_bingo_card(self, card_name: str):
        bingo_card = self.create_image_grid()
        bingo_card_draw = ImageDraw.Draw(bingo_card)
        font = ImageFont.truetype(FONT_TYPE, size=150)
        text = "YISUS'S BINGO\n†"
        _, _, w, h = bingo_card_draw.textbbox((0, 0), text, font)
        text_cordinates = ((WIDTH - w)/2, (Y_OFFSET - h) / 2)
        bingo_card_draw.text(text_cordinates, text,(0,0,0), font, align='center')
        
        bingo_card.save(card_name)

if __name__ == '__main__':
    with open(FILE_DATA) as file:
        data = json.load(file)
        all_songs = [Song.get_song_from_dict(song) for song in data]
        for index in range(20):
            filename = f'output/bingo_yisus_{index}.jpg'
            bingo_card = YisusCard.get_random_grid(all_songs, 12)
            bingo_card.get_yisus_bingo_card(filename)

"""
chat gpt

# Datos de ejemplo para las canciones
canciones = [
    {
        "titulo": "Canción 1",
        "artista": "Artista 1",
        "imagen": "imagen1.jpg"
    },
    {
        "titulo": "Canción 2",
        "artista": "Artista 2",
        "imagen": "imagen2.jpg"
    },
    # Agrega más canciones según sea necesario
]

# Dimensiones de la cuadrícula
num_filas = 5
num_columnas = 5
cell_width = 200
cell_height = 200
spacing = 20

# Crear una imagen en blanco
total_width = (cell_width + spacing) * num_columnas + spacing
total_height = (cell_height + spacing) * num_filas + spacing
bg_color = (255, 255, 255)
image = Image.new('RGB', (total_width, total_height), bg_color)
draw = ImageDraw.Draw(image)

# Cargar una fuente para el texto
font = ImageFont.load_default()

# Rellenar la cuadrícula con las canciones
for row in range(num_filas):
    for col in range(num_columnas):
        index = row * num_columnas + col
        if index < len(canciones):
            x = col * (cell_width + spacing) + spacing
            y = row * (cell_height + spacing) + spacing
            draw.rectangle([x, y, x + cell_width, y + cell_height], outline=(0, 0, 0))
            
            cancion = canciones[index]
            draw.text((x + 10, y + 10), f"Título: {cancion['titulo']}", fill=(0, 0, 0), font=font)
            draw.text((x + 10, y + 40), f"Artista: {cancion['artista']}", fill=(0, 0, 0), font=font)
            
            imagen = Image.open(cancion['imagen']).resize((100, 100))
            image.paste(imagen, (x + 50, y + 70))

# Guardar la imagen
image.save("bingo_spotify.png")
image.show()
"""