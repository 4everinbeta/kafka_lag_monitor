import alarmageddon
from alarmageddon.validations.http import HttpValidation
from alarmageddon.validations.kafka import KafkaStatusValidation
from alarmageddon.validations.kafka import KafkaConsumerLagMonitor
from alarmageddon.validations.ssh import SshContext
from alarmageddon.publishing.hipchat import HipChatPublisher

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

# Setup ssh context
ssh_ctx = SshContext(parser.get("ssh", "user"),parser.get("ssh", "key"))

# Define kafka Validation
zk_nodes = parser.get("kafka", "zookeeper_nodes")
kafka_hosts = parser.get("kafka", "hosts").split(',')

kafka_offset_monitor = KafkaConsumerLagMonitor(ssh_ctx, zookeeper_nodes=zk_nodes,hosts=kafka_hosts)

validations = []
validations.append(kafka_offset_monitor)

# Define publishers
publishers = []
hipchat_endpoint = parser.get("hipchat", "endpoint")
hipchat_token = parser.get("hipchat", "token")
environment = parser.get("hipchat", "environment")
room = parser.get("hipchat", "room")
publishers.append(HipChatPublisher(hipchat_endpoint, hipchat_token, environment, room))

# Run tests
alarmageddon.run_tests(validations,publishers)
