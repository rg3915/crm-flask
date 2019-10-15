from flask_restplus import Resource, abort
from flask import jsonify, request
from app import db
from app.models import Customer
from app.api import api
from flask_restplus import fields

customer_model = api.model(
    'Customer',
    {
        'id': fields.String(readonly=True),
        'name': fields.String(required=True, example='John'),
    }
)
ns_customers = api.namespace('customers', description='Customers')


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
