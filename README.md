# bazar-online-book-store

## About bazar. com

bazar . com is one of a distributed operating system course project.
bazar online book store. It is a microservices builds based on the RAST API using Flask as it is online book store, and contains only four books:
|book title |topic |
|----------------|-----------------------------|
|How to get a good grade in DOS in 20 minutes a day| distributed systems  
|RPCs for Dummies| distributed systems  
|Xen and the Art of Surviving Graduate School| graduate school
|Cooking for the Impatient Graduate Student| graduate school

The project is divided into three main servers:

- front-end server which receive all the request form the user and propagate it back-end servers
- catalog server which consider as one of the back-end server
- order server and its the second back-end server

## Installation

This repository is consist of three main files, each of which represents one of the three servers.
The order server and catalog server files both contain a python scripts called server_configuration.py through which you can change the IP and the ports number of the servers; Where front-end server contains this information inside the front-end server.py file, both servers are running on localhost. If you want to change the environment to works on a different machine, just modify these files to suit the new environment.
After that make sure pip3 is installed if not apply the following command on the terminal

```
$ sudo apt install python3-pip
```

After that, if all three server run at the same machine open the terminal from bazar-online-book-store directory then apply the following commands:

```
$ pip3 install -r requirements.txt
```

if the three servers run at different machines open the terminal from each machine on the server directory according to its name and apply the following installation command:

```
$ pip3 install -r requirements.txt
```

## about the servrs

### front-end server

A front-end server is a server that receives data from the end-user and sends it to each of the back-end servers. This server works under microservices known as **Flask**, which is one of the simplest and most popular microservices that are written using the python.
Flask connects each route with a method, so when a request arrives at this URL, the method linked with it is called to be executed and then the client is responded. All requests that reach a front-end server are sent to another server using a package called **request**, which sends an http request to another server.

### catalog server and order server

Both order and catalog servers work in the same way as the font-end server, as it is based on **Flask** microservices and the order server uses **request** to communicate with the catalog server.
What distinguishes each of these two servers is that they contain a database, as they store data in a simple database known as **SQLite**, and communication with the data base in a simple way without the need to write a complex queries **SQL Alchemy** and **Marshmallow** was used to interact with the database via object relational mapper.
The order server stores all purchases, while the catalog server storing books and their information from quantity, title, topic, and price.

Bazar works fine without any problems, but it may need some improvements to increase security and provide authentication, as it is possible to the the end-user at this moment communicates with the back-end servers directly without verifying the person's identity. Also, bazar servers support a certain number of users, which may cause problems during peak periods, so it is preferable to use more back-end servers that can better distribute the load on them and ensure speedy performance.

## The API

Bazar is divided into two main parts, which are the front-end server and back-end servers.

### front-end server

The fron-end server handles the process of communicating with the end-user, as the user sends the request directly to it and it sends it to the back-end servers according to the nature of the request.

The following table shows all the operations provided by the REST API for this server:
| operation | method | route | request body | response | description |
|-----------------|--------|------------------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| search | GET | /search/<string:topic> | `empty` | `200`, return an array under this topic each element contents book id and title, otherwise `404` when no book under this tpoic | get all books under this topic |
| lookup | GET | /lookup/<int:id> | `empty` | `200` if the book exist return more information about the book (title, quantity, and cost) otherwise it return `404` indicates that there is no book with this id | get more information about the book |
| update price | PUT | /update/price/<int:id> | `{ "price" : 900 }` | `200` if the changes happened correctly and the price updated, `400` if the request bad and cant handle it, or `404` if there is no book with this id | update the price of this book |
| update quantity | PUT | /update/item/<int:id> | `{ "quantity" : 900 } ` | `200` if the changes happened correctly and the quantity updated, `400` if the request bad and cant handle it, or `404` if there is no book with this id | update the book quantity |
| buy | PUT | /buy/<int:id> | `empty` | `201` if the purchase process done and stored inside the order database, otherwise it will return `404` to indicate that the book out of stock or does not exist | apply a buy order from a specific book using its id |

At the moment the aim of the fron-end server is to send the request to responsible servers to serve it; These requests are distributed on the catalog-server as it receives search, lookup, update price, and update quantity from the fron-end and the order server receives purchase requests from it.

### back-end server

The tasks in the back-end servers distribution into two parts, where the order server is responsible for the purchase process, and the catalog server displays the information of the existing books on stocks.

#### catalog server:

The catalog server requests arrive from the front-end server and the order server, as it is responsible for many tasks from searching and obtaining boks information, updating the book information from the available quantity and price, checking the available quantities of the book. As shown in the following table, all these operations are provided by the server through these REST APIs:

| operation               | method | route                          | request body           | response                                                                                                                                                                                                                                                            | description                                                | sender server |
| ----------------------- | ------ | ------------------------------ | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------- |
| search                  | GET    | /search/<string:topic>         | `empty`                | `200`, return an array under this topic each element contents book id and title, otherwise `410`when no book under this tpoic                                                                                                                                       | get all books under this topic                             | front-end     |
| lookup                  | GET    | /lookup/<int:id>               | `empty`                | `200` if the book exist return more information about the book (title, quantity, and cost) otherwise it return `404` indicates that there is no book with this id                                                                                                   | get more information about the book                        | front-end     |
| update price            | PUT    | /update/price/<int:id>         | `{ "price" : 900 }`    | `200` if the changes happened correctly and the price updated, `400` if the request bad and cant handle it, or `404` if there is no book with this id                                                                                                               | update the price of this book                              | front-end     |
| update quantity         | PUT    | /update/item/<int:id>          | `{ "quantity" : 900 }` | `200` if the changes happened correctly and the quantity updated, `400` if the request bad and cant handle it, or `404` if there is no book with this id                                                                                                            | update the book quantity                                   | front-end     |
| check the book quantity | GET    | /verify_item_in_stock/<int:id> | `empty`                | `200` if book the book available and its return book id and quantity, `410` if this book is being sold in this store but is not available right now out, `404` if this book is not being sold here                                                                  | check if the book available before apply the buy operation | order         |
| buy                     | PUT    | /buy/<int:id>                  | `empty`                | `204` if the purchase process done at the catalog side and the catalog database updated, `410` if this book is being sold in this store but is not available right now out, otherwise it will return `404` to indicate that the book out of stock or does not exist | apply a buy order from a specific book using its id        | order         |

### order server:

The oder server continues the purchases that reach the front-end server, where the request arrives, it divides it into two parts. The first is to verify the existence of book and its quantity by communicating with the catalog server and after verifying its presence, it sends the second part to the server to reduce the number of available books, and in the event was successfully process , it stores this purchases with it is database

In the table clarify the cases in which the order server may respond:
| route | status code | message body | description |
| ------------- | ----------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| /buy/<int:id> | 201 | return json object contanes the order id and the book id | The purchase was successfully completed and stored in the database |
| /buy/<int:id> | 410 | return a message says: "This book is currently unavailable" | the book out of stock |
| /buy/<int:id> | 530 | return a message says: "The server is not ready to handle the request" | due to an error of the connection between two back-end servers the order server cant handle th request |

## RESTful APIs output and the communication between them

### front-end server:

- The output of the search process

  - there are books on this topic:

    request: `GET http://fron-end server/search/distributed systems`

    response status: `200 ok`

    response body:

    ```
    [
        {
            "id": 1,
            "title": "How to get a good grade in DOS in 20 minutes a day"
        },
        {
            "id": 2,
            "title": "RPCs for Dummies"
        }
    ]
    ```

  - there are no books on this topic:

    request: `GET http://fron-end server/search/network`

    response status: `404 NOT FOUND`

    response body:

    ```
    {
    "message": "There are no books under this topic"
    }
    ```

- The output of the lookup process

  - there are book with this ID:

    request: `GET http://fron-end server/lookup/1`

    response status: `200 ok`

    response body:

    ```
    {
    "cost": 50.0,
    "quantity": 900,
    "title": "How to get a good grade in DOS in 20 minutes a day"
    }
    ```

  - there is no book with this ID:

    request: `GET http://fron-end server/lookup/90`

    response status: `404 NOT FOUND`

    response body:

    ```
    {
    "message": "There is no book with this ID"
    }
    ```

- The output of the update price process

  - there are book with this ID:

    request: `PUT http://fron-end server/price/1`

    request body:

    ```
    {
    "price" : 900
    }
    ```

    response status: `200 ok`

    response body:

    ```
    {
    "cost": 900.0,
    "quantity": 900,
    "title": "How to get a good grade in DOS in 20 minutes a day"
    }
    ```

  - there is book with this ID but there is a problem with request body :

    request: `PUT http://fron-end server/update/price/1`

    request body:

    ```
    {
    "gool" : 900
    }
    ```

    response status: `400 BAD REQUEST`

    response body:

    ```
    {
        "message": "bad request can not handle the request due to invaled data"
    }
    ```

  - there is no book with this ID:

    request: `PUT http://fron-end server/update/price/90`

    request body:

    ```
    {
    "price" : 900
    }
    ```

    response status: `404 NOT FOUND`

    response body:

    ```
    {
    "message": "There is no book with this ID"
    }
    ```

- The output of the update quantity process

  - there are book with this ID:

        request: `PUT http://fron-end server/update/item/1`

        request body:

        ```
        {
        "quantity" : 600
        }
        ````

        response status: `200 ok`

        response body:

        ```
        {
            "cost": 900.0,
            "quantity": 600,
            "title": "How to get a good grade in DOS in 20 minutes a day"
        }
        ```

  - there is book with this ID but there is a problem with request body :

    request: `PUT http://fron-end server/update/item/1`

    request body:

    ```
    {
    "gool" : 900
    }
    ```

    response status: `400 BAD REQUEST`

    response body:

    ```
    {
        "message": "bad request can not handle the request due to invaled data"
    }
    ```

  - there is no book with this ID:

    request: `PUT http://fron-end server/update/item/10`

    request body:

    ```
    {
    "quantity" : 900
    }
    ```

    response status: `404 NOT FOUND`

    response body:

    ```
    {
    "message": "There is no book with this ID"
    }
    ```

- The output of the buy process

  - there are book with this ID:

        request: `PUT http://fron-end server/buy/1`

        response status: `201 CREATED`

        response body:

        ```
        {
            "book_id": 1,
            "order_id": 2
        }
        ```

  - there is book with this ID but not avaiable at the stock :

    request: `PUT http://fron-end server/update/item/2`

    response status: `401 GONE`

    response body:

    ```
    {
        "message": "This book is currently unavailable"
    }
    ```

  - there is no book with this ID:

    request: `PUT http://fron-end server/update/item/10`

    response status: `404 NOT FOUND`

    response body:

    ```
    {
        "message": "This book unavailable"
    }
    ```

### order server:

- The output of the buy process from the order side veiw

  - there are book with this ID:

        request: `PUT http://order server/buy/3`

        response status: `201 CREATED`

        response body:

        ```
        {
            "book_id": 3,
            "order_id": 4
        }
        ```

  - there is book with this ID but not avaiable at the stock :

    request: `PUT http://fron-end server/update/item/2`

    response status: `401 GONE`

    response body:

    ```
    {
        "message": "This book is currently unavailable"
    }
    ```

  - there is no book with this ID:

    request: `PUT http://fron-end server/update/item/80`

    response status: `404 NOT FOUND`

    response body:

    ```
    {
        "message": "This book unavailable"
    }
    ```

### catalog server:

- Search, lookup, buy, update price, and update quntity replies are the same as in order and front-end server.
- check the book quantity:

  - there are book with this ID:

    request: `GET http://catalog server/verify_item_in_stock/3`

    response status: `200 ok`

    response body:

    ```
    {
    "id": 3,
    "quantity": 79
    }
    ```

    - there is no book with this ID:

    request: `GET http://catalog server/verify_item_in_stock/70`

    response status: `404 NOT FOUND`

    response body:

    ```
    {
    "message": "There is no book with this ID"
    }
    ```

    - there is book with this ID but out of stok:

    request: `GET http://catalog server/verify_item_in_stock/2`

    response status: `410 GONE`

    response body:

    ```
    {
    "message": "This book is currently unavailable"
    }
    ```
