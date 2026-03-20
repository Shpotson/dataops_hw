import os
from jupyterhub.auth import Authenticator

class SimpleAdminAuthenticator(Authenticator):
    async def authenticate(self, handler, data):
        username = data["username"]
        password = data["password"]

        if (
            username == os.environ.get("JUPYTERHUB_ADMIN_USER")
            and password == os.environ.get("JUPYTERHUB_ADMIN_PASSWORD")
        ):
            return {
                "name": username,
            }
        else:
            self.log.warn("Invalid username or password, info: {}, {}".format(username, password))
            return None

c.JupyterHub.authenticator_class = SimpleAdminAuthenticator
port = int(os.environ.get("JUPYTERHUB_PORT", 8000))
c.JupyterHub.port = port

c.JupyterHub.cookie_secret_file = "data/jupyterhub-cookie-secret"
c.JupyterHub.db_url = "sqlite:///jupyterhub.sqlite"

c.Authenticator.admin_users = {os.environ.get("JUPYTERHUB_ADMIN_USER")}
c.Authenticator.allowed_users = {os.environ.get("JUPYTERHUB_ADMIN_USER")}

c.LocalAuthenticator.create_system_users = True
c.PAMAuthenticator.check_account = False

c.JupyterHub.spawner_class = "jupyterhub.spawner.LocalProcessSpawner"
c.Spawner.default_url = "/lab"
c.Spawner.notebook_dir = "/home/{username}"