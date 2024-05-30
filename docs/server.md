## Working with a Linux server port

.Identify the Process Using the Port

Open a terminal and run the following command to find the process ID (PID) using port 5000:

```bash
lsof -i :5000
```

Once you have the PID, you can stop the process by running:

```shell
kill -9 <PID>
Replace <PID> with the actual process ID you found in the previous step.
```