# malware-screen
This is simple tool and prop built for use in cyber security tabletop exercises. The tool has too purposes
 
1. It acts as a simple looking tool enabling participants in the extercise to log decisions they make as the game unfolds
2.  Give the participants the expereince of having a computer ransomed, by displaying a ransomeware demand full screen at a predetermined time during proceedings 


## How it works
Participants can log decisions via the interface. This writes data to timestamped json files, which can be refgerenced after the game to chart theparticipants deciion making processes. At a predefined time the interface will stop working and the computer will instead show a ransomware screen with a deeman for paymenty and a coutndown timer. 

### Setting up the Ransomware Screen

#### Set the time at which the Ransomware Screen will appear
1. Go to the `interface` folder and open `rootview.py`. Find the class `InputScreenTimer` and set the variable `self.termination_time` to the time you would like the input view to disappear and the malware screen to appear. 

#### Set the duration for the ransomeware timer
2. Go to the `interface` folder and open `malwarescreen.py` in your code editor. 
2. find the class named `MalwareTimer`
3. Within the `MalwareTimer` class set `self.termination_time` and set this to the time you would like the countdown clock to run out of time. 

