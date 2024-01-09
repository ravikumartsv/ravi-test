import boto3

def list_services(region):
    client = boto3.client('resourcegroupstaggingapi', region_name=region)
    
    response = client.get_resources(TagFilters=[{'Key': 'aws:service', 'Values': ['*']}])

    return [resource['ResourceARN'].split('/')[1] for resource in response.get('ResourceTagMappingList', [])]

def describe_service(region, service_name):
    if service_name.lower() == 'ec2':
        client = boto3.client('ec2', region_name=region)
        response = client.describe_instances()
    elif service_name.lower() == 'rds':
        client = boto3.client('rds', region_name=region)
        response = client.describe_db_instances()
    else:
        return f"Service {service_name} not supported."

    return response

def main():
    regions = ['us-east-1', 'us-west-2', 'eu-west-1']  
    for region in regions:
        print(f"\nRegion: {region}")
        
        services = list_services(region)
        for service in services:
            print(f"\nService: {service}")
            
            service_details = describe_service(region, service)
            print(f"Details: {service_details}")

if __name__ == "__main__":
    main()

