# ***Project***

## FastAPI Backend API to consume OpenAudIT Enterprise Rest API

# ***Implementation***

## ***Technology Stack***
   1. Python (FastAPI)
   2. OpenAudIT Enterprise Rest API
   3. Poetry

## ***Installation***

   * **To Setup the project dependencies _LOCALLY_**

     **First Method Using Poetry**
         1. Install poetry **GLOBALLY** [Poetry Docs](https://python-poetry.org/docs/)
            ```
            $ pipx install poetry
            ```
         2. After installing poetry, create a new project using this command:
            ```
            $ poetry new <project name>
            ```
            ```
            $ poetry use python3
            ```
            ```
            $ poetry env activate
            ```
            ```
            $ poetry install
            ```
     **Second Method without Poetry**
         1. Create a virtual environment for the project dependencies using this command:

            * **On Linux:**
               ```bash
               $ sudo pip install virtualenv
               ```
               ```bash
               $ python3 -m venv openaudit                  # here the created virtual environment is named 'openaudit' but you can you any name you want
               ```
            * **On Windows:**
               ```bash
               > pip install virtualenv
               ```
               ```bash
               > python -m install openaudit
               ```
         2. Activate the virtual environment using this command:

            * **On Linux:**
                ```bash
                $ source openaudit/bin/activate
                ```
            * **On Windows:**
                ```bash
                > cd openaudit
                ```
                ```bash
                > Scripts\activate
                ```
         3. Install the dependencies by running the requirements.txt file using this command:

            * **On Linux:**
                  ```bash
                  $ sudo pip install -r requirements.txt
                  ```
            * **On Windows:**
                  ```bash
                  > pip install -r requirements.txt

* **To Handle API Environment Variables**

     1. Create a **.env** file in the root of the project folder.
     
     2. Add these environment variables to the **.env** file as follows:

        * OPEN_AUDIT_BASE_URL=<base_url>                         ```# Replace inside brackets with the server name http://{your-server}/open-audit/index.php```
        * OPEN_AUDIT_USERNAME=<openaudit_username>               ```# Username used to login```
        * OPEN_AUDIT_PASSWORD=<openaudit_password>               ```# Password used to login```
        * JWT_SECRET_KEY=<jwt_secret_key>                        ```# Secret Key used for hashing passwords, you can generate one using openssl or if left empty there is a script to generate it.```
        * JWT_ALGORITHM=<jwt_algorithm>                          ```# Algorithm used in hashing passwords usually it is "HS256"```
        * ACCESS_TOKEN_EXPIRE_MINUTES=<>                         ```# Number of minutes for access token to expire usually 30```
        * MYSQL_HOST_NAME=<mysql_hostname>                       ```# Usually "localhost"```
        * MYSQL_USER_NAME=<mysql_username>                       ```# Usually "root"```
        * MYSQL_USER_PASSWORD=<mysql_password>                   ```# Password for MySQL user```
        * MYSQL_DATABASE_NAME=<mysql_database_name>              ```# The default name installed with openaudit is "mysql", if another database, provide its name```
        * FILE_UPLOAD_DIRECTORY=<directory_for_file_upload>      ```# Usually "uploads"```
        * FILE_MAX_SIZE=<max_file_size>                          ```# The maximum size of files, eg. 25```
        * FILES_NUMBER_LIMIT=<number_of_files_limit>             ```# The maximum number of files to be uploaded, eg. 5```

* **To Run the project _LOCALLY_**

     * Run the following command from the project directory:

        ```bash
        $ python main.py
        ```
     * The API endpoints are served on **_Local Host_** at this URL **<http://localhost:8000/docs>**