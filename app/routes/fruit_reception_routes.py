from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask import request
from app.extensions import db
from app.models import FruitReception
from app.schemas.fruit_reception_schema import FruitReceptionSchema
from app.utils.decorators import role_required
from datetime import datetime
import logging
from app.models.client_model import Client

logger = logging.getLogger(__name__)
fruit_reception_blp = Blueprint("fruit_reception", "fruit_reception", description="Operations on fruit reception", url_prefix="/reception")

@fruit_reception_blp.route("/arrival")
class FruitArrival(MethodView):
    @jwt_required()
    @fruit_reception_blp.arguments(FruitReceptionSchema)
    @fruit_reception_blp.response(201, FruitReceptionSchema)
    def post(self, data):
        """Log fruit arrival"""
        try:
            logger.info(f"Logging fruit arrival for client {data['client_name']}")

            client = Client.query.filter_by(name=data["client_name"]).first()
            if not client:
                logger.warning(f"Client with name {data['client_name']} not found")
                return {"message": "Client not found"}, 404

            fruit_arrival = FruitReception(
                client_name=data["client_name"],
                date=data["date"],
                time=data["time"],
                product=data["product"],
                presentation=data["presentation"],
                box_quantity=data["box_quantity"],
                client_id=client.id
            )
            db.session.add(fruit_arrival)
            db.session.commit()
            logger.info(f"Logged fruit arrival successfully: ID {fruit_arrival.id}")
            return fruit_arrival
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error logging fruit arrival: {str(e)}")
            return {"error" : f"Error logging fruit arrival: {str(e)}"}, 500

    @jwt_required()
    @role_required("manager", "admin")
    @fruit_reception_blp.response(200, FruitReceptionSchema(many=True))
    def get(self):
        """Get all info on fruit reception"""
        try:
            arrivals = FruitReception.query.all()
            logger.info(f"Loaded {len(arrivals)} reception records")
            return arrivals
        except Exception as e:
            logger.error(f"Error loading fruit reception data {str(e)}")
            return {"message": f"Error loading fruit reception data {str(e)}"}, 500


@fruit_reception_blp.route("/arrival/<int:id>")
class UpdateFruitArrival(MethodView):
    @jwt_required()
    @fruit_reception_blp.arguments(FruitReceptionSchema(partial=True))
    @fruit_reception_blp.response(200, FruitReceptionSchema)
    def put(self, data, id):
        """Update arrival by ID"""
        try:
            logger.info(f"Updating fruit arrival with ID: {id}")
            fruit_arrival = FruitReception.query.get(id)
            if not fruit_arrival:
                logger.warning(f"Record with ID {id} not found")
                return {"message": "Record not found"}, 404

            # Update fields only if provided
            for key, value in data.items():
                setattr(fruit_arrival, key, value)

            db.session.commit()
            logger.info(f"Updated fruit arrival successfully: ID {fruit_arrival.id}")
            return fruit_arrival
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating fruit arrival: {str(e)}")
            return {"error" : f"Error updating fruit arrival: {str(e)}"}, 500

@fruit_reception_blp.route("/arrival/<int:id>")
class GetFruitArrival(MethodView):
    @jwt_required()
    @fruit_reception_blp.response(200, FruitReceptionSchema)
    def get(self, id):
        """Get info on fruit reception by ID"""
        try:
            arrival = FruitReception.query.get(id)
            if not arrival:
                logger.warning(f"Record with ID {id} not found")
                # Explicitly serialize the 404 response
                return{"message": "Record not found"}, 404
            logger.info(f"Loaded reception data of ID: {id}")
            return arrival  # Will be serialized by FruitReceptionSchema
        except Exception as e:
            logger.error(f"Error loading fruit reception data: {str(e)}")
            return {"message": f"Error loading fruit reception data: {str(e)}"}, 500



@fruit_reception_blp.route("/delete/<int:reception_id>")
class DeleteFruitReception(MethodView):
    @jwt_required()
    @role_required("manager", "admin")
    def delete(self, reception_id):
        """Delete a fruit reception record by ID"""
        try:
            record = FruitReception.query.get(reception_id)
            if not record:
                return {"message": "Record not found"}, 404

            db.session.delete(record)
            db.session.commit()
            logger.info(f"Deleted fruit reception record with ID {reception_id}")
            return {"message": f"Record with ID {reception_id} deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting record with ID {reception_id }: {str(e)}")
            return {"message": f"Error deleting record: {str(e)}"}, 500



@fruit_reception_blp.route("/filter")
class FilterFruitReception(MethodView):
    @jwt_required()
    @role_required("manager", "admin")
    def get(self):
        """Filter fruit reception by date range"""
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        client_id = request.args.get("client_id")

        if not start_date or not end_date:
            return {"message": "Start and end dates are required"}, 400

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            start_date = datetime.combine(start_date, datetime.min.time())
            end_date = datetime.combine(end_date, datetime.max.time())

            query = FruitReception.query.filter(
                FruitReception.date >= start_date,
                FruitReception.date <= end_date
            )

            if client_id:
                query = query.filter(FruitReception.client_id == client_id)

            # Execute the query
            records = query.all()


            logger.info(f"Fetched {len(records)} filtered records")
            return {
                "data": FruitReceptionSchema(many=True).dump(records)
            }, 200
        except ValueError as e:
            logger.error(f"Invalid date format: {str(e)}")
            return {"message": "Invalid date format. Use 'YYYY-MM-DD'."}, 400