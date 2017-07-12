import pytest
from deploy_message import generate_message, MessageData
from deploy_message import generate

expected_message = r"""Dear Scott,

A new install package is ready for SCCM deployment.

Filename: DS Hathi Trust Validate-amd64.msi
Location: \\files.library.illinois.edu\groupfiles\Digital Content Creation\SCCM Upload\


The target hostnames:
- LIBSTFDCC02 (413)
- LIBSTFDCC03 (413)
- LIBSTFDCC04 (413)
- LIBSTFDCC06 (413)
- LIBSTFDCC08 (413)
- LIBSTFDCC09 (lab)
- LIBSTFDCC013 (lab)

The package has passed the msiexec silent install test.

This is an automated message but if you have questions, please contact Henry Borchers at hborcher@illinois.edu.

Thank you for your time.
"""

yml_data = """deployer:
  name: Scott
package:
  filename: DS Hathi Trust Validate-amd64.msi
  path: \\\\files.library.illinois.edu\groupfiles\Digital Content Creation\SCCM Upload\\
maintainer:
  name: Henry Borchers
  email: hborcher@illinois.edu
deployment:
  hostnames:
    - LIBSTFDCC02
    - LIBSTFDCC03
    - LIBSTFDCC04
    - LIBSTFDCC06
    - LIBSTFDCC08
    - LIBSTFDCC09
    - LIBSTFDCC013
"""
@pytest.fixture(scope="session")
def yml_file(tmpdir_factory):
    tmp_yml_file = tmpdir_factory.mktemp("sample").join("sample.yml")
    print(tmp_yml_file)
    with open(tmp_yml_file, "w", encoding="utf8") as w:
        w.write(yml_data)
    return str(tmp_yml_file)


def test_generate_message():
    message = MessageData()
    message.receiver_name = "Scott"
    message.package_filename = "DS Hathi Trust Validate-amd64.msi"
    message.package_path = "\\\\files.library.illinois.edu\groupfiles\Digital Content Creation\SCCM Upload\\"
    message.maintainer_name = "Henry Borchers"
    message.maintainer_email = "hborcher@illinois.edu"
    message.deployment_hostnames = ["LIBSTFDCC02 (413)",
                                    "LIBSTFDCC03 (413)",
                                    "LIBSTFDCC04 (413)",
                                    "LIBSTFDCC06 (413)",
                                    "LIBSTFDCC08 (413)",
                                    "LIBSTFDCC09 (lab)",
                                    "LIBSTFDCC013 (lab)"]
    for generated_line, expected_line in zip(generate_message(message).split("\n"), expected_message.split("\n")):
        assert generated_line == expected_line


def test_get_yml(yml_file):
    print(type(yml_file))
    with open(yml_file) as f:
        print(f.read())
    data = generate.get_message_data(yml_file)
    assert isinstance(data, MessageData)
    assert data.receiver_name == "Scott"
    assert data.package_filename == "DS Hathi Trust Validate-amd64.msi"
    assert data.package_path == "\\\\files.library.illinois.edu\groupfiles\Digital Content Creation\SCCM Upload\\"
    assert data.maintainer_name == "Henry Borchers"
    assert data.maintainer_email == "hborcher@illinois.edu"
    assert isinstance(data.deployment_hostnames, list)

    for hostname in data.deployment_hostnames:
        assert hostname in ["LIBSTFDCC02",
                            "LIBSTFDCC03",
                            "LIBSTFDCC04",
                            "LIBSTFDCC06",
                            "LIBSTFDCC08",
                            "LIBSTFDCC09",
                            "LIBSTFDCC013"]
