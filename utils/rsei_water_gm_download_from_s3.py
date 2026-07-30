import subprocess
import boto3
from botocore import UNSIGNED
from botocore.config import Config

# this script downloads RSEI water microdata  
# from http://abt-rsei.s3-website-us-east-1.amazonaws.com/?prefix=microdata2022/water/


# Define the configurations
bucket_name = 'abt-rsei'
prefix = 'microdata2022/water/'
url = "http://abt-rsei.s3.amazonaws.com/microdata2022/water/"
#outdir = "Y:/uspa_tctac/data/RSEI/microdata2022/water/"
outdir = "/home/lenkne/oboiko/EJ/RSEI/"

# connect to s3 without credentials
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# Function to list all objects under the specified prefix
def list_s3_objects(bucket, prefix):
    s3_objects = []
    # Use the list_objects_v2 method to list objects under the prefix
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    # Check if the response contains 'Contents' which will list objects
    if 'Contents' in response:
        for obj in response['Contents']:
            s3_objects.append(obj['Key'])
            # Build the URL for each object
            #file_url = f"http://{bucket}.s3-website-us-east-1.amazonaws.com/{obj['Key']}"
            #print(obj["Key"])
        return s3_objects
    else:
        print("No objects found under the specified prefix.")

# Call the function to list objects
s3_objects = list_s3_objects(bucket_name, prefix)
filenames = [f.split("/")[-1] for f in s3_objects if f.endswith(".zip")]
# Construct the curl command as a string to donwload file to local directory
for filename in filenames:
    curl_command = f"curl {url}{filename} --output {outdir}{filename}"
    print (f"Executing {curl_command}")
    # Execute the command using subprocess
    subprocess.run(curl_command, shell=True, capture_output=True, text=True)
