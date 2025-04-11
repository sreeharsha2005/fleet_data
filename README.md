# FLEET DATA GENERATOR

### Introduction
This module does the following operations:
* Create/Reuse vehicle, user, driver_profile data and store to file
* Publish kafka message for each type of generated data on respective kafka topic
* Consume kafka message based on topic


### Python virtual environment setup
Navigate to the project directory (base directory) where this README file is present
Run the below command to install python virtual environment

```
python3 -m venv env
source env/bin/activate
```

### Install requirement python packages
Run the below command to install the necessary packages listed in requirements file

```
pip3 install -r requirements.txt
```

### Include the project path into PYTHONPATH env variable
Run the below command in the project base directory
```
export PYTHONPATH=$PYTHONPATH:/path/to/your/project_directory
```

### Generating synthetic data
Navigate to `synthetic_data_producer` directory and run the below command:
```
python3 synthetic_data_producer.py -n 10 -c y

Note: -n : number of vehicles data required
      -c : create new data (yes/no)
```

## Viewing Published data on Kafka using Kafka GUI viewer
Below steps are for creating Kafka broker nodes
```
brew install redpanda-data/tap/redpanda              #will install redpanda package
rpk container --help        # Get hel from Redpanda confrontation
rpk container start -n 1    # will start kafka broker nodes and also start redpanda GUI

rpk cluster info            # show how many broker nodes have 
rpk cluster health          # show the healthof running broker nodes
rpk container purge         # will purge/stop all the running broker nodes
```

When the container start command is issued, RedPanda Console GUI is also started.
To view the Kafka UI, open web browser and goto below address:
```
http://localhost:8080/overview
```

### Consuming Kafka data
Navigate to `synthetic_data_consumer` directory and run the below command:
```
python3 synthetic_data_consumer.py
```




