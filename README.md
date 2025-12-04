# Kinsta WP Site to SSH Config

Running this command will create a `~/Documents/.ssh/config` file that can be included in the main `~/.ssh/config` file so that we can easily access websites without needing to look up their details in Kinsta. 

You can also schedule this command so it runs daily, etc. 

## Prerequisites

- Python 3.x
- pip (Python package manager)
- A Kinsta account with API access

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/KinstaToSSH.git
   cd KinstaToSSH
   ```

2. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Kinsta credentials:
   ```
   KINSTA_API_KEY=your_api_key_here
   KINSTA_COMPANY_ID=your_company_id_here
   ```

   To get these values:
   - **KINSTA_API_KEY**: 
     1. Log in to your Kinsta account
     2. Go to User Settings > API Keys
     3. Create a new API key or use an existing one
   
   - **KINSTA_COMPANY_ID**:
     1. Log in to your Kinsta account
     2. The company ID is visible in the URL when you're on the dashboard
     3. It's the number after `/company/` in the URL

4. Make the script executable:
   ```bash
   chmod +x kinsta_ssh_config.py
   ```

5. Run the script to test:
   ```bash
   ./kinsta_ssh_config.py
   ```

6. Include the generated config in your main SSH config:
   Add this line to your `~/.ssh/config` file:
   ```
   Include ~/Documents/.ssh/config
   ```

## Scheduling

### Install Schedule

1. Copy the launch agent file:
   ```bash
   mkdir -p ~/Library/LaunchAgents
   cp com.kinsta.sshconfig.plist ~/Library/LaunchAgents/
   ```

2. Load the launch agent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.kinsta.sshconfig.plist
   ```

### Reinstall Schedule

If you need to update the schedule:
```bash
launchctl unload ~/Library/LaunchAgents/com.kinsta.sshconfig.plist
launchctl load ~/Library/LaunchAgents/com.kinsta.sshconfig.plist
```

## Usage

After setup, you can connect to your Kinsta sites using:
```bash
ssh k.site-name
```

Where `site-name` is the name of your WordPress site in Kinsta.

## Troubleshooting

- If you get permission errors, ensure the script is executable (`chmod +x kinsta_ssh_config.py`)
- Check the `error.log` file for any API-related issues
- Verify your API key and company ID are correct in the `.env` file
- Ensure your SSH config directory exists (`mkdir -p ~/Documents/.ssh`)
