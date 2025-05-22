# Kinsta WP Site to SSH Config

Running this command will create a ~/Documents/.ssh/config file that can be included in the main ssh/config file so that we can easily access websites without needing to look up their details in kinsta. 

You can also schedule this command so it runs daily, etc. 

## Setup

This file will be included into the `~/.ssh/config` file with the `Include ~/Documents/.ssh/config` command. Make sure you add that after you run this the first time.


## Scheduling

### Install Schedule

    $ mkdir -p ~/Library/LaunchAgents && cp com.kinsta.sshconfig.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.kinsta.sshconfig.plist

### Reinstall Schedule

    $ launchctl unload ~/Library/LaunchAgents/com.kinsta.sshconfig.plist && launchctl load ~/Library/LaunchAgents/com.kinsta.sshconfig.plist
