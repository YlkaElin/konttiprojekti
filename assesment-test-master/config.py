

def access_secrets(project_id, secret_id, version_id):

    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """
    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    payload = response.payload.data.decode("UTF-8")
    return payload


# if __name__ == "__main__":
#     access_secrets("fall-week7-2", "database", "latest")
#     access_secrets("fall-week7-2", "username", "latest")
#     access_secrets("fall-week7-2", "password", "latest")

 # parsitaan database.ini tiedoston sisältö ja palautetaan se

# from configparser import ConfigParser

# def configmodule(filename='database.ini', section='postgresql'):
#     parser = ConfigParser()
#     parser.read(filename)
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise
#       Exception('Section {0} not found in the {1} file'.format(section, filename))
#     return db