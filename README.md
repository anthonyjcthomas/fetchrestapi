Fetch Rewards Points Tracking API
=================================

**Project Overview** This is a REST API for tracking user points across Fetch Rewards, allowing users to add points, spend points, and check their current point balance.

**Setup**

1.  Ensure you have Python 3.10+ and pip installed.
2.  Run `https://github.com/anthonyjcthomas/fetchrestapi`
3.  Run `cd fetchrestapi`
2.  Run `python3 -m venv venv`
3.  Run `source venv/bin/activate`
4.  Run `pip install -r requirements.txt`
5.  Run `python app.py` to start the server on port 8000.

**Endpoints**

-   POST /add
    -   Body: `{"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"}`
-   POST /spend
    -   Body: `{"points": 5000}`
-   GET /balance

**Testing**

1.  POST /add with the given example transactions:

-   DANNON 300 points `curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"}'`
-   UNILEVER 200 points `curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z"}'`
-   DANNON -200 points `curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z"}'`
-   MILLER COORS 10000 points `curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z"}'`
-   DANNON 1000 points `curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z"}'`

1.  POST /spend with 5000 points:

-   Spend 5000 points `curl -X POST http://localhost:8000/spend -H "Content-Type: application/json" -d '{"points": 5000}'`

1.  GET /balance and verify the response:

-   Get current balance `curl http://localhost:8000/balance`
-   Should be; 
        {
        "DANNON": 1000, ”UNILEVER” : 0, "MILLER COORS": 5300
        }   
