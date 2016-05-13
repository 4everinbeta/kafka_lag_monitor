import alarmageddon
from alarmageddon.validations.http import HttpValidation
from alarmageddon.validations.kafka import KafkaStatusValidation
from alarmageddon.validations.kafka import KafkaConsumerLagMonitor
from alarmageddon.validations.ssh import SshContext
from alarmageddon.publishing.hipchat import HipChatPublisher
from alarmageddon.publishing.emailer import SimpleEmailPublisher

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

# Setup ssh context
ssh_ctx = SshContext(parser.get("ssh", "user"),parser.get("ssh", "key"))

# Define kafka Validation
zk_nodes = parser.get("kafka", "zookeeper_nodes")
kafka_hosts = parser.get("kafka", "hosts").split(',')
kafka_lag_threshold = parser.getint("kafka", "lag_threshold")

kafka_offset_monitor = KafkaConsumerLagMonitor(ssh_ctx, zookeeper_nodes=zk_nodes,hosts=kafka_hosts,kafka_lag_threshold=kafka_lag_threshold)

validations = []
validations.append(kafka_offset_monitor)

# Define publishers
publishers = []

# HipchatPublisher config
hipchat_endpoint = parser.get("hipchat", "endpoint")
hipchat_token = parser.get("hipchat", "token")
environment = parser.get("hipchat", "environment")
room = parser.get("hipchat", "room")

# EmailPublisher config
publishers.append(SimpleEmailPublisher(sender_address={'real_name':'Find-Team-Alerts','address':'dnr@helixeducation.com'},recipient_addresses =[{'real_name':'Ryan Brown', 'address':'rbrown@helixeducation.com'}],host='email-smtp.us-west-2.amazonaws.com',port=587,smtp_user='AKIAJVVSDV5QC2K66BXQ',smtp_password='Akqr8UXujRUuQwC60p611rThYABFINshTCNh3iEYPxGX'))

# Run tests
alarmageddon.run_tests(validations,publishers)
