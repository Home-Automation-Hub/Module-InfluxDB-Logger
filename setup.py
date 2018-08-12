from distutils.core import setup

setup(
    name="Home Automation InfluxDB Logger",
    version="1.0",
    description="Home Automation Hub Module - InfluxDB Logger",
    author="Cameron Gray",
    author_email="development@camerongray.me",
    url="https://github.com/camerongray1515",
    install_requires=[
        "influxdb==5.2.0"
    ],
    packages=["home_automation_influxdb_logger"],
    include_package_data=True
)