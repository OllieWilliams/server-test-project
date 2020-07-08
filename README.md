# server-test-project
quick server project to be used for programming test

How to run application:
1. Extract folder contents to a designated location.
2. Navigate to the extracted location on terminal.
3. Build the container: 

    _docker build ._

4. After container is built, run the container with external port connection:

    _docker run -p 8000:8000 *container_id*_
    
5. _Optional:_ Access: _*server_ip*:8000/_ confirming application is ready to receive HTTP requests
