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

pagination = api.model(
    'Page Model', {
        'page': fields.Integer(
            description='Number of this page of results'),
        'per_page': fields.Integer(
            description='Number of items per page of results'),
        'total_pages': fields.Integer(
            description='Total number of pages of results'
        ),
        'total_items': fields.Integer(
            description='Total number of results'),
        'next_page': fields.String(),
        'prev_page': fields.String()
    }
)

customers_list = api.inherit('Page of customers', pagination, {
    'customers': fields.List(fields.Nested(customer_model))
})

ns_customers = api.namespace('customers', description='Customers')

parser = reqparse.RequestParser()
parser.add_argument('page', 1, type=int, location='args', required=False)
parser.add_argument('per_page', 10, type=int, location='args', required=False)


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
    @api.expect(parser, validate=True)
    @api.marshal_list_with(customers_list, skip_none=True, code=200)
    def get(self):
        args = parser.parse_args()
        per_page = min(args['per_page'], 100)
        page = args['page']
        query = Customer.to_collection_dict(Customer.query, page, per_page)
        data = {
            'customers': query['items'],
            'page': page,
            'per_page': per_page,
            'total_pages': query['_meta']['total_pages'],
            'total_items': query['_meta']['total_items'],
        }
        if query['has_next']:
            data.update(
                {
                    'next_page': api.url_for(
                        CustomersService, page=page + 1, per_page=per_page)
                }
            )
        if query['has_prev']:
            data.update(
                {
                    'prev_page': api.url_for(
                        CustomersService, page=page - 1, per_page=per_page)
                }
            )
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
