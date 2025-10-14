import setuptools


setuptools.setup(
    name="bt_to_bq_pipeline",
    version="0.0.1",
    install_requires=[
        "apache-beam[gcp]",
        "cramjam"
    ],
    packages=setuptools.find_packages(),
)
