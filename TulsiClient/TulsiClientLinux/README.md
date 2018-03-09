# TULSI CLIENT

## Installation Procedure


## Prerequisites 
python 2.7
```
https://www.python.org/download/releases/2.7.6/
```

Numpy 
```
http://sourceforge.net/projects/numpy/files/NumPy/
```

Scipy

```
http://www.scipy.org/install.html
```



Download and unzip the TulsiClient Mac package


Edit the /etc/tulsi/tulsi.conf file


```
[tulsi]
host = <<Ip of the host>>
port = 5005
[tulsistatsd]
host = << IP of the host>>
port = 8125
log_duration = 10

```
Now run the following command to make it executable

```
# chmod a+x TulsiClient.sh

```

Run the Tulsi engine with the below command

```
# sh TulsiClient.sh

```




Note : The Tulsi Server has to be up and running before the client. 
       The logstatd parameters has to be enabled with host IP  in swift cluster  to get statsd logs. 
		

