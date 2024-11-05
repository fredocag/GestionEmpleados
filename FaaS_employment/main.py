import functions_framework
from google.cloud import firestore
from flask import jsonify, abort, make_response

# Inicializa el cliente de Firestore
db = firestore.Client(project="laboratory4-440522", database="roles-permission-db")

@functions_framework.http
def roles_permissions_api(request):
    # Verifica el método HTTP de la solicitud
    if request.method == 'POST':
        # Crear un nuevo rol o permiso
        data = request.get_json()
        if not data or 'id' not in data or 'details' not in data:
            abort(400, description="Bad Request: Missing 'id' or 'details' in request data.")
        
        doc = db.collection("roles_permissions").document(data['id'])
        doc.set(data['details'])
        return make_response(jsonify({"message": f"Role/Permission with id={data['id']} created!"}), 201)
    
    elif request.method == 'GET':
        # Obtener un rol o permiso por ID
        role_permission_id = request.args.get('id')
        if not role_permission_id:
            abort(400, description="Bad Request: Missing 'id' parameter.")
        
        doc = db.collection("roles_permissions").document(role_permission_id).get()
        if not doc.exists:
            abort(404, description=f"Role/Permission with id={role_permission_id} not found.")
        
        return jsonify({"id": role_permission_id, "details": doc.to_dict()})
    
    elif request.method == 'PUT':
        # Actualizar un rol o permiso existente
        data = request.get_json()
        if not data or 'id' not in data or 'details' not in data:
            abort(400, description="Bad Request: Missing 'id' or 'details' in request data.")
        
        doc = db.collection("roles_permissions").document(data['id'])
        if not doc.get().exists:
            abort(404, description=f"Role/Permission with id={data['id']} not found.")
        
        doc.update(data['details'])
        return make_response(jsonify({"message": f"Role/Permission with id={data['id']} updated!"}), 200)
    
    elif request.method == 'DELETE':
        # Eliminar un rol o permiso
        role_permission_id = request.args.get('id')
        if not role_permission_id:
            abort(400, description="Bad Request: Missing 'id' parameter.")
        
        doc = db.collection("roles_permissions").document(role_permission_id)
        if not doc.get().exists:
            abort(404, description=f"Role/Permission with id={role_permission_id} not found.")
        
        doc.delete()
        return make_response(jsonify({"message": f"Role/Permission with id={role_permission_id} deleted!"}), 200)
    
    else:
        # Método no permitido
        abort(405, description="Method Not Allowed")
