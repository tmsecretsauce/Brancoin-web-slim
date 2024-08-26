from io import BytesIO
import os
from typing import List
from models.models import Card
from PIL import Image, ImageDraw, ImageOps, ImageSequence
from cardmaker import CardConstructor
import requests

class DrawUtils:
    @staticmethod
    def card_to_byte_image(card: Card):
        input_data = {
            "card": card.card_style,
            "Title": card.title,
            "attribute": card.attribute,
            "Level": int(card.level),
            "Type": card.type,
            "Descripton": str(card.description).replace('\\n','\n'),
            "Atk": card.atk,
            "Def": card.defe
        }
        image_response = requests.get(card.image.discord_url)
        input_data["image_card"] = Image.open(BytesIO(image_response.content))
        output = CardConstructor(input_data)
        output_card = output.generateCard()
        return BytesIO(output_card)
    
    @staticmethod 
    def summon(card: Card):
        im = Image.open(os.path.dirname(__file__) + f"/../assets/summon.gif")
        frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
        for idx, frame in enumerate(frames):
            if idx > len(frames) - 4:
                card_size = (250, 270)
                pos = (60,-15)
                card_image = DrawUtils.card_to_image(card)
                card_image = card_image.resize(card_size)

                width, height = card_image.size
                m = -0.5
                xshift = abs(m) * width
                new_width = width + int(round(xshift))
                card_image = card_image.transform((new_width, height), Image.AFFINE,
                        (1, m, -xshift if m > 0 else 0, 0, 1, 0), Image.BICUBIC)
                
                card_image = card_image.rotate(15, expand=1)

                frame.paste(card_image, pos, card_image)
                
        buffered = BytesIO()
        frames[0].save(buffered, format="GIF", save_all=True, append_images=frames[1:])
        return BytesIO(buffered.getvalue())

    @staticmethod
    def card_to_image(card: Card):
        return Image.open(DrawUtils.card_to_byte_image(card))
    
    @staticmethod
    def draw_inv_card_spread(cards: List[Card], bg_size, card_grid, draw_blanks, bg = "inventorybg.jpg"):
        spread = Image.open(os.path.dirname(__file__) + f"/../assets/{bg}")
        spread = spread.resize(bg_size)
        
        margin_x = 20
        margin_y = 20

        draw = ImageDraw.Draw(spread)   
        rect_size = (int(bg_size[0]/card_grid[0] - (margin_x*1.5)), int(bg_size[1]/card_grid[1] - (1.5*margin_y)))

        card_idx = 0
        for y in range(card_grid[1]):
            for x in range(card_grid[0]):
                top_left_x = rect_size[0]*x + margin_x*(x+1)
                top_left_y = rect_size[1]*y + margin_y*(y+1)

                bot_right_x = top_left_x + rect_size[0]
                bot_right_y = top_left_y + rect_size[1]
                pos = (top_left_x, top_left_y, bot_right_x, bot_right_y)
                if card_idx < len(cards) or draw_blanks:
                    image_card = DrawUtils.card_to_image(cards[card_idx]) if card_idx < len(cards) else DrawUtils.card_to_image(cards[0])
                    image_bg = Image.new('RGBA', (image_card.size[0] + 20, image_card.size[1] + 20), (203, 189, 147))
                    if card_idx < len(cards):
                        image_bg.paste(image_card, (10, 10))
                    image_sized = ImageOps.contain(image_bg, rect_size)

                    gap_x = rect_size[0] - image_sized.size[0]
                    gap_y = rect_size[1] - image_sized.size[1]

                    spread.paste(image_sized, (top_left_x + int(gap_x/2), top_left_y + int(gap_y/2)))
                card_idx += 1

        return spread