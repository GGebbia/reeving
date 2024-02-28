### Reeving Tech Task
This repo contains the code to achieve the objectives of the tech task of Reeving.  
The repo is splitted in two folders (ideally it would be threated as independent git submodules).

Follow the steps below to install the virtual enviroment, create the database and run the backend service.

## Backend setup
In order to setup the backend service follow these steps
```bash
cd backend
make install
make create_db
make run
```
Therefore the backend can be accessible at (`http://127.0.0.1:8000`)


## Frontend setup
In order to setup the frontend service follow these steps
```bash
cd frontend
python3 -m http.server 3000
```
Therefore the frontend can be accessible at (`http://127.0.0.1:3000`)
