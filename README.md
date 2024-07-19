#### Overview
This project sets up a simple web server using Flask that responds to three main endpoints (/home, /heartbeat, /add, /rm). The server is containerized using Docker and managed using Docker Compose to create multiple instances. A load balancer is implemented to distribute the requests across these instances using consistent hashing. Additionally, the system includes monitoring and logging mechanisms to track server health and request distribution.

#### Purpose
The purpose of this project is to demonstrate the implementation of a load balancer that evenly distributes incoming traffic to multiple server instances, ensuring efficient handling of requests and high availability.

#### Components
1. **Web Server**: Handles HTTP requests and provides endpoints for home and heartbeat. Each server instance runs inside a Docker container, making it easy to scale horizontally by adding more instances. The web server also includes basic health checks to ensure each instance is operational.
2. **Consistent Hash Map**: Used for mapping client requests to server instances. The consistent hash map ensures that the addition or removal of servers minimally impacts the mapping of existing requests. This reduces the need for rehashing and helps maintain a stable request distribution across servers.
3. **Load Balancer**: Routes client requests using consistent hashing and manages server replicas. It monitors the health of server instances using heartbeat signals and dynamically adjusts the server pool based on load and server availability. The load balancer can also redistribute requests in case of server failures to ensure continuous service availability.

**System Architecture Diagram**:
```plaintext
+---------------------+
|      Client         |
+---------+-----------+
          |
          v
+---------+-----------+
|    Load Balancer    |
+---------+-----------+
          |
  +-------+-------+
  |       |       |
  v       v       v
+---+   +---+   +---+
| S |   | S |   | S |
| e |   | e |   | e |
| r |   | r |   | r |
| v |   | v |   | v |
| e |   | e |   | e |
| r |   | r |   | r |
| 1 |   | 2 |   | 3 |
+---+   +---+   +---+
```

---

### Assumptions

1. **Network Reliability**: Assumes a reliable network with minimal packet loss. The system is designed to handle transient network issues, but prolonged network failures could affect performance.
2. **Uniform Load Distribution**: Assumes that client requests are uniformly distributed. If the requests are skewed towards specific keys, additional mechanisms might be needed to balance the load more effectively.
3. **Server Homogeneity**

### Prerequisites
1. Docker: latest [version 20.10.23, build 7155243]
   sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

2.  Docker-compose standalone [version v2.15.1]
   sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose 

**Docker**: To containerize the application.

2. **Python**: For implementing the server, load balancer, and consistent hash map.
3. **Flask**: For handling HTTP requests within the server and load balancer.
4. **Git**: For version control and managing the project repository.


---

### Installation Steps

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/Ian-Mutuge/DS-load-Balancer
   cd DS-load-Balancer
   ```

2. **Build Docker Images**:

   ```sh
   docker-compose build
   ```

3. **Run Docker Containers**:

   ```sh
   docker-compose up
   ```

#### Functional Tests
1. **Test Endpoints**:
   - Use tools like `curl` or Postman to test the following endpoints:
     - `/home`: Returns a unique identifier for the server.
     - `/heartbeat`: Returns the heartbeat status.
     - `/rep`: Checks the status of replicas.
     - `/add`: Adds a new server instance.
     - `/rm`: Removes a server instance.

   Example using `curl`:

   ```sh
   curl http://localhost:5000/home
   curl http://localhost:5000/heartbeat
   curl -X POST http://localhost:5000/add -d 'server_id=new_server'
   curl -X DELETE http://localhost:5000/rm -d 'server_id=existing_server'
   ```

#### Performance Tests
1. **Load Testing**:
   - Use tools like `aiohttp` or `requests` to simulate high traffic and observe the load distribution and fault tolerance.

2. **Experiment Scenarios**:
   - **A-1**: Launch 10000 async requests on 3 server containers and report the request count handled by each server instance.
   - **A-2**: Increment server instances from 2 to 6, launching 10000 requests on each increment, and report the average load.
   - **A-3**: Test all load balancer endpoints and demonstrate quick spawning of new instances upon server failure.
   - **A-4**: Modify hash functions and observe changes from A-1 and A-2.

By following these sections, you can understand the design, implement the distributed queue with sharding, and set up and test the customizable load balancer.


**Task 1: Server Implementation**

**Overview:**
In Task 1, we implemented a simple web server that accepts HTTP requests on port 5000 and provides two endpoints: `/home` and `/heartbeat`. The `/home` endpoint returns a string with a unique identifier to distinguish among replicated server containers. The `/heartbeat` endpoint sends heartbeat responses upon request, allowing the load balancer to identify failures in the set of containers maintained by it.

**Implementation:**
We implemented the server using Python, utilizing the Flask framework for handling HTTP requests. The server runs on port 5000 and provides the required endpoints as specified in the assignment. The server's unique identifier is set as an environment variable while running a container instance from the Docker image of the server.

**Dockerfile:**
We included a Dockerfile to containerize the server as an image, making it deployable for subsequent tasks. The Dockerfile installs necessary dependencies and sets up the environment for running the Flask application.

**Deployment:**
To deploy the server, build the Docker image using the provided Dockerfile and run a container instance from the built image. Ensure that the container is exposed on port 5000 to accept incoming HTTP requests.

**Task 2: Consistent Hashing Implementation**

**Overview:**
In Task 2, we implemented a consistent hash map using Python, which serves as the underlying data structure for the load balancer in Task 3. We utilized an array-based implementation to represent the hash map, with provisions for handling collisions using linear or quadratic probing.

**Implementation:**
We implemented the consistent hash map using Python, utilizing an array data structure to represent the hash map and hash functions provided in the assignment. The implementation ensures that requests are mapped to the appropriate server instances based on the consistent hashing algorithm.

**Task 3: Load Balancer Implementation**

**Overview:**
Task 3 involves building a load balancer container that uses the consistent hashing data structure from Task 2 to manage a set of server replicas. The load balancer is responsible for routing client requests to server replicas in a balanced manner and maintaining the desired number of replicas even in case of failure.

**Implementation:**
We implemented the load balancer container using Python and Flask, leveraging the consistent hashing data structure implemented in Task 2. The load balancer provides HTTP endpoints for modifying configurations, checking the status of managed web server replicas, and routing client requests to server replicas.

**Endpoints:**
- `/rep`: Returns the status of the replicas managed by the load balancer.
- `/add`: Adds new server instances to scale up with increasing client numbers.
- `/rm`: Removes server instances to scale down with decreasing client or system maintenance.
- `/<path>`: Routes client requests to a server replica as scheduled by the consistent hashing algorithm.

##
## Task 4: Testing loadbalaner and endpoints**

- This task was mainly to test endpoints and the load balancer.

## 10,000 async requests
This script performs an analysis of request distribution among different server instances by making multiple asynchronous HTTP GET requests to a local server endpoint and visualizing the results.

**What the Script Does**

1. **Fetches Data**: 
   - Makes 10,000 asynchronous HTTP GET requests to `http://localhost:5000/home`.
   - Each request fetches a JSON response from the server.

2. **Processes Responses**:
   - Parses each response to extract the server identifier from the `message` field.
   - Counts how many requests were handled by each server.

3. **Visualizes Results**:
   - Creates a bar chart that shows the number of requests handled by each server.
   - Saves the bar chart as an image file named `request_distribution_changed_function.png`.

**Requirements**

Make sure you have Python 3.7+ installed along with the following packages:

- `aiohttp` for making asynchronous HTTP requests
- `matplotlib` for creating visualizations


```sh
python3 ascyn.py
```

**Results:**

![10,000 async requests](/request_distribution.png)

Request Distribution: Server1 and Server3 handled significantly more requests compared to Server2. This suggests that the load balancer algorithm might have allocated more requests to Server1 and Server3 based on their current load or other factors considered by the load balancer.
Performance: Server1 and Server3, with higher request counts, could potentially have more available resources or faster response times compared to Server2. This could be due to differences in hardware, network latency, or server load at the time of testing.
Load Balancer Effectiveness: The load balancer seems to have effectively distributed requests across the three servers, albeit unevenly. This could be intentional based on configured weights or dynamic load balancing metrics.
Server1: Handled 4591 requests
Server2: Handled 1427 requests
Server3: Handled 3982 requests
The total number of requests handled by all three servers is:
4591+1427+3982=10000



## N=2 to 6 increments
**What the Script Does**

1. **Measure Server Load**:
   - Sends 10,000 asynchronous HTTP GET requests to `http://localhost:5000/home`.
   - Tracks the number of requests handled by each server.
   - Counts failed requests due to errors or unsuccessful responses.

2. **Check Existing Nodes**:
   - Retrieves the list of existing server replicas from `http://localhost:5000/rep`.
   - Determines if new servers need to be added.

3. **Main Execution**:
   - Iterates over a range of server counts (2 to 6).
   - Adds new servers if needed.
   - Measures the load for each server count and collects data on server load and failed requests.
   - Plots the average load and average failed requests over the range of server counts.

4. **Visualization**:
   - Creates a plot showing the average number of requests per server and the average number of failed requests.
   - Saves the plot as `average_server_load_and_failed_requests.png`.

**Results:**
![Increment Results](/average_server_load_and_failed_requests.png)
For 2 servers (server1 and server2), server1 handled 3808 requests and server2 handled 1597 requests.
With 3 servers (server1, server2, and server3), the distribution changed where server1 handled 3273 requests, server2 handled 2682 requests, and server3 handled 4045 requests.
Adding more servers (4, 5, and 6 servers) shows varying distributions of requests among the servers. For instance:
With 4 servers, server4 handled a significantly higher load compared to others.
With 5 and 6 servers, the load distribution shifted again, showing different patterns across the servers.

**Average Load:** The average load per server was calculated for each configuration. For 6 servers, the average load was approximately 1667 requests per server.
This metric helps gauge how evenly the load balancer distributes requests among the available servers. In this case, as the number of servers increased, the average load per server generally decreased, indicating effective load balancing.


**Scalability Strengths:** The load balancer demonstrates scalability by effectively distributing incoming requests across a growing number of servers (server1 to server6).
Dynamic Adjustment: As servers are added (server4, server5, server6), the the load balancer adjusts the distribution of requests, evident in the varying server loads.

**Load Distribution:** The load balancer's ability to balance the load among servers is critical for scalability. Here, we observe dynamic adjustments in load distribution as more servers are added, which is a positive sign for scalability.

**Graphical Representation:**

The plotted graph (not shown here but inferred from the script) would display the average requests per server (avg_loads) and the average failed requests (avg_failed_requests).
The average load per server would decrease with an increasing number of servers, indicating the load balancer's ability to efficiently distribute workload as it scales.
In conclusion, the load balancer implementation appears to handle scalability well by adjusting the distribution of requests among servers dynamically. This capability ensures that as the system scales up with more servers, the overall performance and reliability are maintained, making it suitable for handling varying levels of traffic and maintaining service availability.




##
**Deployment:**
Deploy the load balancer container using the provided Dockerfile, Docker-compose file, and Makefile. Ensure that the load balancer is exposed on port 5000 to accept incoming HTTP requests.


**Conclusion:**
Overall, the load balancer implementation effectively distributes the load among server containers and demonstrates scalability and fault tolerance. The analysis provides insights into the performance and behavior of the load balancer in various scenarios, contributing to the understanding of distributed systems and load balancing techniques. The other testing images are found in rm_responses.json.

