import json
import boto3
import os
import urllib 
from urllib.request import urlopen
 


bank_table = os.environ['BANK_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(bank_table)




def getCompany(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] # "/company/company_123"
    array_path = path.split("/") # ["", "company", "123"]
    comp_id = array_path[-1]
    
    #id_empresa = "company_" + comp_id
    
    print(json.dumps("antes de get Item"))
    response = table.get_item(
        Key={
            'pk': comp_id,
            'sk': "sk"
        }
    )
    
   
    print(json.dumps("despues de get Item"))
    if 'Item' in response:

        print(json.dumps("si response no es None"))
        
        item = response['Item']
        
        if item["Confiable"] == "Si":
            return{
                'body': json.dumps('Confiable')
            }
        else:
            return{
                'body': json.dumps('No Confiable')
            }
            
        
       
    else:
        
        print(json.dumps("entramos al None"))
        
        response = urlopen('https://bucket-empresas.s3.us-east-2.amazonaws.com/empresas.json')
                            

          
        
        data_json = json.loads(response.read())
        
        encontrado = False
        
        for i in data_json:
            if i["id"] == comp_id:
                encontrado = True
                print(json.dumps("entra al if"))
                print(json.dumps(i))
                table.put_item(
                    Item={
                        'pk': comp_id,
                        'sk': 'sk',
                        'Confiable': 'Si'
                    }
                )
                return {
                'body': json.dumps('Confiable')
                }
               
        
        
        if encontrado == False:
            table.put_item(
                    Item={
                        'pk': comp_id,
                        'sk': 'sk',
                        'Confiable': 'No'
                    }
                )
            return {
                'body': json.dumps('No Confiable')
                }

    
