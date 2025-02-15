import click

from basic_kafka_consumer import run_basic_consumer


@click.command("kafka-consumer")
@click.option("-t", "--consumer-type", required=True, type=click.Choice(['basic']),
              help="Type of Kafka consumer to run")
def main(consumer_type):
    if consumer_type == 'basic':
        print(f"Starting consumer of type {consumer_type}")
        run_basic_consumer()


if __name__ == '__main__':
    main()
