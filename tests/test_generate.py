import pytest
import deploy_message

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

expected_footer = r"""Message generated using deploy_message version {}.
(https://github.com/UIUCLibrary/sccm_deploy_message_generator)
""".format(deploy_message.__version__)

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
    tmp_yml_file = str(tmpdir_factory.mktemp("sample").join("sample.yml"))
    with open(tmp_yml_file, "w", encoding="utf8") as w:
        w.write(yml_data)
    return str(tmp_yml_file)


def test_generate_message():
    message = deploy_message.MessageData()
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
    for i, (generated_line, expected_line) in enumerate(
            zip(deploy_message.generate_message(message).split("\n"), expected_message.split("\n"))):
        assert generated_line == expected_line, "differences on line {}".format(i + 1)


def test_generate_body():
    message = deploy_message.MessageData()
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
    for i, (generated_line, expected_line) in enumerate(
            zip(deploy_message.generate_body(message).split("\n"), expected_message.split("\n"))):
        assert generated_line == expected_line, "differences on line {}".format(i + 1)


def test_generate_footer():
    footer = deploy_message.get_footer()
    assert footer == expected_footer


def test_get_yml(yml_file):
    print(type(yml_file))
    with open(yml_file) as f:
        print(f.read())
    data = deploy_message.generate.get_message_data(yml_file)
    assert isinstance(data, deploy_message.MessageData)
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
