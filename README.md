# Bank App
This aplication deploys a backend for a bank app.
## Diagram
![Diagrama en blanco](https://user-images.githubusercontent.com/72634666/123903025-e8628280-d93b-11eb-998a-b8c7e510de8d.jpeg)![Diagrama en blanco](https://user-images.githubusercontent.com/72634666/123893615-bd236780-d92a-11eb-99e5-1eea512187cf.jpeg)

## Ejemplos
Ingresar estos 3 clientes para poder hacer los ejemplos de transacciones
## 3 clientes
{
    "name":"Pedro",
    "lastName": "Sanchez",
    "moneyInAccount":"500$",
    "salaryPerMonth": "5000$",
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
    "moneyInAccount":"100$",
    "salaryPerMonth": "2000$",
    "company": "company_006"


}



## 3 transacciones
No hay sufieciente dinero por parte emisor
{
    "emisor": "client_002",
    "receptor": "client_001",
    "monto": "200$",
    "fecha": "28/06/2020"
}
Todo bien
{
    "emisor": "client_002",
    "receptor": "client_001",
    "monto": "20$",
    "fecha": "28/06/2020"
}
Todo bien
{
    "emisor": "client_002",
    "receptor": "client_003",
    "monto": "20$",
    "fecha": "28/06/2020"
}

