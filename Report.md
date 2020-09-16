## 2020 Sensor Miniproject Jaden Cho & Maxine Loebs - EC 463 - September 17, 2020

### Task 0 - Set up Python Websockets
After running the code, we see that the greeting string issued is **ECE Senior Capstone IoT Simulator** 

### Task 1 - Data Flow
Below is our code added to client.py, which saves the incoming JSON data to a text file. You pass the name of the file you want to write to into the command line. For example, *python -m sp_iotsim.client mydata.txt* would save the incoming data into a text file called mydata.

    print_stdout = sys.stdout               #Redirects printed JSON data

    with open(log_file, "a") as f:          #Opens/creates file do append JSON string
        sys.stdout = f 
        print(data)                         #Prints JSON data to file
        sys.stdout = print_stdout           #Reverts output back to terminal

### Task 2  - Analysis
We chose to look at the data from the office. 
1. The median of the temperature data is () and the variance is ().  
2. The median of the occupancy data is () and the variance is ().  
3. Here are the histogram plots for each sensor type:  
![office temperature](/2020-sensor-miniproject Pics/officetemp.png)
4. The mean of of the time intervals is () and the variance is (). Here is the probability density as a histogram:  

(Answer question here)

### Task 3  - Design
1.  Our algorithm, (temp.py in the src/sp_iotsim folder) analyzes the temperature data for the office. It removes "outlier" points from the data (anything outside of one standard deviation from the mean), and then calculates the median and variance of the new temperature data. It also calculated the percentage of "bad" data points. 

2.  A persistent change in temperature doesn't always indicate a failed sensor, but more often than not, we believe it would. For example, if the room temperature is consistently coming back to be 70C, perhaps the room is on fire. But if it persists for a while, the most probable answer would be that the sensor had failed. In some instances, we got back readings of -80C. Unless the office somehow moved to Antarctica, this would be pretty impossible. So in this case, it seems to be surely a failed sensor.
3.  Our temperature values were more or less centered around 23C, so perhaps 20-25C would be good bounds. Anything outside of the range isn't a comfortable room temperature.

### Task 4 - Conclusions
1.  The data that we are receiveing pertaining to temperature, Co2 levels, and occupancy would all be important in the real world. For example, if you saw sensor readings returning values that are too high or low, you may have a problem with the heating/AC system in that room. CO2 readings have becoming increasingly important in the context of COVID-19, where air quality may dictate the chance of transmission. You could also put occupancy in the context of COVID-19 -- it would be important to know if capacity guidelines are being violated. During more normal times, it is also important not to exceed the occupancy of a room in case of emergency.  
2.  If we view this project as a sort of pseudo-HVAC system, then it would lack sensors for things like pressure and humidity. The temperature sensors in real HVAC systems not only record the ambient temperature in the room, but also the gases and/or liquids used to keep the room at temperature. Pressure sensors work alongside temperature sensors to provide efficiency. Humidity sensors also help to control humidity which largely contributes to air quality and how comfortable the room is.  
3.  
4.  

