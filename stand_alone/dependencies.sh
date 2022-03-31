 #!/bin/sh
 
 if [ ! -d "venv" ] 
    then
        echo "venv not present. Creating" 
        echo '============== Virtual Environment Creation =============='
        python3 -m venv venv
        source venv/bin/activate

        echo '============== Upgrading pip3 =============='
        pip3 install --upgrade pip

        echo '============== Installing app dependencies =============='
        pip3 install -r ../../streams_manipulation_poc/requirements.txt
        chmod -R 775 venv
    fi

    source "./venv/bin/activate"
