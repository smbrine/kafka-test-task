import argparse
import typing as t
import kafka

def produce(args):
    producer = kafka.KafkaProducer(bootstrap_servers=args.kafka)
    producer.send(args.topic, args.message.encode("utf-8"))

def consume(args):
    consumer = kafka.KafkaConsumer(args.topic, bootstrap_servers=args.kafka)
    for msg in consumer:
        print(msg.value.decode('utf-8'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer and Consumer")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command help")

    # Producer sub-command
    produce_parser = subparsers.add_parser("produce", help="Produce messages to Kafka")
    produce_parser.add_argument("-m", "--message", required=True, help="Message to send")
    produce_parser.add_argument("--topic", required=True, help="Kafka topic name")
    produce_parser.add_argument("--kafka", required=True, help="Kafka broker address")
    produce_parser.set_defaults(func=produce)

    # Consumer sub-command
    consume_parser = subparsers.add_parser("consume", help="Consume messages from Kafka")
    consume_parser.add_argument("--topic", required=True, help="Kafka topic name")
    consume_parser.add_argument("--kafka", required=True, help="Kafka broker address")
    consume_parser.set_defaults(func=consume)

    args = parser.parse_args()

    # Call the appropriate function based on the sub-command
    args.func(args)