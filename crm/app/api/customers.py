from flask import jsonify, request, url_for
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import Customer


@bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    return jsonify(Customer.query.get_or_404(id).to_dict())


@bp.route('/customers', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Customer.to_collection_dict(
        Customer.query, page, per_page, 'api.get_customers')
    return jsonify(data)


@bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name fields')
    if Customer.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    customer = Customer()
    customer.from_dict(data)
    db.session.add(customer)
    db.session.commit()
    response = jsonify(customer.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_customer', id=customer.id)
    return response


@bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json() or {}
    if 'customer' in data and data['name'] != customer.name and \
            Customer.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    customer.from_dict(data)
    db.session.commit()
    return jsonify(customer.to_dict())


@bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Success'})
