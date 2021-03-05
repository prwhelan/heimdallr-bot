import discord
import boto3

version = "1.1.1"
client = discord.Client()
ssm = boto3.client('ssm')
ec2 = boto3.client('ec2')

# AWS part of the bot

# Find our EC2 instance running the valheim server
# Figure out a better way to do this, probably another file
def server():
    return ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:heimdallr',
                    'Values': [''],
                },
            ])['Reservations'][0]['Instances'][0]

def startServer():
    currentServer = server()
    if(currentServer['State']['Name'] == 'stopped'):
        instanceId = currentServer['InstanceId'];
        ec2.start_instances(InstanceIds=[instanceId], DryRun=False)
        return "Starting Valheim Server, this is a dry run and not actually doing anything yet."
    else:
        return "Valheim Server is currently {} and can only start from stopped.".format(currentServer['State']['Name'])

# Discord part of the bot

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Stop spamming everyone
    if message.channel.name.lower() != "valheim-bot":
        return

    if message.content.lower() == "-v" or message.content.lower() == "version":
        await message.channel.send(version)

    if message.content.lower() == "-h" or message.content.lower() == "-help":
        await message.channel.send(("Available commands:\n"
                                    "-server ip\n"
                                    "-server port\n"
                                    "-server status\n"
                                    "-server start\n"));

    if message.content.lower() == "-server ip":
        await message.channel.send(server()['PublicIpAddress'])

    if message.content.lower() == "-server port":
        await message.channel.send("For the Valheim Client: 2456")
        await message.channel.send("For the Steam Client: 2457")

    if message.content.lower() == "-server status":
        await message.channel.send(server()['State']['Name'])

    if message.content.lower() == "-server start":
        await message.channel.send(startServer())

discordToken = ssm.get_parameter(Name='heimdallr-token', WithDecryption=True)['Parameter']['Value']
client.run(discordToken)
