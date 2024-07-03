import boto3
import json
import requests
import os
from urllib.parse import unquote




def update_incident(ticket_id, new_data):
    # Authentication
    user_name = os.environ['SERVICENOW_USERNAME']
    password = os.environ['SERVICENOW_PASSWORD']
    host = os.environ['SERVICENOW_HOST']
    auth = (user_name, password)
    
    # API endpoint for incident records
    url = f'https://{host}/api/now/table/incident/{ticket_id}'
    
    # Update incident data
    response = requests.put(url, auth=auth, json=new_data)
    
    # Check for success
    if response.status_code == 200:
        print("Incident updated successfully")
    else:
        print(f"Error updating incident: {response.status_code}")

def lambda_handler(event, context):
 
    s3 = boto3.client('s3')
    client = boto3.client('connect')
    InstanceId = os.environ['InstanceId']
    

    
    # Specify the bucket name and folder/key prefix
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    # key = 'Analysis/Voice/2024/05/21/15e39520-5451-4bde-8487-23cf7722302f_analysis_2024-05-21T14.3A47.3A00Z.json'
    key = event['Records'][0]['s3']['object']['key']
    key = unquote(key)
    # key = key.replace('%3A',':').replace('%2B','+')
    
    
    
    Contact_id = key.split('/')[-1]
    Contact_id = Contact_id.split('_')[0]
    
    print(bucket_name)
    print(key)
    print(Contact_id)
    
    # Fetch contact attributes based on contact id
    
    response = client.get_contact_attributes(
    InstanceId= InstanceId,
    InitialContactId= Contact_id
    )
    print(response)
    sys_id = response['Attributes']['sys_id']
    number = response['Attributes']['number']
    print(sys_id)
    
    # Get object data
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    json_data = obj['Body'].read().decode('utf-8')
                
    # Parse JSON data
    data = json.loads(json_data)

    data = data['ConversationCharacteristics']['ContactSummary']['PostContactSummary']['Content']
                
    # Process or analyze the JSON data here
    print(data)
    
    
    
     # Example usage
    ticket_id = sys_id
    new_data = {
        'work_notes': 'Call Summary' + data
    }
    
    update_incident(ticket_id, new_data)
    
    
    

    
    # client = boto3.client('sns')
    # response = sns_client.publish(
    #     TopicArn = topicArn,
    #     Message="Incident_number: " number " "
    #         "Contact Summary: " data,
    #     Subject= message
    # )
    
    

    

# from urllib.parse import unquote
# key = 'Analysis/Voice/2024/05/21/15e39520-5451-4bde-8487-23cf7722302f_analysis_2024-05-21T14.3A47.3A00Z.json'
# key = unquote(key)
# print(key)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # url = 'https://dev247754.service-now.com'
    # incident_sys_id = 'f7068708c31a021067a9563ed4013160'
    # incident_url = f'{url}/nav_to.do?uri=%2Fincident.do%3Fsys_id%3D{incident_sys_id}'
    
    # response = {
    #     'statusCode': 302,
    #     'headers':{
    #         'Location': incident_url
    #     }
    # }
    # return response
    
    
    
    
# import json
# import boto3

# transcribe = boto3.client('transcribe')
# kinesis = boto3.client('kinesis')



# def lambda_handler(event, context):
#     print(event)
    
    
#     stream_arn = event['Details']['ContactData']['MediaStreams']['Customer']['Audio']['StreamARN']
#     contact_id = event['Details']['ContactData']['ContactId']
    
    
#     response = transcribe.start_stream_transcription(
#         Language = 'en-US',
#         MediaSampleRateHertz=8000,
#         MediaEncoding='pcm',
#         mediaStream ={
#             'MediaStramType': 'kinesisVideoStream',
#             'KinesisVideoStream': {
#                 'StreamArn': stream_arn
#             }
#         },
#         OutputBucketName ='outputbucketsn',
#         OutputKey= f'transcriptions/{contact_id}/'
        
#         )
        
#     return {
#         'statusCode': 200,
#         'body': response
#     }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # print('Event:', json.dumps(event, indent=2))

    # contact_id = event['detail'].get('ContactId')
    # rule_name = event['detail'].get('RuleName')
    # transcript = event['detail'].get('Transcript')

    # # Example logic: Print the detected keywords
    # if transcript and 'TranscriptResults' in transcript:
    #     for result in transcript['TranscriptResults']:
    #         if not result.get('IsPartial', True):
    #             print('Detected Keywords:', result['Transcript'])

    # # Additional processing logic here
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Processing complete')
    # }

    
    