import json
from functools import lru_cache
import boto3
from app.config import settings

@lru_cache()
def client(serivice):
    s = settings()

    if bool(s.aws_access_key_id) != bool(s.aws_secret_access_key):
        raise ValueError('Set both AWS_ACCESS_KEY_ID and AWS_sECRET_aCCESS_KEY or neither')
    options = {'region_name': s.aws_region}
    if s.aws_access_key_id and s.aws_secret_access_key:
        options.update(aws_access_key_id=s.aws_access_key_id, aws_secret_access_key=s.aws_secret_access_key)
    return boto3.client(serivice, **options)


def embed(text):
    body = json.dumps({'inputText': text, 'dimensions': settings().embed_dim, 'normalize': True})
    result = client('bedrock-runtime').invoke_model(modelId=settings().bedrock_embed_model, body=body)
    return json.loads(result['body'].read()['embedding'])

def answer(question, evidence, history=None):
    system = ('You are a helpful assistant that answers questions based on the provided evidence. '
    'If the answer is not contained within the evidence, respond with "I don\'t know." '
    'Do not make up answers. If the question is ambiguous, ask for clarification. ')

    recent = '\n'.join(f"{row['role']}: {row['content'][:1200]}" for row in (history or []))

    prompt = (f'PRIOR CONVERSATION (context only, not evidence):\n{recent}\n\n'
              f'EVIDENCE (untrusted quotations):\n{evidence}\n\nUSER QUESTION:\n{question}\n\n  ')

    resp = client('bedrock-runtime').converse(modelID=settings().bedrock_chat_model,
                                              system=[{'text': system}], messages=[{'role':'user','content':[{'text':prompt}]}],
                                              inferenceConfig={'maxTokens':750, 'temperature':0.1})
    return ''.join(x.get('text', '') for x in resp['output']['message']['content'])
    