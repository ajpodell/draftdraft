""" This is attempting to make the project top level discoverable.

Goal here is to make things like the dev_tools directory work and able to import out of root
"""

import setuptools

setuptools.setup(
    name="draftdraft",
    version="0.0.1",
    author="apodell",  # TODO: come back and find a way to make this a list
    author_email="aaronpodell@gmail.com",
    description="draftdraft - the hottest new nfl game",
    packages=[],
)
