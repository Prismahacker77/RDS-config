import boto3

def scan_rds_instances():
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

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
            publicly_accessible = db['PubliclyAccessible']
            storage_encrypted = db['StorageEncrypted']
            vpc_id = db.get('DBSubnetGroup', {}).get('VpcId', 'N/A')
            retention_period = db['BackupRetentionPeriod']
            
            # Retrieve security groups associated with the RDS instance
            security_groups = [sg['VpcSecurityGroupId'] for sg in db['VpcSecurityGroups']]

            print(f"DB Identifier: {db_identifier}")
            print(f"Status: {db_status}")
            print(f"Engine: {engine}")
            print(f"Region: {region}, AZ: {az}")
            print(f"Port: {port}")
            print(f"VPC ID: {vpc_id}")
            print(f"Security Groups: {security_groups}")
            print(f"Publicly Accessible: {publicly_accessible}")
            print(f"Storage Encrypted: {storage_encrypted}")
            print(f"Backup Retention Period: {retention_period} days")
            print("-" * 60)

if __name__ == "__main__":
    scan_rds_instances()
