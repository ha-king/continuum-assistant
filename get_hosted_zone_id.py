#!/usr/bin/env python3
import boto3

def get_hosted_zone_id(domain_name):
    """Get the hosted zone ID for a domain name."""
    route53 = boto3.client('route53')
    
    # List all hosted zones
    response = route53.list_hosted_zones()
    
    # Find the hosted zone for the domain
    for zone in response['HostedZones']:
        if zone['Name'] == f"{domain_name}.":  # Route 53 adds a trailing dot
            return zone['Id'].replace('/hostedzone/', '')  # Remove the '/hostedzone/' prefix
    
    return None

if __name__ == "__main__":
    domain = "infascination.com"
    zone_id = get_hosted_zone_id(domain)
    
    if zone_id:
        print(f"Hosted Zone ID for {domain}: {zone_id}")
        print(f"Update the CDK stack with this ID")
    else:
        print(f"No hosted zone found for {domain}")