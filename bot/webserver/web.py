import base64
from io import BytesIO
import PIL
from bottle import Bottle, route, request 
from models.models import Card
import models
from models.dbcontainer import DbContainer, DbService
from dependency_injector.wiring import Provide, inject
from envvars import Env
from bottle import route, run, template, post, get, response
from discord.drawutils import DrawUtils
import math
from cardmaker import CardConstructor

@post('/image')
@inject
def upload_image(dbservice: DbService = Provide[DbContainer.service]):
    image = models.Image()
    print(request.files.get("image"))
    image.bin = request.files.get("image").file.read()
    image.label = request.forms.get("label")

    with dbservice.Session() as session:
        session.add(image)
        session.commit()

    return "done"

@get('/card')
@inject
def get_card(dbservice: DbService = Provide[DbContainer.service]):
    id = request.query['id']

    with dbservice.Session() as session:
        card = session.query(Card).filter(Card.id == id).first()
        response.set_header('Content-type', 'image/png')
        return DrawUtils.card_to_byte_image(card)

    return "done"

@get('/summon')
@inject
def get_summon(dbservice: DbService = Provide[DbContainer.service]):
    id = request.query['id']

    with dbservice.Session() as session:
        card = session.query(Card).filter(Card.id == id).first()
        response.set_header('Content-type', 'image/gif')
        return DrawUtils.summon(card)

    return "done"

@get('/cards')
@inject
def get_cards(dbservice: DbService = Provide[DbContainer.service]):
    ids: List[str] = request.query['ids'].split(',')
    with dbservice.Session() as session:
        cards = session.query(Card).filter(Card.id.in_(ids)).all()
        response.set_header('Content-type', 'image/png')
        grid = (math.ceil(math.sqrt(len(cards))), math.ceil(math.sqrt(len(cards))))
        inv_img =  DrawUtils.draw_inv_card_spread(cards, (1600,1200), grid, True)
        buffered = BytesIO()
        inv_img.save(buffered, format="PNG")
        return BytesIO(buffered.getvalue())

    return "done"

def start():


    run(host='0.0.0.0', port=Env.web_port)