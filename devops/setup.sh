#!/bin/bash

# Define a spinner.
spin() {
  spinner="/|\\-/|\\-"
  while :
  do
    for i in `seq 0 7`
    do
      echo -n "${spinner:$i:1}"
      echo -en "\010"
      sleep 1
    done
  done
}

# Download and install all necessary dependencies.
setup() {
  echo "This only mostly works, unfortunately.  I think it's missing a step for adding the GPU driver, but honestly I don't care about this anymore."
	echo "Output stored in setup.log"
	touch setup.log

	read -p "Enter GitHub token: " GITHUB_TOKEN

    echo "Getting protos"
    cd ../../..
    git clone https://${GITHUB_TOKEN}@github.com/Seneca-AI/common.git >> setup.log
    cp -r common/proto_out/python/api ML >> setup.log

    # Needs some fixing -- add to beginning of file instead.
    echo "Setting up python environment"
    curl https://pyenv.run | bash >> setup.log

    touch bashtemp.txt
    echo "" >> bashtemp.txt
    echo "export PYENV_ROOT=\"\$HOME/.pyenv\"" >> bashtemp.txt
    echo "export PATH=\"\$PYENV_ROOT/bin:\$PATH\"" >> bashtemp.txt
    echo "eval \"\$(pyenv init --path)\"" >> bashtemp.txt
    echo "" >> bashtemp.txt
    cat ~/.bashrc >> bashtemp.txt
    cat bashtemp.txt > ~/.bashrc
    rm bashtempt.txt

    sudo apt-get install build-essential libffi-dev libssl-dev zlib1g-dev -y >> setup.log
    pyenv install 3.7.0 >> setup.log
    pyenv global 3.7.0 >> setup.log
    pyenv virtualenv my-venv >> setup.log

    echo "Installing dependencies"
    pip install --upgrade pip >> setup.log
    pip install -r requirements.txt >> setup.log
}

start() {
    if [ -z "$2" ]; then
		echo "Must specify 'bash devops/setup.sh start_server [GOOGLE_CLOUD_PROJECT] [ABSOLUTE_PATH_TO_GOOGLE_APPLICATION_CREDENTIALS]'"
		exit 1
	fi

	export GOOGLE_CLOUD_PROJECT=$1
	export GOOGLE_APPLICATION_CREDENTIALS=$2
    export FLASK_APP=ml/server/flask.py

	echo "Starting single server."
	nohup sudo env "PATH=$PATH" "GOPATH=$GOPATH" "GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT" "GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS" flask run --host=0.0.0.0 > start.txt 2>&1 </dev/null &
}
