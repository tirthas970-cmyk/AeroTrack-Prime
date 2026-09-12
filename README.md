# AeroTrack-Prime
Desktop Command Dashboard About Asteroids

### What does it do?
* **NASA Feed Table**: A clean, updating table that shows real names, speeds, and sizes of every asteroid passing Earth today, pulled live from Nasa's actual satellites
* **Threat Assessment Panel**: Shows asteroids with the highest potential energy
* **AI Profile Analysis**: Classifies selected asteroid into a specific group based on historical data using Machine Learning
* **Automated Report Generator**: A text file that details all information of the selected asteroid
* **Trajectory Modifier**: Slide bars where you can manually change an asteroid's variables, and see if your mock asteroid hits or misses Earth!

## How to Run?
* Click on this link: https://aerotrack-prime-4hx2awdqlc4qm8pawawcya.streamlit.app/ 

## Key Files Explanations:
* The files that my program depends on are:
  * **app.py**: The file that creates the streamlit GUI, and uses the other files
  * **AsteroidData.py**: This file fetches NEO data using NASA API, finds the cluster group of a new asteroid and characterizes them, gets the highest potential energy asteroid, and creates the .txt file
  * **TrajectoryEngine.py**: This file calculates whether or not a mock asteroid will hit earth, calculates the highest potential energy (which is used in AsteroidData.py, and animates the mock asteroid into a gif
  * **Markdown.py**: The overall aesthetics of my program
    * Not in app.py because it made the file too long
  * **Plot.py**: Plots the new asteroid datapoint into the existing cluster groups
* **NeoClassifierV2.ipynb**: This is the notebook that contains my unsupervised KMeans Model
* **.joblib** files: These files were saved as .joblib files from the notebook; used in AsteroidData.py to find the cluster of a new asteroid
* **requirements.txt**: The requirements to create this app in Streamlit

## Technologies Used:
* Python: 3.13.2
* Vs Code
* Google Colab
  
## Why I built this?
* Interested in astronomy and computer science
  * This project combines those to interests into a real usable application
* Enables me to incorporate other interests like ML and physics into the program
* Helps me learn both backend and frontend skills
* Allows one to find all data about asteroids, specifically Near-Earth-Asteroids (NEOs)

## Developmental Timeline:
* Around 2 Months (Late June 2026 - Early September)
* On and Off between other projects
  * Most of the work was done early to mid July, and late to early September

## Key Milestones:
* Month 1: Getting the GUI setup, NASA feed table, threat panel, and trajectory modifier
* Month 2: Doing Unsupervised machine learning for AI Profile Analysis, polishing the GUI, creating a GIF of mock asteroids, publishing to Streamlit Cloud

## Future Roadmap:
>> Note: This project is considered complete in regards to functionality. However, soon, I will make my code more readable professional. Feel free to fork this repository and further develop it using these ideas:
* Create a feature that shows historical asteroids
* Update **Trajectory Modifier** to incorporate Earth's magnetic field on whether or not an asteroid will burn up when entering the atmosphere
* Create a interactive 3D orbit viewer


>> Note that **Google Gemini** was used for GUI debugging and helping out with the physics. Other than that, I wrote almost all the code for this program. **ChatGPT** was also used for initial concept images of this dashboard.





