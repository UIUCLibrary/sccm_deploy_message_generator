import sys
from jinja2 import Template
import yaml
import warnings
import deploy_message

class MessageData:
    template = """Dear {{ receiver_name }},

A new install package is ready for SCCM deployment.

Filename: {{ package_filename }}

Location: {{ package_path }}


The target hostnames:
{%- for hostname in host_names %}
- {{ hostname }}
{%- endfor %}

The package has passed the msiexec silent install test.

This is an automated message but if you have questions, please contact {{ maintainer_name }} at {{ maintainer_email }}.

Thank you for your time.
"""

    def __init__(self):
        self.receiver_name = None
        self.package_filename = None
        self.package_path = None
        self.maintainer_name = None
        self.maintainer_email = None
        self.deployment_hostnames = None


def generate_message(message: MessageData):
    warnings.warn("generate_body() instead.", DeprecationWarning)
    template = Template(message.template)

    return template.render(
        receiver_name=message.receiver_name,
        package_filename=message.package_filename,
        package_path=message.package_path,
        host_names=message.deployment_hostnames,
        maintainer_name=message.maintainer_name,
        maintainer_email=message.maintainer_email
    )


def generate_body(message: MessageData):
    template = Template(message.template)

    return template.render(
        receiver_name=message.receiver_name,
        package_filename=message.package_filename,
        package_path=message.package_path,
        host_names=message.deployment_hostnames,
        maintainer_name=message.maintainer_name,
        maintainer_email=message.maintainer_email
    )


def get_footer():
    template_message = """Message generated using {{ title }} version {{ version }}.
({{ url }})

"""
    template = Template(template_message)

    return template.render(
        title = deploy_message.__title__,
        version = deploy_message.__version__,
        url= deploy_message.__url__
    )

def get_message_data(yml_file)->MessageData:
    with open(yml_file, "r") as f:
        yml_data = yaml.load(f)
    data = MessageData()
    try:
        deployer = yml_data["deployer"]
        maintainer = yml_data["maintainer"]
        package = yml_data["package"]
        deployment = yml_data["deployment"]

        data.receiver_name = deployer["name"]

        data.package_path = package["path"]
        data.package_filename = package["filename"]

        data.maintainer_email = maintainer["email"]
        data.maintainer_name = maintainer["name"]

        data.deployment_hostnames = deployment['hostnames']


    except KeyError as e:
        print("Invalid YML file {}.".format(yml_file), file=sys.stderr)
        raise
    return data