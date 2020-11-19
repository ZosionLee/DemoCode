"""
ASGI config for django3 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import click
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django3.settings')

application = get_asgi_application()

@click.command()
@click.option('-h','--host', 'host',default='127.0.0.1',show_default=True)
@click.option('-p','--port', 'port',default=8000,show_default=True)
def main(host,port,app=application):
    import uvicorn
    uvicorn.run(app, host=host,port=port)

if __name__ == '__main__':
    main()