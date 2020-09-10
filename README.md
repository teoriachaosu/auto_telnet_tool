Auto Telnet Tool for Windows. 
A script to automate ASUS router configuration via telnet.
Compatibility: Windows 10, 7 (x64 only), ASUS routers.

router_login.txt
================
Replace the defaults with your router's values.
Default router prompts come from ASUS RT-N66U router. 
Do not change the order of data, remove '///' or leave empty line.
Adjust read timeout to your router's response time if necessary.

router_setup.txt
================
Enter commands for the router to execute.
Lines starting with '///' are ignored and file reading continues.
An empty line stops file reading and can be used to quickly disable the entire block of commands.
Run the auto_telnet_tool.exe to apply your settings.

The router output and operations performed are logged to session_log.txt 
If there's no log file in the app directory, it will be created on the first run.
The log file present is a result of running the exe file with the default contents. 

The app was developed and tested on ASUS routers RT-N66U, RT-AC52U_B1.
There's no guarantee it will work with routers of other vendors.

Copyright (c) 2020 Maciej Białowąs, MIT License 
