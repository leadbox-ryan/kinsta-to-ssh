#!/bin/bash
# Setup script for Kinsta SSH Config scheduler

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.kinsta.sshconfig.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "Setting up Kinsta SSH Config scheduler..."

# Create LaunchAgents directory if needed
mkdir -p "$LAUNCH_AGENTS_DIR"

# Unload existing agent if present
if launchctl list | grep -q "com.kinsta.sshconfig"; then
    echo "Unloading existing agent..."
    launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null
fi

# Generate plist with correct paths for this user
cat > "$LAUNCH_AGENTS_DIR/$PLIST_NAME" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.kinsta.sshconfig</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$SCRIPT_DIR/kinsta_ssh_config.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>0</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/kinsta-ssh-config.error.log</string>
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/kinsta-ssh-config.log</string>
    <key>RunAtLoad</key>
    <true/>
    <key>StartOnMount</key>
    <true/>
</dict>
</plist>
EOF

# Load the agent
echo "Loading agent..."
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

echo "Done! The script will run:"
echo "  - Now (on load)"
echo "  - Daily at midnight"
echo "  - When volumes are mounted"
echo ""
echo "Logs: ~/Library/Logs/kinsta-ssh-config.log"
