from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId 
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonreact'
mongo = PyMongo(app)

CORS(app) # Middleware para poder interactuar entre este servidor y el de React

db = mongo.db.pythonreact

# CREACIÓN DE RUTAS PARA PODER HACER EL CRUD
# Ruta para crear un usuario
@app.route('/users', methods=['POST'])
def createUser():
    print(request.json)
    id = db.insert_one({
        'name': request.json['name'],
        'lastname': request.json['lastname'],
        'email': request.json['email'],
        'nacionality': request.json['nacionality'],
        'password': request.json['password']
    })
    print(str(id.inserted_id))
    return jsonify(str(id.inserted_id))

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'lastname': doc['lastname'],
            'email': doc['email'],
            'nacionality': doc['nacionality'],
            'password': doc['password'],
        })
    return jsonify(users)

# Ruta para obtener un usuario
@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({
        '_id':ObjectId(id)
    })
    if user:
        return jsonify({
            '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'lastname': user['lastname'],
            'email': user['email'],
            'nacionality': user['nacionality'],
            'password': user['password']
        })
    else:
        return jsonify('Usuario no encontrado', 404)

# Ruta para eliminar un usuario
@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    user = db.find_one({
        '_id': ObjectId(id)
    })
    if user:
        nombre = user.get('name', 'N/A')
        try:
            result = db.delete_one({
                '_id': ObjectId(id)
            })
            if result.deleted_count == 1:
                return jsonify('Usuario ' + nombre + ' ha sido eliminado')
            else:
                return jsonify('Usuario no encontrado', 404)
        except Exception as e:
            return jsonify('Error al eliminar el usuario: ' + str(e), 500)
    else:
        return jsonify('Usuario no encontrado', 404)

# Ruta para actualizar un usuario
@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    user = db.find_one({
        '_id': ObjectId(id)
    })
    if user:
        nombre = user.get('name', 'N/A')
        try:
            db.update_one({'_id': ObjectId(id)}, {"$set": {
                'name': request.json['name'],
                'lastname': request.json['lastname'],
                'email': request.json['email'],
                'nacionality': request.json['nacionality'],
                'password': request.json['password']
            }})
            return jsonify('Usuario '+ nombre +' actualizado')
        except Exception as e:
            return jsonify('Error al editar el usuario: ' + str(e), 500)
    else:
        return jsonify('Usuario no encontrado', 404)
    
if __name__ == "__main__":
    app.run(debug=True)



