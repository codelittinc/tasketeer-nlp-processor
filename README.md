# Steps to run the project using docker

### Set the environment variables
```bash
cp .env.example .env
```

set the production values of these env variables in `production`:
```
FLASK_DEBUG=0
ENV=production
AUTHORIZATION=
OPENAI_API_KEY=
MONGODB_HOST=
```

### start the `bin/dev` script for development mode
```bash
sh bin/dev
```

### Install python libraries and dependencies
```bash
pip install -r requirements.txt
```

### Run server ```(this process is not automated - needs to be executed manually in the docker container or server!)```
```bash
python3 app.py
```

### Health endpoint
- Checker to verify if the server is running as expected
```bash
curl --location 'http://localhost:8080/health'
```

response:
```json
{
    "datetime": "Fri, 10 Mar 2023 17:37:36 GMT",
    "success": "true"
}
```


### Index content 
- Store file contents to be used by an organization to search by context
- This endpoint expects to receive the `Authorization` header in production environment `(ENV=production)`
```bash
curl --location 'http://localhost:8080/contents' \
--header 'Content-Type: application/json' \
--data '{
    "organization": "codelitt",
    "content": "Travel Expense Report Process on Codelitt: You need to make sure to include: 1) the business purpose of the trip, 2) dates traveled, and 3) the client’s information and details (if applicable). You need to make sure to include all receipts or documents related to the expense for our review. Business trip expense reports need to be submitted to Cody, cc Mary no more than a week after traveling. When submitting your report and receipts, please make sure they are in PDF format and email them in a .Zip file."
}'
```

response:
```json
{
    "Document_ID": "640a0bb44789ef2014f53513",
    "Status": "Successfully Inserted"
}
```

### Search indexed content
- Search by context (based on **files** already uploaded or the open_ai global knowledge database)
- This endpoint expects to receive the `Authorization` header in production environment `(ENV=production)`
```bash
curl --location 'http://localhost:8080/search?organization=codelitt&q=explain%20the%20Travel%20Expense%20Report%20Process%20on%20Codelitt'
```

response:
```json
{
    "response": {
        "extra_info": null,
        "response": "\nThe Travel Expense Report Process on Codelitt requires that the employee submit a report with the business purpose of the trip, dates traveled, and client information (if applicable). All receipts and documents related to the expense must be included and submitted to Cody, cc Mary, no more than a week after traveling. The report and receipts must be in PDF format and emailed in a .Zip file.",
        "source_nodes": [
            {
                "doc_id": "c76a1959-f620-406d-bfe1-258e2ac3481f",
                "extra_info": null,
                "node_info": null,
                "similarity": null,
                "source_text": "Travel Expense Report Process on Codelitt: You need to make sure to include: 1) the business purpose of the trip, 2) dates traveled, and 3) the client’s information and details (if applicable). You need to make sure to include all receipts or documents related to the expense for our review. Business trip expense reports need to be submitted to Cody, cc Mary no more than a week after traveling. When submitting your report and receipts, please make sure they are in PDF format and email them in a .Zip file."
            },
            {
                "doc_id": null,
                "extra_info": null,
                "node_info": null,
                "similarity": null,
                "source_text": "Codelitt has a travel expense report process that requires the business purpose of the trip, dates traveled, and client information (if applicable) to be included. All receipts and documents related to the expense must be included and submitted to Cody, cc Mary, no more than a week after traveling. The report and receipts must be in PDF format and emailed in a .Zip file."
            }
        ]
    }
}
```