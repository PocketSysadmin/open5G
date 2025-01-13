# Open5GS-UERANSIM-CRAAX for Horse

## Execution Instructions:

To start the environment and run the main scripts, use these commands:

```bash
sudo docker volume create mytb-data
sudo docker volume create mytb-logs
docker-compose up --build -d
python3 ./scripts/create_users.py  
python3 ./scripts/execute_gnb_ue.py 
python3 ./TCPserver/server.py & > /dev/null
```

## API for PCAP files

The FastAPI-developed API allows management of `.pcap` packet capture files generated in the 5G environment. Below are the main functions:

- **POST: `/uploadPCAPfiles`**
   - **Description:** Allows you to upload a `.pcap` file to the server with a `timestamp` identifier.
   - **Parameters:**
      - `timestamp` (str): Unique temporal identifier for the file.
      - `file` (UploadFile): `.pcap` file to upload.
   - **Response:** Confirms that the file was successfully saved.

- **GET: `/downloadPCAPfiles/{file_id}`**
   - **Description:** Downloads a specific `.pcap` file using its `file_id` as an identifier.
   - **Parameters:** 
      - `file_id` (str): Identifier of the file to download.
   - **Response:** Returns the `.pcap` file if it exists; otherwise, a 404 error.


- **GET: `/getPCAPfiles`**
   - **Description:** Lists all `.pcap` files available on the server.
   - **Response:** Returns a list with the names of the files.

- **DELETE: `/deletePCAPfile/{file_id}`**
   - **Description:** Deletes a specific `.pcap` file.
   - **Parameters:** 
      - `file_id` (str): Identifier of the file to delete.
   - **Response:** Confirms that the file was deleted or returns a 404 error if it does not exist.

To import these endpoints into a testing tool, you can use the Postman collection provided in the file `api/docs/5Gcore.postman_collection.json`. This collection contains examples of each endpoint, facilitating the use of the API for testing or automation operations.

## Monitoring and Traffic Generation Scripts

The system includes specific commands for running monitoring and traffic generation scripts. Here are the usage instructions:

**Extecute the script:**
```bash
python3 cliente.py
```

Help:  
- `monitoring <time> <steps>` - Executes the monitoring script X time in X steps 
- `trafgen ping <ID_UE_0-9> <time>` - Executes the traffic generation script in the specified UE, with the selected type of traffic for X
time. 
- `trafgen media <time>` - Execute the traffigen media script in ue-0, ue-1, ue-2 X time

## Architecture

![image](./docs/5GTestbed.png)

### Based on:
[Infinitydon's Open5GS Docker Compose for IoT](https://bitbucket.org/infinitydon/open5gs-5gcore-ueransim-iot-docker-compose/src/master/)