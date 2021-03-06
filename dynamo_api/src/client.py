import os
import boto3
import json
import bank

from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr 

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
    
    
    try:
        item = response['Item']
    except:
        return {
        'statusCode': 500,
        'body': json.dumps("No existe el cliente")
        }
   
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
        'body': json.dumps('CLIENTE CORRECTAMENTE AGREGADO')
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
    fecha = body_obj['fecha']
    
    #getClient emisor
    
    response1 = table.get_item(
        Key={
            'pk': emisor,
            'sk': 'info'
        }
    )
    
    print("printing response1", response1)
    try:
        item_emisor = response1['Item']
    except:
        return {
        'statusCode': 500,
        'body': json.dumps("No existe el cliente")
        }
   
    company_id = item_emisor['company']
    company_p = "/company/" + company_id
    
    prueba = {'path': company_p, 'try': "trying" } 
    
    answer = bank.getCompany(prueba, prueba)
    
    print(json.dumps(answer))
    #answer2= json.loads(answer)
    
    if "No Confiable" not in (answer['body']) :
        #seguimos con el procesos
    
         #Primera anomalia max 6 transacciones por cliente
        responseT = table.scan(
            
           
            ##KeyConditionExpression=Key('pk').begins_with('transaction') & Key('sk').eq('info'),
      
            FilterExpression =Key('pk').begins_with('transaction') & Attr('fecha').eq(fecha) & Attr('receptor').eq(receptor)
        )
        
        ##list_transactions = responseT['Items']
        numTrans = 1
        
        for i in responseT['Items']:
            numTrans = numTrans + 1
            
            
        print("printing numero de transacciones:",numTrans)
       ## numberTrans = len(list_transactions)
        
    
        #### 2. verificar el dinero suficiente the emisor
    
        dineroEmisor = item_emisor['moneyInAccount']
        dineroEmisor =  dineroEmisor.replace("$","")
        
        saldoEmisor = item_emisor['salaryPerMonth']
        saldoEmisor =  saldoEmisor.replace("$","")
        
        montoStr = montoStr.replace("$","")
        
        moneyLeft = int( dineroEmisor) - int(montoStr)
        if ( moneyLeft < 0 ):
            return {
            'statusCode': 200,
            'body': json.dumps('TRANSACCION NO COMPLETADA, DINERO SUPERIOR AL POSEIDO')
            }
        elif ( int(montoStr) > 20000 and int(saldoEmisor) < 2000 ):  ### Verificar anomalia 1
            return {
            'statusCode': 200,
            'body': json.dumps('TRANSACCION NO COMPLETADA, SE ENCONTRO UNA ANOMALIA DE TIPO 1: SALARIO INSUFICIENTE PARA REALIZAR ESTA TRANSACCION')
            }
        elif (numTrans > 5): ### Verificar anomalia 2
            return{
            'statusCode': 200,
            'body': json.dumps('TRANSACCION NO COMPLETADA, SE ENCONTRO UNA ANOMALIA DE TIPO 2: HA ALCANZADO EL LIMITE DE TRANSACCIONES EN UN DIA HACIA LA MISMA CUENTA')
            }
        elif ( int(montoStr) > 10000 and moneyLeft < 100): ### Verificar anomalia 3
            return {
            'statusCode': 200,
            'body': json.dumps('TRANSACCION NO COMPLETADA, SE ENCONTRO UNA ANOMALIA DE TIPO 3: SALDO INSUFICIENTE PARA REALIZAR ESTA TRANSACCION')
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
            try:
                item_receptor = response4['Item']
            except:
                return {
                    'statusCode': 500,
                    'body': json.dumps("No existe el receptor")
                }
            
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
            responseTrans = table.scan(
            
           
            ##KeyConditionExpression=Key('pk').begins_with('transaction') & Key('sk').eq('info'),
      
                FilterExpression =Key('pk').begins_with('transaction')
            )
            print(json.dumps("antes del len.........."))
            aux = len(responseTrans['Items'])
            print(json.dumps(aux))
            aux2 = "%03d" % (aux + 1)
              

            #### 5. agregar la transaccion
            
            table.put_item(
                Item={
                    'pk': 'transaction_' + str(aux2),
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
    
def getTransaction(event, context):
        print(json.dumps({"running": True}))
        print(json.dumps(event))
        
        path = event["path"]    #user/transaction_001
        array_path = path.split("/") ##[user,transaction_001]
        tran_id = array_path[-1]
        
        response = table.get_item(
            Key={
                'pk': tran_id,
                'sk': 'info'
            }
        )
        
        
        try:
            item = response['Item']
        except:
            return {
            'statusCode': 500,
            'body': json.dumps("No existe transaccion")
            }
       
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }

    
    