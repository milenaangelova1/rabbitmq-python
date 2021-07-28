```
Given the message structure:
{ 
   "task": "task_{n}",
   "param": {b}
}
, where {n} could be 1 or 2 and {b} is a boolean parameter.
Using a dockerized message broker service (eg. RabbitMQ - https://hub.docker.com/_/rabbitmq)
- Create 2 queues: 'messages' and 'failed'
Create a dockerized worker broker service to poll for messages with that structure (within the 'messages' queue) and the worker/s would call one of the methods, depending on the message value:
	when "task" has a value of "task_1":
	bool function worker_1(param) {
		if param == true {
			print "Task 1 executed successfully.";
		}  else {
			print "Task 1 execution failed.";
		}
		return param;
	}
	when "task" has a value of "task_2"
	bool function worker_2() {
		print "Task 2 executed.";
		return true;
	}
- Your broker should call one of the methods depending on the message.
- After a successful execution (return true) the message should be removed (acknowledged).
- After a failed execution (return false) the message should be sent to another queue ('failed').
- Unit tests are not required, but will be appreciated.
```