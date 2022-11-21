# Ransomware Simulator
This is simple prop built for use in cyber security tabletop exercises. The tool has two purposes
 
1. It acts as a simple logging tool, enabling participants in the extercise to log decisions they make as the tabletop event unfolds
2. Simulates the expereince of having a computer ransomed, by displaying a fullscreen ransomeware demand with countdown timer and shutting off keyboard escapes at a predetermined time during proceedings 


## How it works
During a tabletop exercise the person runing it presents participants with vairous stimuli. As participants navigate the material they make decisons which can be logged via the ransomeware simulator tool. For example, someone may receive a suspicious email and decide that they should inform a member of the Security team. This deciiosn can be logged via the interface. Loggin the decion writes timestamped data to .json files. These files can then be reviewed after the simulation exercise so as to better understand the participants deciion making processes. At a predefined time during the simulation the interface will suddenlt be replaced with a ransomware demand screen with a coutndown timer. This enables the person running the scenario to shift the focus to a ransomware attack.   

### Setting up the Ransomware Screen

#### Set the time at which the Ransomware Screen will appear
1. Go to the `interface` folder and open `rootview.py`. Find the class `InputScreenTimer` and set the variable `self.termination_time` to the time you would like the input view to disappear and the malware screen to appear. 

#### Set the duration for the ransomeware timer
2. Go to the `interface` folder and open `malwarescreen.py` in your code editor. 
2. find the class named `MalwareTimer`
3. Within the `MalwareTimer` class set `self.termination_time` and set this to the time you would like the countdown clock to run out of time. 


## Features under development
I am currently working on adding the ability to write the data to a cloud based database. This means that the software can run on multiple computers simultaneously with decions being logged to a central point.
