import os
import logging
from flask import Flask
from flask_restful import Api
import config
from common.key_vault import KeyVaultSecret
from common import AADToken
from controllers import GitHubFileController

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger('werkzeug')
#logger.setLevel(logging.ERROR)

#============================== AAD Token ==========================================
AAD_IDENTITY_TENANT = os.environ['AAD_IDENTITY_TENANT']
AAD_IDENTITY_CLIENTID = os.environ['AAD_IDENTITY_CLIENTID']
AAD_IDENTITY_SECRET = os.environ['AAD_IDENTITY_SECRET']
key_vault_token = AADToken(AAD_IDENTITY_CLIENTID, AAD_IDENTITY_SECRET, 'https://vault.azure.net', tenant=AAD_IDENTITY_TENANT)
#===================================================================================


#============================== GitHub secret from KeyVault ========================
secret = KeyVaultSecret(config.KeyVaultName, config.GitHubSecretName, key_vault_token)
github_token = secret.get()
#===================================================================================

#============================== Register controllers ===============================

api.add_resource(GitHubFileController, '/<repo>/<path:path>', endpoint="github_file", resource_class_args=(logger, github_token))
#===================================================================================

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)