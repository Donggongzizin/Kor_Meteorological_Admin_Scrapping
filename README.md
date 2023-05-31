## **Earthquake detection method**

We can utilize real-time earthquake information services provided by meteorological agencies. These websites offer information about the magnitude, location, and maximum intensity of earthquakes that occur. In this case, we are scraping data from the website using a Raspberry Pi and uploading it to the Mobius platform.

The website also provides simulated videos of past earthquake cases. For the simulation, we used data from an earthquake that occurred in Seogwipo, Jeju on December 14, 2021.

If an earthquake occurs in a region other than the last observed earthquake occurrence area, data is uploaded to the Mobius platform.

**Target Resource:** /Mobius/KETIDGZ_earthquake

con: web_scrapping

cin (format): **`scale + "|" + origin + "|" + magnitude`**