# Seneca-AI/ML

The ML repo maintains all of the code for running machine learning models in Seneca.

## Dev Notes
* The entire Seneca org utilizes [protocol buffers](https://developers.google.com/protocol-buffers) to define a language-agnostic data model.  These protocol buffers are published to the 'common' repository, and the generated code must be copied from there into this repository's api/type directory.  We guarantee that the code will always be backwards compatible, so you do not need to worry about changes in the 'common' repo.  However, if you want to use new messages from the repo, you must copy the files again manually.  Note that these files should never be edited -- the code is automatically generated. These are the steps to copy the relevant code:
    * (from the parent directory of this repo)
    * `git clone https://github.com/Seneca-AI/common.git`
    * `cp -r common/proto_out/python/api ML`
    * `echo '\n*_pb2.py' >> ML/api/type/.gitignore`
