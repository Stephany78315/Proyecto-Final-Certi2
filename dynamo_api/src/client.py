import os
import boto3
import json
import bank

from boto3.dynamodb.conditions import Key
clients_table = os.environ['BANK_TABLE'] 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(clients_table)


##START ANDREA
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
        'body': json.dumps('CLIENE CORRECTAMENTE AGREGADO')
    }
    
    
def putTransaction(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    print("Imprimiendo paht:",path)
    array_path = path.split("/") ##[user,123]
    transaction_id = array_path[-1]
    
    body = event["body"]   
    body_obj = json.loads(body)
    
    print("Imprimiendo path:",transaction_id)
    
    #### 1. analyse the company before adding the transaction  , getClient -> get company -> verificar commpany
    
    emisor = body_obj['emisor']
    receptor = body_obj['receptor']
    montoStr = body_obj['monto']
    
    #getClient emisor
    response1 = table.get_item(
        Key={
            'pk': emisor,
            'sk': 'info'
        }
    )
    print("printing response1", response1)
    
    item_emisor = response1['Item']
   
    company_id = item_emisor['company']
    company_p = "/company/" + company_id
    
    prueba = {'path': company_p, 'try': "trying" } 
    
    answer = bank.getCompany(prueba, prueba)
    
    print(json.dumps(answer))
    #answer2= json.loads(answer)
    
    if "No Confiable" not in (answer['body']) :
        #seguimos con el procesos
    
        #### 2. verificar el dinero suficiente the emisor
    
        dineroEmisor = item_emisor['moneyInAccount']
        dineroEmisor =  dineroEmisor.replace("$","")
        
        montoStr = montoStr.replace("$","")
        
        moneyLeft = int( dineroEmisor) - int(montoStr)
        if ( moneyLeft < 0 ):
            return {
            'statusCode': 200,
            'body': json.dumps('TRANSACCION NO COMPLETADA, DINERO SUPERIOR AL POSEIDO')
            }
        else:
            ##seguimos con el proceso
            #### 3. quitar el dinero de emisor
            newMoney = str(moneyLeft) + "$"
            
            table.put_item(
                Item={
                    'pk': emisor,
                    'sk': 'info',
                    'name': item_emisor['name'],
                    'lastName': item_emisor['lastName'],
                    'moneyInAccount': newMoney ,
                    'company': item_emisor['company'],
                    'salaryPerMonth': item_emisor['salaryPerMonth']
                    
               
                }
            )
            
            #### 4. add el dinero a receptor
            
            #getClient receptor
            response4 = table.get_item(
                Key={
                    'pk': receptor,
                    'sk': 'info'
                }
            )
            print("printing response4", json.dumps(response4))
            item_receptor = response4['Item']
            
            dineroReceptor = item_receptor['moneyInAccount'].replace("$","")
            montoTotal = int(dineroReceptor) + int(montoStr)
            
            newMoney2 =  str(montoTotal) + "$"
            
            table.put_item(
                Item={
                    'pk': receptor,
                    'sk': 'info',
                    'name': item_receptor['name'],
                    'lastName': item_receptor['lastName'],
                    'moneyInAccount': newMoney2,
                    'company': item_receptor['company'],
                    'salaryPerMonth': item_receptor['salaryPerMonth']
                    
               
                }
            )
            
            
            #### 5. agregar la transaccion
            
            table.put_item(
                Item={
                    'pk': transaction_id,
                    'sk': 'info',
                    'emisor': body_obj['emisor'],
                    'receptor': body_obj['receptor'],
                    'monto': body_obj['monto'],
                    'fecha': body_obj['fecha']
                
                    
               
                }
            )
    
    else:
        return {
        'statusCode': 200,
        'body': json.dumps('TRANSACCION NO COMPLETADA, COMPANY NO CONFIABLE')
    }
    
   
    
    

    
    return {
        'statusCode': 200,
        'body': json.dumps('TRANSACCION CORRECTLY DONE')
    }
    ##END ANDREA
    
    
    