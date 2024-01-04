from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
        return jsonify(messages), 200, {'Content-Type': 'application/json'}
    
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(message)
        db.session.commit()

        return jsonify(message.to_dict()), 201, {'Content-Type': 'application/json'}

@app.route('/messages/<int:id>', methods = [ 'GET', 'PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'GET':
        message_dict = message.to_dict()

        response = make_response(jsonify(message_dict),200)
      

    elif request.method == 'PATCH':
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
            db.session.commit()

        message_dict = message.to_dict()
        response = make_response(jsonify(message_dict), 200)


    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {"delete_successful":True}
        response = make_response(jsonify(response_body),200)
    
    response.headers['Content-Type'] = 'application/json'
    return response
    

if __name__ == '__main__':
    app.run(port=5555)
