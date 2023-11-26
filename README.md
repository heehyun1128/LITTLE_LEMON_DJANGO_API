## User Story & API Routes

1.	The admin can assign users to the manager group

    POST http://localhost:8000/api/groups/manager/users

    ```
        {
            "username": "user2",
            "email": "user2@user2.com"
        }
    ```
    
     
2.	You can access the manager group with an admin token

    GET http://localhost:8000/api/groups/manager/users

3.	The admin can add menu items 

    POST http://localhost:8000/api/menu-items/

    Sample data:

    ```
        {
            "title": "MenuItem5",
            "price": 50.00,
            "featured": false,
            "category": {
                "id": 1,
                "slug": "Slug1",
                "title": "Category1"
            }
        }
    ```

4.	The admin can add categories

    POST http://localhost:8000/api/category

    ```
        {
            "slug": "Slug2",
            "title": "Category4"
        }
    ```

5.	Managers can log in 

    POST http://localhost:8000/api/login/

    ```
        {
            "username":"user1",
            "password":"User1pass123"
        }
    ```
    
6.	Managers can update the item of the day

    UPDATE http://localhost:8000/api/menu-items/1

    ```
        {
            "id": 1,
            "category": {
                "id": 1,
                "slug": "Slug2",
                "title": "Category2"
            },
            "title": "MenuItem1",
            "price": "30.00",
            "featured": false
        }
    ```

    DELETE http://localhost:8000/api/menu-items/3

7.	Managers can assign users to the delivery crew

    POST http://localhost:8000/api/groups/delivery-crew/users
    ```
        {
            "username":"user1"
        }
    ```

8.	Managers can assign orders to the delivery crew

    PUT http://localhost:8000/api/orders/2

    ```
        {
            "delivery_crew": 4
        }
    ```

9.	The delivery crew can access orders assigned to them

    LOG IN as delivery(username): http://localhost:8000/api/login
    
    GET http://localhost:8000/api/orders

10.	The delivery crew can update an order as delivered

    PATCH http://localhost:8000/api/orders/1

    ```
        {
            "status": true
        }
    ```

11.	Customers can register

    POST http://localhost:8000/api/register/

    ```
        {
            "username":"newuser1",
            "password":"Newuser1pass123",
            "email":"newuser1@newuser1.com"
        }
    ```

12.	Customers can log in using their username and password and get access tokens

    POST http://localhost:8000/api/login/ TO LOG IN

    ```
        {
            "username":"newuser",
            "password":"Newuserpass123"
        }
    ```

13.	Customers can browse all categories 

    GET http://localhost:8000/api/category

14.	Customers can browse all the menu items at once

    GET http://localhost:8000/api/menu-items/

15.	Customers can browse menu items by category

    GET http://localhost:8000/api/menu-items/category/1/

16.	Customers can paginate menu items

    GET http://localhost:8000/api/menu-items/paginated/

17.	Customers can sort menu items by price

    GET http://localhost:8000/api/menu-items/sort=price

18.	Customers can add menu items to the cart

    POST http://localhost:8000/api/cart/menu-items

    ```
        {
            "user": 5,
            "menuitem": "4",
            "quantity": 1,
                    "unit_price": 40.00,
                    "price": 40.00
        }
    ```

19.	Customers can access previously added items in the cart

    LOG IN AS user1

    GET http://localhost:8000/api/cart/menu-items

20.	Customers can place orders

    POST http://localhost:8000/api/orders

    ```
        {
    
            "delivery_crew": 4, 
            "status": true,
            "total": 20.00,
            "date": "2023-11-23",
            "menu_items": [
                {
                "menuitem_id": 1, 
                "quantity": 2
                }
            ]    
        }
    ```

21.	Customers can browse their own orders

    GET http://localhost:8000/api/orders

