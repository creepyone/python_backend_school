from flask import Flask

print(__name__)


def create_app():
    return Flask(__name__)
