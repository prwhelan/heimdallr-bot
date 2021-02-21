# heimdallr-bot
A Discord Bot used to control the Valheim dedicated server.

Disclaimer: I have never written python.

The [Valheim Server](https://github.com/prwhelan/valheim-dedicated) is hosting on EC2, which has a rotating IP address.  In order to help people discover what the IP address is, this discord bot yells it at them.

Version 1.0.0 is painfully simple:
- `-server ip` prints out the IP address
- `-server port` prints out the port
- `-server status` prints out if the ec2 instances is running or stopped

