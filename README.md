# Seneca-AI/ML

The ML repo maintains all of the code for running machine learning models in Seneca.

## Installation (using pyenv)
* `pyenv virtualenv 3.7.0 venv3.7`
* `pyenv activate venv3.7`
* `pip install --upgrade pip`
* `pip install -r requirements.txt`
* `python setup.py install`

## Dev Notes
* Please pay attention to the other README's embedded into subdirectories of this repo.
* The entire Seneca org utilizes [protocol buffers](https://developers.google.com/protocol-buffers) to define a language-agnostic data model.  These protocol buffers are published to the 'common' repository, and the generated code must be copied from there into this repository's api/type directory.  We guarantee that the code will always be backwards compatible, so you do not need to worry about changes in the 'common' repo.  However, if you want to use new messages from the repo, you must copy the files again manually.  Note that these files should never be edited -- the code is automatically generated. These are the steps to copy the relevant code:
    * (from the parent directory of this repo)
    * `git clone https://github.com/Seneca-AI/common.git`
    * `cp -r common/proto_out/python/api ML`
    * `echo '*_pb2.py' >> ML/api/type/.gitignore`
* Seneca utilizes [Cloud Functions](https://cloud.google.com/functions) to run the ML microservices.  In Python, you use the flask framework to define each microservice as an endpoint, and define each in main.py as its own function that takes a request parameter, e.g.: `def microservice_one(flask.request):```
    *  No logic is placed in main.py, and it simply calls server.py
    *  The function name must match the cloud function's name (which is also the last piece of the endpoint's path)


## Repository Rules
* 1 commit per pull request

### Style Rules
* Functions must not be more than 100 lines of code, with few exceptions granted.
* Functions must be defined like
` def func_name(param_one: type, param_two: type) -> return_type: `

### Testing Rules
* Tests should test the output of a function.  If the function has no output but performs some operation, then the output of the function should _not_ be tested, but rather whatever operation was done should be tested (e.g. checking output paths, _and the values stored in the files_).
* The location of test files matches the location of the implementation it is testing.  For example, if the implementation is at ml/utils/fileutils/ then the tests will be located at tests/utils/fileutils/.