from setuptools import setup

setup(name="interact",
      version="0.1",
      url="http://github.com/swarchal/interact",
      description="Display microscope images with interactive plots",
      author="Scott Warchal",
      author_email="S.warchal@sms.ed.ac.uk",
      license="MIT",
      packages=["interact"],
      install_requires=["scikit-image>=0.12",
                        "numpy>=1.0",
                        "bokeh>=0.12.0"],
      zip_safe=False)
