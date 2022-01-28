<h1 align="center">
   <a href="#"> CashBack GB </a>
</h1>

<h3 align="center">
    Rest API for registering purchases and cashback consultation. 
</h3>

<p align="center">
  
  <a href="https://www.python.org/downloads/release/python-390/">
    <img alt="Python version" src="https://img.shields.io/badge/python-_>=_3.9-blue.svg">
  </a> 
  
  <a href="https://github.com/psf/black">
    <img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
   
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/wlsouza/cashbackgb">
  
  <a href="https://github.com/wlsouza/cashbackgb/commits/master">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/wlsouza/cashbackgb">
  </a>
    
  <img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">
</p>


<h4 align="center"> 
	 Status: Finished
</h4>

<p align="center">
 <a href="#-about">About</a> •
 <a href="#%EF%B8%8F-features">Features</a> •
 <a href="#-demo">Demo</a> • 
 <a href="#-running-the-project">Running the project</a> • 
 <a href="#-tech-stack">Tech Stack</a> •
 <a href="#-how-to-contribute">How to contribute</a> •
 <a href="#%EF%B8%8F-autor">Author</a> • 
 <a href="#-license">License</a>

</p>


## 💻 About

**Cashback GB** - is an API project that aims to provide a backend for a web system where resellers can register their purchases and track the cashback return of each one. 

---

## ⚙️ Features

### API Routes:  
✔️ Route to register a new reseller. (It's called user within API and database)  
✔️ Route to validate a reseller login and obtain a JWT token.  
✔️ Route to register a new purchase.  
✔️ Route to edit a validating purchase.  
✔️ Route to delete a purchase in validation.  
✔️ Route to list registered purchases.  
✔️ Route to display cashback accumulated so far. (Sum of purchases registered in the API + value from external API) 

### Technical resources:  
✔️ Interactive documentation with OpenAPI (swagger)  
✔️ Documentation with Redoc  
✔️ JWT authentication  
✔️ Unitary tests  
✔️ Integration Tests  
✔️ Asynchronous database layer (both Postgres and SqLite)  
✔️ Database Migrations  
✔️ Dockerized application  
✔️ CI/CD using **AWS RDS**, **AWS ECR**, **AWS Lambda** and **AWS API Gateway** and **Serverless framework**  

---

## 👀 Demo

The application is available on AWS:

<a href="https://85oefk100h.execute-api.us-east-1.amazonaws.com/dev/docs">
  <img alt="CashBack GB" src="https://img.shields.io/badge/Access%20interactive%20documentation%20-OpenAPI-%2304D361">
</a>
<a href="https://85oefk100h.execute-api.us-east-1.amazonaws.com/dev/docs">
  <img alt="CashBack GB" src="https://img.shields.io/badge/Access%20documentation%20-Redoc-blue">
</a>

---
## 🚀 Running the project

### Pre-requisites

Before you begin, you will need to have the following tools installed on your machine:  
* [Git](https://git-scm.com)  
* [Python](https://www.python.org).  
* In addition, it is good to have an editor to work with the code like [VSCode](https://code.visualstudio.com/)  
* And if you want to run using containers you will need [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).   

Obs:
  * If an environment variable named APP_ENVIRONMENT is set to "PROD", the API by default will try to connect to a postgres database, otherwise it will create a sqlite database called temp.db in the project's root folder.  
  * I'm assuming you already know and will follow these steps using a virtualenv. If you don't know, see more here. 

> <details open>
>	 <summary>
> 		<b> Running locally </b>
>	 </summary>
> 
>	 1. Clone this repository:  
>	 	`$ git clone https://github.com/wlsouza/cashbackgb.git`  
> 	2. Access the project folder cmd/terminal:  
>	 	`$ cd cashbackgb`  
> 	3. Install the dependencies (step for Linux users only):  
> 		`$ make install-dev`  
>	 4. Install the dependencies (step for windows users only):  
>	 	`$ pip install -r ./requirements.txt`  
> 		`$ pip install -r ./requirements-dev.txt`  
> 	5. Run the application in development mode:  
> 		`$ uvicorn app.main:app `  
>	 6. The server will start at port: 8000 - [see the docs](http://localhost:8000/docs)
> </details>


> <details>
> 	<summary>
> 		<b> Running in docker </b>
> 	</summary>
> 
> 	1. Clone this repository:  
> 		`$ git clone https://github.com/wlsouza/cashbackgb.git`   
> 	2. Access the project folder cmd/terminal:  
> 		`$ cd cashbackgb`  
> 	3. Create a copy and rename the file "example.env" to ".env":  
>		`$ cp example.env .env` - (for Linux users)  
>		`$ copy example.env .env` - (for Windows users)  
>	4. Run the docker-compose in development mode:  
>		`$ docker-compose build --no--cache && docker-compose up -d`  
> 	5. The server will start at port: 8000 - [see the docs](http://localhost:8000/docs)
> </details>


> <details>
>	<summary>
>		<b> Running tests </b>
>	</summary>
>
>	1. Clone this repository:  
>		`$ git clone https://github.com/wlsouza/cashbackgb.git`  
>	2. Access the project folder cmd/terminal  
>		`$ cd cashbackgb`  
>	3. Install the dependencies (step for Linux users only)  
>		`$ make install-dev`  
>	4. Install the dependencies (step for windows users only)  
>		`$ pip install -r ./requirements.txt`  
>		`$ pip install -r ./requirements-dev.txt`  
>	5. Run the tests (step for Linux users only)  
>		`$ make test`  
>	6. Run the tests (step for windows users only)  
>		`$ set APP_ENVIRONMENT="TEST"`  
>		`$ alembic upgrade head`  
>		`$ pytest app/tests/ -v --cov=app`  
> </details>

---

## 🛠 Tech Stack

The following tools were used in the construction of the project:

  [Python](https://www.python.org) + [FastAPI](https://fastapi.tiangolo.com)


> <details open>
>	<summary>
>		<b> Dependences </b>
>	</summary>
>
> -   [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)  
> -   [psycopg2](https://github.com/psycopg/psycopg2)  
> -   [asyncpg](https://github.com/MagicStack/asyncpg)  
> -   [aiosqlite](https://github.com/omnilib/aiosqlite)  
> -   [alembic](https://github.com/sqlalchemy/alembic)  
> -   [passlib](https://github.com/glic3rinu/passlib)  
> -   [pyjwt](https://github.com/jpadilla/pyjwt)  
> -   [httpx](https://github.com/encode/httpx)  
> -   [mangum](https://github.com/jordaneremieff/mangum)  
> </details>

> <details>
>	<summary>
>		<b> Development Dependences </b>
>	</summary>
>
> -   [black](https://github.com/psf/black)  
> -   [flake8](https://github.com/PyCQA/flake8)  
> -   [isort](https://github.com/PyCQA/isort)  
> -   [faker](https://github.com/joke2k/faker)  
> -   [pytest](https://github.com/pytest-dev/pytest)  
> -   [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)  
> -   [pytest-cov](https://github.com/pytest-dev/pytest-cov)  
> -   [pygount](https://github.com/roskakori/pygount)  
> </details>
---

## 💪 How to contribute

1. Fork the project.
2. Create a new branch with your changes: `git checkout -b my-feature`
3. Save your changes and create a commit message telling you what you did: `git commit -m" feature: My new feature "`
4. Submit your changes: `git push origin my-feature`

---

## 🦸‍♂️ Autor

<a href="https://github.com/wlsouza">
 <img style="border-radius: 50%;" src="https://github.com/wlsouza.png" width="100px;" alt=""/>
 <br />
 <sub><b>Wellington Lorenço de Souza</b></sub></a> <a href="https://github.com/wlsouza" title="Github Wellington">🚀</a>
 <br />

[![Linkedin Badge](https://img.shields.io/badge/-Wellington-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://in.linkedin.com/in/wellingtonlorenco)](https://in.linkedin.com/in/wellingtonlorenco) 
[![Gmail Badge](https://img.shields.io/badge/-wlsouza@protonmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:wlsouza@protonmail.com)](mailto:wlsouza@protonmail.com)

---

## 📝 License

This project is under the license [MIT](./LICENSE).
