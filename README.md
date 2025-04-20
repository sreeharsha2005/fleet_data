[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)

# FLEET DATA GENERATOR

### **Block diagram**

<img width="786" alt="Screenshot 2025-04-19 at 9 02 52 PM" src="https://github.com/user-attachments/assets/76c7d033-b9bf-4bcc-a9f0-87ba82c17959" />


### Introduction
This codebase has the below functionality:
* Create vehicle, user, driver_profile data for a specified number of instances and store to file
* Use the stored data to generate fake metrics for vehicle, user and driver_profile 
* For each generated metric, publish a message on Kafka topic
* Kafka Consumer to ingest the above metrics and call REST API service

### **Flow diagram**

<img width="842" alt="Screenshot 2025-04-19 at 9 02 15 PM" src="https://github.com/user-attachments/assets/a559b5f3-4c24-49f6-8517-dbd50c6bb6a3" />


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




