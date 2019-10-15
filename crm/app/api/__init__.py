from flask_restplus import Api


api = Api(
    version='1.0.0',
    title='Customers',
    doc='/doc/',
    description='CRM Api'
)


from app.api import customers, errors
