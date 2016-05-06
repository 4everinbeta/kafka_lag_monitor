import alarmageddon
from alarmageddon.validations.http import HttpValidation
from alarmageddon.validations.kafka import KafkaStatusValidation
from alarmageddon.validations.kafka import KafkaConsumerLagMonitor
from alarmageddon.validations.ssh import SshContext
from alarmageddon.publishing.hipchat import HipChatPublisher

# Setup ssh context
ssh_ctx = SshContext("ec2-user","/Users/Ryan/.ssh/kafka-key.pem")

# Define kafka Validation
zk_nodes = '10.196.2.40:2181,10.196.2.39:2181,10.196.2.38:2181'
kafka_hosts = ['52.26.246.89','52.24.9.167','52.27.168.120']
# kafka_validation = KafkaStatusValidation(ssh_ctx, zookeeper_nodes=zk_nodes,hosts=kafka_hosts,kafka_list_topic_command="/usr/local/kafka/bin/kafka-topics.sh --describe")

kafka_offset_monitor = KafkaConsumerLagMonitor(ssh_ctx, zookeeper_nodes=zk_nodes,hosts=kafka_hosts)

validations = []
# validations.append(kafka_validation)
validations.append(kafka_offset_monitor)

# Define publishers
publishers = []
hipchat_endpoint = "https://api.hipchat.com/v1/"
hipchat_token = "cce062fd37d94bb9da4bff76bc292f"
environment = "stable"
room = 2686409
publishers.append(HipChatPublisher(hipchat_endpoint, hipchat_token, environment, room))

# Run tests
alarmageddon.run_tests(validations,publishers)
