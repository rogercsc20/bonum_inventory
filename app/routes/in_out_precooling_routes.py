import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from flask import request
from app.extensions import db
from app.models.in_out_precooling_model import InOutPrecooling
from app.schemas.in_out_precooling_schema import InOutPrecoolingSchema
from app.models.client_model import Client
from app.utils.decorators import role_required
from datetime import datetime
from app.utils.api_responses import create_response


logger = logging.getLogger(__name__)
in_out_precooling_blp = Blueprint(
    "in_out_precooling",
    "in_out_precooling",
    url_prefix="/precooling",
    description="Operations for pre cooling chambers"
)

precooling_schema = InOutPrecoolingSchema()

@in_out_precooling_blp.route("/entry")
class PrecoolingEntry(MethodView):
    @jwt_required()
    @in_out_precooling_blp.arguments(InOutPrecoolingSchema(partial=True))
    def post(self, data):
        """Log an entry to pre cooling chambers"""
        try:
            logger.info(f"Logging pre cooling entry for client {data.get('client_name')}")

            client = db.session.query(Client).filter_by(name=data["client_name"]).first()
            if not client:
                logger.warning(f"Client with name {data['client_name']} not found")
                return create_response(message=f"Client with name {data['client_name']} not found", status_code=404)

            entry = InOutPrecooling(
                client_id= client.id,
                client_name=data["client_name"],
                date=data["date"],
                product=data["product"],
                presentation=data["presentation"],
                fruit_type=data["fruit_type"],
                pallet_quantity=data.get("pallet_quantity"),
                box_quantity=data["box_quantity"],
                pallet_code=data.get("pallet_code"),
                room_number=data["room_number"],
                entry_time=data["entry_time"],
                entry_temperature=data.get("entry_temperature"),
            )
            db.session.add(entry)
            db.session.commit()
            logger.info(f"Precooling entry logged successfully with ID: {entry.id}")
            return create_response(message="Success", data=precooling_schema.dump(entry), status_code=201)
        except Exception as e:
            db.session.rollback()
            logger.error(f"Fruit type in payload: {data.get('fruit_type')}")
            logger.error(f"Error logging precooling entry: {str(e)}")
            return  create_response(message="Error logging precooling entry", data={str(e)}, status_code=500)

@in_out_precooling_blp.route("/exit/<int:id>")
class PrecoolingExit(MethodView):
    @jwt_required()
    @in_out_precooling_blp.arguments(InOutPrecoolingSchema(partial=True))
    def put(self, data, id):
        """Log an exit from pre cooling chambers"""
        try:
            logger.info(f"Logging pre cooling exit for record ID: {id}")
            entry = InOutPrecooling.query.get(id)
            if not entry:
                logger.warning(f"Record with ID {id} not found")
                return create_response(message=f"Record with ID {id} not found", status_code=404)

            if entry.exit_time:
                logger.warning(f"Exit already logged for record ID: {id}")
                return create_response(message=f"Exit already logged for ID {id}", status_code=400)

            entry.exit_time = data["exit_time"]
            entry.exit_temperature = data.get("exit_temperature")
            db.session.commit()
            logger.info(f"Precooling exit logged successfully for record ID: {id}")
            return create_response(message="Success", data=precooling_schema.dump(entry), status_code=200)
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error logging precooling exit: {str(e)}")
            return create_response(message=f"Internal Server Error: {str(e)}", status_code=500)


@in_out_precooling_blp.route("/update/<int:id>")
class UpdatePrecoolingRecord(MethodView):
    @jwt_required()
    @in_out_precooling_blp.arguments(InOutPrecoolingSchema(partial=True))
    @in_out_precooling_blp.response(200, InOutPrecoolingSchema)
    def patch(self, data, id):
        """Update a precooling record by ID"""
        try:
            logger.info(f"Updating precooling record with ID: {id}")
            record = InOutPrecooling.query.get(id)
            if not record:
                logger.warning(f"Record with ID {id} not found")
                return {"message": "Record not found"}, 404

            # Update provided fields only
            for key, value in data.items():
                setattr(record, key, value)

            db.session.commit()
            logger.info(f"Precooling record with ID {id} updated successfully")
            return record
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating precooling record: {str(e)}")
            return {"error": f"Error updating record: {str(e)}"}, 500


@in_out_precooling_blp.route("/records")
class RetrievePrecoolingRecords(MethodView):
    @jwt_required()
    @role_required("manager", "admin")
    @in_out_precooling_blp.response(200, InOutPrecoolingSchema(many=True))
    def get(self):
        """Retrieve pre cooling records with optional filters"""
        client_id = request.args.get("client_id")
        product = request.args.get("product")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        try:
            query = InOutPrecooling.query

            if client_id:
                query = query.filter_by(client_id=client_id)
            if product:
                query = query.filter_by(product=product)
            if start_date and end_date:
                try:
                    # Parse both dates
                    start_date = datetime.strptime(start_date, "%d/%m/%y").date()
                    end_date = datetime.strptime(end_date, "%d/%m/%y").date()
                except ValueError:
                    return {"error": "Invalid date format. Use 'DD/MM/YY' for both start_date and end_date."}, 400

                # Apply date range filter
                query = query.filter(InOutPrecooling.date.between(start_date, end_date))

            records = query.all()
            logger.info(f"Fetched {len(records)} precooling records")
            return records
        except Exception as e:
            logger.error(f"Error fetching precooling records: {str(e)}")
            return {"error": f"Error fetching records: {str(e)}"}, 500


@in_out_precooling_blp.route("/record/<int:id>")
class RetrieveSinglePrecoolingRecord(MethodView):
    @jwt_required()
    @role_required("manager", "admin")
    @in_out_precooling_blp.response(200, InOutPrecoolingSchema)
    def get(self, id):
        """Retrieve a single precooling record by ID"""
        try:
            logger.info(f"Fetching precooling record with ID: {id}")
            record = InOutPrecooling.query.get(id)
            if not record:
                logger.warning(f"Record with ID {id} not found")
                return {"message": "Record not found"}, 404

            logger.info(f"Fetched precooling record with ID {id}")
            return record
        except Exception as e:
            logger.error(f"Error fetching record with ID {id}: {str(e)}")
            return {"error": f"Error fetching record: {str(e)}"}, 500


@in_out_precooling_blp.route("/delete/<int:id>")
class DeletePrecoolingRecord(MethodView):
    @jwt_required()
    @role_required("manager", "admin")
    def delete(self, id):
        """Delete a pre cooling record by ID"""
        try:
            logger.info(f"Attempting to delete pre cooling record with ID: {id}")
            record = InOutPrecooling.query.get(id)
            if not record:
                logger.warning(f"Record with ID {id} not found")
                return {"message": "Record not found"}, 404

            db.session.delete(record)
            db.session.commit()
            logger.info(f"Precooling record with ID {id} deleted successfully")
            return {"message": f"Record with ID {id} deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting precooling record: {str(e)}")
            return {"error": f"Error deleting record: {str(e)}"}, 500
