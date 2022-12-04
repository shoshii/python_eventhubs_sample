import asyncio
import time
#from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventHubProducerClient, EventData
#from azure.eventhub import EventData
CONNECTION_STRING = "<connection string>"
EVENTHUB_NAME = "<event hub name>"
async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STRING, eventhub_name=EVENTHUB_NAME)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData('{"Rows": [{"name": "Alice", "uid": 1}]'))
        event_data_batch.add(EventData('{"Rows": [{"name": "Bob", "uid": 2}]}'))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

def send_event_data_batch():
    # Without specifying partition_id or partition_key
    # the events will be distributed to available partitions via round-robin.
    producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STRING, eventhub_name=EVENTHUB_NAME)
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData('{"Rows": [{"name": "Alice", "uid": 1}]}'))
    event_data_batch.add(EventData('{"Rows": [{"name": "Bob", "uid": 2}]}'))
    producer.send_batch(event_data_batch)
    """
    /*
                steps at ADX:

                .create table RawTable (Rows: dynamic)

                .create table RawTable ingestion json mapping 'TestMapping' '[{"column":"Rows", "Properties": {"Path": "$.Rows"}}]'

                .create table TargetTable (id: int, name: string)

                .create function TestExpand() {
                    RawTable
                    | mv-expand event = Rows
                    | project
                        name = tostring(event['name']),
                        uid = toint(event['uid'])
                }

                .alter table TargetTable policy update @'[{"Source": "RawTable", "Query": "TestExpand()", "IsEnabled": "True", "IsTransactional": true}]'

                */
    """

#loop = asyncio.get_event_loop()
#loop.run_until_complete(run())
start_time = time.time()
#asyncio.run(run())
send_event_data_batch()
print("Send messages in {} seconds.".format(time.time() - start_time))
