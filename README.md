# Seneca-AI/ML

Once upon a time, this repo was for a server that would host services that ran Seneca's machine learning algorithm.

Now you can basically just run https://github.com/Tianxiaomo/pytorch-YOLOv4 on a Google Cloud instance.  I never got around to figuring out how to use git
submodules, so it's just copied and pasted under quarantined/object_detection.

The only reason anyone should be reading this repo is because I said "No, look, I promise I've written a few lines of Python! Check out this repo", in which case the ml/ and tests/ directories are the only parts of interest (and the only ones linted).

## Getting Started
### Prerequisites
* a Google Cloud project with billing enabled
* enough quota for a VM instance with a GPU (you get zero by default, so you'll have to request it)

### Setup
1. Create your VM instance 
    1. Note that this machine type is only supported in some zones.
    1. `$ gcloud compute instances create ${VM_INSTANCE_NAME} --image=ubuntu-minimal-2104-hirsute-v20210511 --image-project=ubuntu-os-cloud --zone=us-central1-c --accelerator type=nvidia-tesla-k80,count=1 --maintenance-policy TERMINATE --restart-on-failure --project=${PROJECT_ID}`
1. Copy your [service account](https://cloud.google.com/iam/docs/service-accounts) credentials into the VM
    1. `$ gcloud compute scp ${PATH_TO_GOOGLE_APPLICATION_CREDENTIALS} ${VM_INSTANCE_NAME}:~ --project=${PROJECT_ID}`
1. SSH into your VM instance 
    1. `$ gcloud compute ssh ${VM_INSTANCE_NAME} --project=${PROJECT_ID}`
1. Install git
    1. `$ sudo apt-get update -y`
    1. `$ sudo apt-get install git -y`
1. Clone this repo
1. Run the setup script
    1. `$ bash devops/setup.sh setup`

### Starting the server
1. `$ bash devops/setup.sh start`

### Exposing the server
1. `$ gcloud compute firewall-rules create rule-allow-tcp-$PORT --source-ranges 0.0.0.0/0 --target-tags allow-tcp-$PORT --allow tcp:$PORT`
2. `$ gcloud compute instances add-tags $VM_INSTANCE --tags allow-tcp-$PORT`

## Dev Notes
* Please pay attention to the other README's embedded into subdirectories of this repo.
* The entire Seneca org utilizes [protocol buffers](https://developers.google.com/protocol-buffers) to define a language-agnostic data model.  These protocol buffers are published to the 'common' repository, and the generated code must be copied from there into this repository's api/type directory.  We guarantee that the code will always be backwards compatible, so you do not need to worry about changes in the 'common' repo.  However, if you want to use new messages from the repo, you must copy the files again manually.  Note that these files should never be edited -- the code is automatically generated. These are the steps to copy the relevant code:
    * (from the parent directory of this repo)
    * `git clone https://github.com/Seneca-AI/common.git`
    * `cp -r common/proto_out/python/api ML`
    * `echo '*_pb2.py' >> ML/api/type/.gitignore`

## Repository Rules
* 1 commit per pull request

### Style Rules
* Functions must not be more than 100 lines of code.
* Functions must be defined like
` def func_name(param_one: type, param_two: type) -> return_type: `

### Testing
* The location of test files matches the location of the implementation it is testing.  For example, if the implementation is at ml/utils/fileutils/ then the tests will be located at tests/utils/fileutils/.