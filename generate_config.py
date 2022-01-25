from dotenv import load_dotenv
import os
import json
import yaml


def get_template_string(file_name, extention):
    if extention == "json":
        with open(file_name, "r") as f:
            template_load = json.load(f)
        template_string = json.dumps(template_load)
        return template_string
    elif extention == "yaml":
        with open(file_name, 'r') as yml:
            template_load = yaml.safe_load(yml)
        template_string = yaml.safe_dump(template_load)
        return template_string
    else:
        return ""


def main():
    load_dotenv()

    access_token = os.environ["ACCESS_TOKEN"]
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    project_id = os.environ["PROJECT_ID"]

    template_client_secrets = get_template_string(
        "template_client_secrets.json", "json")
    template_credentials = get_template_string(
        "template_credentials.json", "json")
    template_settings = get_template_string(
        "template_settings.yaml", "yaml")

    template_client_secrets_formated = template_client_secrets % (
        client_id, project_id, client_secret)
    template_credentials_formated = template_credentials % (
        access_token, client_id, client_secret, access_token)
    template_settings_formated = template_settings.format(
        client_id, client_secret)

    with open("client_secrets.json", "w") as f:
        f.write(template_client_secrets_formated)
    with open("credentials.json", "w") as f:
        f.write(template_credentials_formated)
    with open("settings.yaml", "w") as f:
        f.write(template_settings_formated)


if __name__ == '__main__':
    main()
