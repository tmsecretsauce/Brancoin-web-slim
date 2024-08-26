from bottle import Bottle, route, request, response, post, get
from models.models import Card, Image
from models.dbcontainer import DbContainer, DbService
from dependency_injector.wiring import Provide, inject
from envvars import Env
from discord.drawutils import DrawUtils
import math
from io import BytesIO

@post('/image')
@inject
def add_image(dbservice: DbService = Provide[DbContainer.service]):
    label = request.query.get('label')
    discord_url = request.query.get('discord_url')

    image = Image(label=label, discord_url=discord_url)

    with dbservice.Session() as session:
        session.add(image)
        session.commit()

    return "Image reference added successfully"

@get('/card')
@inject
def get_card(dbservice: DbService = Provide[DbContainer.service]):
    id = request.query['id']

    with dbservice.Session() as session:
        card = session.query(Card).filter(Card.id == id).first()
        if card:
            response.set_header('Content-type', 'image/png')
            return DrawUtils.card_to_byte_image(card)
        else:
            response.status = 404
            return "Card not found"

@get('/summon')
@inject
def get_summon(dbservice: DbService = Provide[DbContainer.service]):
    id = request.query['id']

    with dbservice.Session() as session:
        card = session.query(Card).filter(Card.id == id).first()
        if card:
            response.set_header('Content-type', 'image/gif')
            return DrawUtils.summon(card)
        else:
            response.status = 404
            return "Card not found"

@get('/cards')
@inject
def get_cards(dbservice: DbService = Provide[DbContainer.service]):
    ids = request.query['ids'].split(',')
    with dbservice.Session() as session:
        cards = session.query(Card).filter(Card.id.in_(ids)).all()
        if cards:
            response.set_header('Content-type', 'image/png')
            grid = (math.ceil(math.sqrt(len(cards))), math.ceil(math.sqrt(len(cards))))
            inv_img = DrawUtils.draw_inv_card_spread(cards, (1600,1200), grid, True)
            buffered = BytesIO()
            inv_img.save(buffered, format="PNG")
            return BytesIO(buffered.getvalue())
        else:
            response.status = 404
            return "No cards found"

def start():
    run(host='0.0.0.0', port=Env.web_port)