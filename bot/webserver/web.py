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

@get('/preview')
@inject
def get_image(dbservice: DbService = Provide[DbContainer.service]):
    id = request.query['id']

    with dbservice.Session() as session:
        card = session.query(Card).filter(Card.id == id).first()
        print(card.description)
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
        input_data["image_card"] = PIL.Image.open(BytesIO(card.image.bin))
        output = CardConstructor(input_data)
        response.set_header('Content-type', 'image/png')
        output_card = output.generateCard()
        return BytesIO(base64.b64decode(output_card))

    return "done"



def start():


    run(host='0.0.0.0', port=Env.web_port)