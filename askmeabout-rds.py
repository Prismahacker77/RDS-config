import boto3
from prettytable import PrettyTable

def scan_rds_instances():
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    rds_info = []

    for region in regions:
        print(f"Scanning region: {region}")
        rds_client = boto3.client('rds', region_name=region)
        db_instances = rds_client.describe_db_instances()['DBInstances']

        for db in db_instances:
            db_identifier = db['DBInstanceIdentifier']
            db_status = db['DBInstanceStatus']
            engine = db['Engine']
            port = db['Endpoint']['Port']
            az = db['AvailabilityZone']
            multi_az = db['MultiAZ']
            publicly_accessible = db['PubliclyAccessible']
            storage_encrypted = db['StorageEncrypted']
            vpc_id = db.get('DBSubnetGroup', {}).get('VpcId', 'N/A')
            retention_period = db['BackupRetentionPeriod']
            
            security_groups = [sg['VpcSecurityGroupId'] for sg in db['VpcSecurityGroups']]

            rds_info.append({
                'DBIdentifier': db_identifier,
                'Status': db_status,
                'Engine': engine,
                'Region': region,
                'AZ': az if not multi_az else 'Multi-AZ',
                'Port': port,
                'VPCID': vpc_id,
                'SecurityGroups': security_groups,
                'PubliclyAccessible': publicly_accessible,
                'StorageEncrypted': storage_encrypted,
                'RetentionPeriod': retention_period
            })

    return rds_info

def print_rds_info_table(rds_info):
    table = PrettyTable()
    table.field_names = [
        "DB Identifier", "Status", "Engine", "Region", "AZ/Multi-AZ", "Port", 
        "VPC ID", "Publicly Accessible", "Storage Encrypted", "Retention Period", "Security Groups"
    ]

    for info in rds_info:
        table.add_row([
            info['DBIdentifier'], info['Status'], info['Engine'], info['Region'], 
            info['AZ'], info['Port'], info['VPCID'], info['PubliclyAccessible'], 
            info['StorageEncrypted'], info['RetentionPeriod'], ', '.join(info['SecurityGroups'])
        ])

    print(table)

if __name__ == "__main__":
    rds_info = scan_rds_instances()
    print_rds_info_table(rds_info)
