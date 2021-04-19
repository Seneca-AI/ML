# Seneca-AI/ML

The ML repo maintains all of the code for running machine learning models in Seneca.

## Dev Notes
* Please pay attention to the other README's embedded into subdirectories of this repo.
* The entire Seneca org utilizes [protocol buffers](https://developers.google.com/protocol-buffers) to define a language-agnostic data model.  These protocol buffers are published to the 'common' repository, and the generated code must be copied from there into this repository's api/type directory.  We guarantee that the code will always be backwards compatible, so you do not need to worry about changes in the 'common' repo.  However, if you want to use new messages from the repo, you must copy the files again manually.  Note that these files should never be edited -- the code is automatically generated. These are the steps to copy the relevant code:
    * (from the parent directory of this repo)
    * `git clone https://github.com/Seneca-AI/common.git`
    * `cp -r common/proto_out/python/api ML`
    * `echo '\n*_pb2.py' >> ML/api/type/.gitignore`
* Seneca utilizes [Cloud Functions](https://cloud.google.com/functions) to run the ML microservices.  In Python, you use the flask framework to define each microservice as an endpoint, and define each in main.py as its own function that takes a request parameter, e.g.: `def microservice_one(flask.request):```
    *  No logic is placed in main.py, and it simply calls server.py
    *  The function name must match the cloud function's name (which is also the end of the endpoint's path)