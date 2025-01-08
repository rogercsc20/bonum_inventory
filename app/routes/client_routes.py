import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.client_model import Client
from app.schemas.client_schema import ClientSchema
from app.utils.decorators import role_required

logger = logging.getLogger(__name__)
client_blp = Blueprint(
    "clients",
    "clients",
    url_prefix="/clients",
    description="Operations on clients"
)


@client_blp.route("/")
class ClientList(MethodView):
    @jwt_required()
    @client_blp.arguments(ClientSchema)
    @client_blp.response(201, ClientSchema)
    def post(self, data):
        """Create a new client"""
        try:
            logger.info(f"Creating new client: {data['name']}")
            client = Client(**data)
            db.session.add(client)
            db.session.commit()
            logger.info(f"Client created successfully with ID: {client.id}")
            return client
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating client: {str(e)}")
            return {"error": f"Error creating client: {str(e)}"}, 500

    @jwt_required()
    @role_required("manager", "admin")
    @client_blp.response(200, ClientSchema(many=True))
    def get(self):
        """Retrieve all clients"""
        try:
            clients = Client.query.all()
            logger.info(f"Fetched {len(clients)} clients")
            return clients
        except Exception as e:
            logger.error(f"Error fetching clients: {str(e)}")
            return {"error": f"Error fetching clients: {str(e)}"}, 500


@client_blp.route("/<int:client_id>")
class ClientDetail(MethodView):
    @jwt_required()
    @client_blp.response(200, ClientSchema)
    def get(self, client_id):
        """Retrieve a single client by ID"""
        try:
            client = Client.query.get(client_id)
            if not client:
                logger.warning(f"Client with ID {client_id} not found")
                return {"message": "Client not found"}, 404
            logger.info(f"Fetched client with ID: {client_id}")
            return client
        except Exception as e:
            logger.error(f"Error fetching client: {str(e)}")
            return {"error": f"Error fetching client: {str(e)}"}, 500

    @jwt_required()
    @client_blp.arguments(ClientSchema(partial=True))
    @client_blp.response(200, ClientSchema)
    def put(self, data, client_id):
        """Update an existing client"""
        try:
            logger.info(f"Updating client with ID: {client_id}")
            client = Client.query.get(client_id)
            if not client:
                logger.warning(f"Client with ID {client_id} not found")
                return {"message": "Client not found"}, 404

            for key, value in data.items():
                setattr(client, key, value)

            db.session.commit()
            logger.info(f"Client with ID {client_id} updated successfully")
            return client
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating client: {str(e)}")
            return {"error": f"Error updating client: {str(e)}"}, 500

    @jwt_required()
    @role_required("manager", "admin")
    def delete(self, client_id):
        """Delete a client by ID"""
        try:
            logger.info(f"Deleting client with ID: {client_id}")
            client = Client.query.get(client_id)
            if not client:
                logger.warning(f"Client with ID {client_id} not found")
                return {"message": "Client not found"}, 404

            db.session.delete(client)
            db.session.commit()
            logger.info(f"Client with ID {client_id} deleted successfully")
            return {"message": f"Client with ID {client_id} deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting client: {str(e)}")
            return {"error": f"Error deleting client: {str(e)}"}, 500
