import time, json
import boto3, pdb



transcribe = boto3.client('transcribe')
bucket = 'mytestbucketbookman'

job_name = "7"  #must be unique or removed?
job_uri = f"s3://{bucket}/{file}"   ### file from main

transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='wav',
    LanguageCode='en-US',
    OutputBucketName=bucket

)

while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print(f"{status['TranscriptionJob']['TranscriptionJobStatus']}")
    time.sleep(5)
transcript_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
print(f"GOT TRANSCRIPT URL: {transcript_url}")

# get json
itemname = job_name + ".json"

s3 = boto3.resource('s3')
obj = s3.Object(bucket, itemname)
body = obj.get()['Body'].read()
data = json.loads(body)
print(data['results']['transcripts'][0]['transcript'])
# save output as text