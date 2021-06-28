import os
import boto3
import json
from boto3.dynamodb.conditions import Key
clients_table = os.environ['BANK_TABLE'] 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(clients_table)

def getClient(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    array_path = path.split("/") ##[user,123]
    client_id = array_path[-1]
   
    response = table.get_item(
        Key={
            'pk': client_id,
            'sk': 'info'
        }
    )
    item = response['Item']
    print("imprimiendo item:",item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

def putClient(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    print("Imprimiendo paht:",path)
    array_path = path.split("/") ##[user,123]
    client_id = array_path[-1]
    
    body = event["body"]   
    body_obj = json.loads(body)
    
    print("Imprimiendo path:",client_id)
    
    table.put_item(
        Item={
            'pk': client_id,
            'sk': 'info',
            'name': body_obj['name'],
            'lastName': body_obj['lastName'],
            'moneyInAccount': body_obj['moneyInAccount'],
            'company': body_obj['company'],
            'salaryPerMonth': body_obj['salaryPerMonth']
            
       
        }
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
    