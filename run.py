from flask import Flask
import asyncio

from betting_app.utils import read_config

config = read_config()

app = Flask(__name__)

with app.app_context():
    # Import routes
    import betting_app.routes

if __name__ == "__main__":
    asyncio.run(betting_app.routes.main())
    app.run(host=config['SETTINGS']['HOST'],
            port=config['SETTINGS']['PORT'],
            threaded=config['SETTINGS']['THREADED'],
            debug=config['SETTINGS']['DEBUG'],
            #ssl_context=('cert.pem', 'key.pem'))
            #ssl_context=('nginx-selfsigned.crt', 'nginx-selfsigned.key')
            )