from flask import request
from flask_restplus import Resource, abort, fields, reqparse
from app import db
from app.api import api
from app.models import Customer


customer_model = api.model(
    'Customer',
    {
        'id': fields.String(readonly=True),
        'name': fields.String(required=True, example='John'),
    }
)
ns_customers = api.namespace('customers', description='Customers')


pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument(
    'page', type=int, location='args', required=False, default=1
)
pagination_arguments.add_argument(
    'per_page', type=int, location='args', required=False,
    choices=[5, 10, 25, 50, 100], default=5
)


@ns_customers.route('/<int:id>')
class CustomerService(Resource):

    @api.marshal_with(customer_model)
    def get(self, id):
        return Customer.query.get_or_404(id).to_dict()

    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, id):
        customer = Customer.query.get_or_404(id)
        data = request.get_json() or {}
        if 'customer' in data and data['name'] != customer.name and \
                Customer.query.filter_by(name=data['name']).first():
            return abort(400, 'please use a different name')
        customer.from_dict(data)
        db.session.commit()
        return customer.to_dict()

    @api.response(204, 'Customer deleted')
    def delete(self, id):
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return 'Success', 204


@ns_customers.route('/')
class CustomersService(Resource):

    @api.expect(pagination_arguments, validate=True)
    @api.marshal_list_with(customer_model, code=200)
    def get(self):
        data = Customer.query.all()
        return data

    @api.expect(customer_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        data = request.get_json() or {}
        if 'name' not in data:
            return abort(400, 'must include name fields')
        if Customer.query.filter_by(name=data['name']).first():
            return abort(400, 'please use a different name')
        customer = Customer()
        customer.from_dict(data)
        db.session.add(customer)
        db.session.commit()
        return customer.to_dict(), 201
