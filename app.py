import json
import os
import re
import urlexpander
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import cafe_api
from forms import CafeForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
google_api = os.environ.get('GOOGLE_API')

engine = create_engine(os.environ.get('DATABASE_URL'), connect_args={'check_same_thread': False})
cafe_api.BaseORM.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes/<c_id>')
@app.route('/cafes', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cafes(c_id=0):
    if request.method == 'GET':
        city = request.args.get('city')
        cafes_list = cafe_api.get_cafes(db_session, c_id=int(c_id), city=city)
        return json.dumps(cafes_list)
    elif request.method == 'POST':
        post_request = request.json
        cafe_api.add_cafe(db_session, post_request)
        return {'Status': 'Success!'}
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

@app.route('/cafes_page/<city>')
@app.route('/cafes_page')
def cafes_page(city=None):
    if city is None:
        city_name = 'ALL CITIES'
    else:
        city_name = city

    cafes_list = cafe_api.get_cafes(db_session, city=city)

    return render_template('cafes_page.html', city=city_name, cafes_list=cafes_list, google_api=google_api)


@app.route('/cities')
def get_cities():
    cities_list = cafe_api.get_cities(db_session)
    cities_links = [{'city': 'ALL CITIES', 'link': '/cafes_page'}]
    for city in cities_list:
        cities_links.append({'city': city, 'link': '/cafes_page/' + city})
    return json.dumps(cities_links)


@app.route('/cafe/<c_id>')
def cafe(c_id):
    cafe_item = cafe_api.get_cafes(db_session, c_id=int(c_id))[0]
    return render_template('cafe.html', cafe=cafe_item)


@app.route('/add_cafe')
def add_cafe():
    cafe_form = CafeForm()
    return render_template('add_cafe.html', edit_form=cafe_form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/unpack_google_url')
def unpack_google_url():
    try:
        short_url = request.args.get('short_url')
        response_url = urlexpander.expand(short_url)
        pattern = '@(\-?\d+.\d+),(\-?\d+.\d+)'
        res = re.search(pattern, response_url)
        if res is not None:
            result = {'lat': res.group(1), 'lng': res.group(2), 'status': 'OK'}
        else:
            result = {'status': 'unable to parse', 'url': response_url}
        return json.dumps(result)
    except Exception as e:
        result = {'status': 'error', 'description': str(e)}
        return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
