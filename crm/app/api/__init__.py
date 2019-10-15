from flask_restplus import Api


api = Api(
    version='1.0.0',
    title='Customers',
    doc='/doc/',
    description='API e-Campus'
)


from app.api import customers, errors
