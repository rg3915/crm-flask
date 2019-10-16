from app import db


class PaginatedAPIMixin(object):

    @staticmethod
    def to_collection_dict(query, page, per_page):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            'has_next': True if resources.has_next else False,
            'has_prev': True if resources.has_prev else False
        }
        return data


class Customer(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, unique=True)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'name': self.name,
        }
        return data

    def from_dict(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])
