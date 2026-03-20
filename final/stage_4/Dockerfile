FROM python:3.14-slim

RUN pip install --no-cache-dir jupyterhub configurable-http-proxy jupyterlab

EXPOSE 8000

WORKDIR /srv/jupyterhub

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]