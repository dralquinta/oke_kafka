 #!/bin/sh

source ./venv/bin/activate
sh dependencies.sh
source ./venv/bin/activate

python3 consumer.py