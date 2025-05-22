#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Kinsta API configuration
KINSTA_API_URL = "https://api.kinsta.com/v2"
API_KEY = os.getenv("KINSTA_API_KEY")
COMPANY_ID = os.getenv("KINSTA_COMPANY_ID")

def to_slug(name):
    """Convert a string to a slug format."""
    # Convert to lowercase and replace spaces with hyphens
    slug = name.lower()
    # Remove any characters that aren't alphanumeric or hyphens
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # Replace multiple hyphens with a single hyphen
    slug = re.sub(r'-+', '-', slug)
    # Remove leading and trailing hyphens
    slug = slug.strip('-')
    return slug

def get_wordpress_sites():
    """Fetch all WordPress sites from Kinsta API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("Fetching sites from Kinsta API...")
    print(f"Using company ID: {COMPANY_ID}")
    # Get all environments
    response = requests.get(
        f"{KINSTA_API_URL}/sites?company={COMPANY_ID}",
        headers=headers
    )
    
    print(f"API Response Status: {response.status_code}")
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch sites: {response.text}")
    
    data = response.json()
    sites = data.get('company', {}).get('sites', [])
    print(f"Found {len(sites)} total sites")
    return sites

def get_site_ssh_info(site_id, site_name):
    """Fetch SSH information for a specific site."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Get the environments
    response = requests.get(
        f"{KINSTA_API_URL}/sites/{site_id}/environments",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"Warning: Could not fetch environment info for site {site_id}: {response.text}")
        return None
        
    data = response.json()
    environments = data.get('site', {}).get('environments', [])
    
    # Find the production environment
    for env in environments:
        if env.get('name') == 'live':
            ssh_connection = env.get('ssh_connection', {})
            if ssh_connection:
                return {
                    'host': ssh_connection.get('ssh_ip', {}).get('external_ip'),
                    'user': site_name,  # Use the site name as the SSH user
                    'port': ssh_connection.get('ssh_port')
                }
    
    return None

def generate_ssh_config(sites):
    """Generate SSH config entries for each site."""
    ssh_config = []
    production_sites = 0
    
    for site in sites:
        if site.get("status") == "live":
            production_sites += 1
            site_name = site.get("name")
            print(f"Processing site: {site_name}")
            
            # Get SSH information
            ssh_info = get_site_ssh_info(site.get("id"), site_name)
            if not ssh_info:
                print(f"Skipping {site_name} - no SSH information available")
                continue
                
            ssh_config.append(f"""
# {site_name}
Host k.{site_name}
    HostName {ssh_info.get('host')}
    User {ssh_info.get('user')}
    Port {ssh_info.get('port')}
""")
    
    print(f"Generated config for {production_sites} live sites")
    return "\n".join(ssh_config)

def main():
    if not API_KEY or not COMPANY_ID:
        print("Error: Please set KINSTA_API_KEY and KINSTA_COMPANY_ID environment variables")
        return
    
    try:
        print("Starting Kinsta SSH config generation...")
        sites = get_wordpress_sites()
        
        if not sites:
            print("No sites found. Please check your API credentials and company ID.")
            return
            
        ssh_config = generate_ssh_config(sites)
        
        # Write to SSH config file
        config_path = os.path.expanduser("~/Documents/.ssh/config")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, "w") as f:
            f.write(ssh_config)
        
        print(f"SSH config has been generated at {config_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 