# Bank App
This aplication deploys a backend for a bank app.
## Diagram
![Diagrama en blanco (1)](https://user-images.githubusercontent.com/72634666/124035959-4a1dfd80-d9cb-11eb-9391-da53f2671b61.jpeg)


## Cosas que debe hacer para hacer correr
En el archivo Proyecto-Final-Certi2/dynamo_api/deployment.sh debe cambiar el bucket por uno que lo que tenga en su cuenta.
Se debe hacer lo mismo en los archivos Proyecto-Final-Certi2/lambda/deployment.sh y Proyecto-Final-Certi2/deploymentSMM.sh.



## Ejemplos
Ingresar estos 3 clientes para poder hacer los ejemplos de transacciones
## 3 clientes


{
    "name":"Pedro",
    "lastName": "Sanchez",
    "moneyInAccount":"40000$",
    "salaryPerMonth": "1000$",
    "company": "company_001"


}
{
    "name":"Juan",
    "lastName": "Gonzalez",
    "moneyInAccount":"100$",
    "salaryPerMonth": "5000$",
    "company": "company_002"


}
{
    "name":"Richard",
    "lastName": "Perez",
    "moneyInAccount":"900$",
    "salaryPerMonth": "2000$",
    "company": "company_003"


}
{
    "name":"Michael",
    "lastName": "Bolaños",
    "moneyInAccount":"12000$",
    "salaryPerMonth": "2000$",
    "company": "company_003"


}




## 3 transacciones
#IMPORTANTE las transacciones se autoincrementan 

Path: /transactions
"TRANSACCION NO COMPLETADA, SE ENCONTRO UNA ANOMALIA DE TIPO 1: SALARIO INSUFICIENTE PARA REALIZAR ESTA TRANSACCION"
{
    "emisor": "client_001",
    "receptor": "client_002",
    "monto": "21000$",
    "fecha": "28/06/2020"
}
## Anomalia 2  
Path: /transactions
{
    "emisor": "client_001",
    "receptor": "client_002",
    "monto": "50$",
    "fecha": "28/06/2020"
}
Path: /transactions
Path: /transactions
Path: /transactions
{
    "emisor": "client_003",
    "receptor": "client_002",
    "monto": "50$",
    "fecha": "28/06/2020"
}
Path: /transactions

Error de Anomalia 1 Limite de transacciones en un dia
Path: /transactions



## Anomalia 3 "TRANSACCION NO COMPLETADA, SE ENCONTRO UNA ANOMALIA DE TIPO 3: SALDO INSUFICIENTE PARA REALIZAR ESTA TRANSACCION"
Path: /transactions
{
    "emisor": "client_004",
    "receptor": "client_001",
    "monto": "11950$",
    "fecha": "28/06/2020"
}





