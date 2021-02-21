import discord
import boto3

version = "1.0.0"
client = discord.Client()
ssm = boto3.client('ssm')

# Find our EC2 instance running the valheim server
# Figure out a better way to do this, probably another file
server = boto3.client('ec2').describe_instances(
        Filters=[
            {
                'Name': 'tag:heimdallr',
                'Values': [''],
            },
        ])['Reservations'][0]['Instances'][0]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "-v" or message.content.lower() == "version":
        await message.channel.send(version)

    if message.content.lower() == "-h" or message.content.lower() == "-help":
        await message.channel.send(("Available commands:\n"
                                    "-server ip\n"
                                    "-server port\n"
                                    "-server status\n"));

    if message.content.lower() == "-server ip":
        await message.channel.send(server['PublicIpAddress'])

    if message.content.lower() == "-server port":
        await message.channel.send("For the Valheim Client: 2456")
        await message.channel.send("For the Steam Client: 2457")

    if message.content.lower() == "-server status":
        await message.channel.send(server['State']['Name'])


discordToken = ssm.get_parameter(Name='heimdallr-token', WithDecryption=True)['Parameter']['Value']
client.run(discordToken)
