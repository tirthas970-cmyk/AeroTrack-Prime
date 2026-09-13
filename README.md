<h1 align="center">AeroTrack-Prime</h1>
<p align="center">Desktop Command Dashboard About Asteroids</p>
<div align="center">
  <a href="https://github.com/tirthas970-cmyk">tirthas970-cmyk</a>
</div>

#### What does it do?
* **NASA Feed Table**: A clean, updating table that shows real names, speeds, and sizes of every asteroid passing Earth today, pulled live from Nasa's actual satellites
* **Threat Assessment Panel**: Shows asteroids with the highest potential energy
* **AI Profile Analysis**: Classifies selected asteroid into a specific group based on historical data using Machine Learning
* **Automated Report Generator**: A text file that details all information of the selected asteroid
* **Trajectory Modifier**: Slide bars where you can manually change an asteroid's variables, and see if your mock asteroid hits or misses Earth!

## How to Run?
* Click on this link: https://aerotrack-prime-4hx2awdqlc4qm8pawawcya.streamlit.app/
   * This is the public version!

## Installation & Local Setup

If you want to run the dashboard locally on your machine instead of using the Streamlit Cloud link, follow these steps:

### Prerequisites
- **Python**: 3.13.2
- **NASA API Key**: Get a free key instantly at [api.nasa.gov](https://nasa.gov)

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd AeroTrack-Prime
   ```

2. **Create and activate a virtual environment (Recommended):**
   ```bash
   # Create environment
   python -m venv venv
   
   # Activate on Windows:
   .\venv\Scripts\activate
   
   # Activate on macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your NASA API Secrets:**
   * Create a folder named `.streamlit` in your project's root directory.
   * Inside that folder, create a file named `secrets.toml`.
   * Add your API key to the file exactly like this:
     ```toml
     nasa_key = "YOUR_ACTUAL_API_KEY_HERE"
     ```
   *(Note: The `.streamlit/secrets.toml` file is automatically ignored by git to keep your key secure!)*

5. **Launch the application:**
   ```bash
   streamlit run app.py
   ```



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
> Note: This project is considered complete in regards to functionality. However, soon, I will make my code more readable professional. Feel free to fork this repository and further develop it using these ideas:
* Create a feature that shows historical asteroids
* Update **Trajectory Modifier** to incorporate Earth's magnetic field on whether or not an asteroid will burn up when entering the atmosphere
* Create a interactive 3D orbit viewer


## Final Comments:
> Note that **Google Gemini** was used for GUI debugging and helping out with the physics. Other than that, I wrote almost all the code for this program. **ChatGPT** was also used for initial concept images of this dashboard.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Pictures:

<img width="1902" height="720" alt="Screenshot 2026-09-12 130631" src="https://github.com/user-attachments/assets/6d3cd4c7-0355-4807-9290-df06f3ba550c" /><img width="1875" height="847" alt="Screenshot 2026-09-12 130735" src="https://github.com/user-attachments/assets/178edcb6-e0af-4bae-919c-97c42bd51eb5" />
<img width="988" height="767" alt="image" src="https://github.com/user-attachments/assets/8419d46a-d8c9-488e-8799-12e520cf710c" />
<img width="1851" height="697" alt="image" src="https://github.com/user-attachments/assets/6210b3f3-b2cd-43b9-afbd-85b972c2b662" />
<img width="685" height="752" alt="image" src="https://github.com/user-attachments/assets/7c50d737-4dd4-41aa-abec-0b9f89689318" />





