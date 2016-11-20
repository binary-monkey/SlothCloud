from setuptools import setup
from gen_ssl import create_self_signed_cert

setup(name="SlothCloud", version="0.1",
      description="RESTful access media server made using Python 3 and Flask",
      author="Ninia",
      author_email="ninia@protonmail.com",
      url="https://github.com/Ninia/SlothCloud",
      install_requires=["flask", "Flask-AutoIndex", "pyopenssl"])

create_self_signed_cert()