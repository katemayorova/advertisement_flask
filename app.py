from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy import Column, Integer, DateTime, String, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
import atexit

DSN = 'postgresql://postgres:1qaz!QAZ@127.0.0.1:5432/advertisement'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
app = Flask('app')
Base = declarative_base()


class Advertisement(Base):

    __tablename__ = 'advertisement'

    id = Column(Integer, primary_key=True)
    header = Column(String(120))
    description = Column(String)
    date_creat = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all(engine)


def on_exit():
    engine.dispose()


atexit.register(on_exit)


def get_advertisement(advertisement_id: int, session) -> Advertisement:
    advertisement = session.query(Advertisement).get(advertisement_id)
    return advertisement


class AdvertisementViews(MethodView):
    def get(self, advertisement_id: int):
        with Session() as session:
            advertisement = get_advertisement(advertisement_id, session)
            return jsonify({'owner': advertisement.owner, 'header': advertisement.header})

    def post(self):
        json_data = request.json
        with Session() as session:
            new_advertisement = Advertisement(owner=json_data['owner'], header=json_data['header'],
                                              description=json_data['description'])
            session.add(new_advertisement)
            session.commit()

            return jsonify({'owner': new_advertisement.owner})

    def delete(self, advertisement_id):

        with Session() as session:
            advertisement = get_advertisement(advertisement_id, session)
            session.delete(advertisement)
            session.commit()
        return jsonify({'status': 'success'})


app.add_url_rule('/advertisement/', methods=['POST'], view_func=AdvertisementViews.as_view('create_advertisement'))
app.add_url_rule('/advertisement/<int:advertisement_id>', methods=['GET', 'DELETE'], view_func=AdvertisementViews.as_view('get_advertisement'))
app.run()
