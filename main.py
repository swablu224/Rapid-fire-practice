"""
Tiny program to practice frame perfect rapid fire hops for Mario Kart Wii as shown in Braixens recent Moo Moo Meadows WR
No AI was used in the making of this program.
"""

import Gamepad.Gamepad as gp
import time
import sys
from colorama import Fore

TRIGGERTRHESHOLD = (2*150/255) - 1 #58% pressed down leads to a hop (thanks campbell!), this is mapped onto the -1 -> 1 range that is recorded
INTERVAL = 1/60 #60 fps

#define the needed buttons on the gcn controller
#if you want to define your own keymappings for another controller, you can use the Gamepad.py script, and check which buttons/axes change when you give input
class GCN(gp.Gamepad):
    def __init__(self, joystickNumber = 0):
        gp.Gamepad.__init__(self, joystickNumber)
        self.axisNames = {
            5: 'R-TRIGGER'
        }
        self.buttonNames = {
            0:  'A',
            1:  'B',
            2:  'X',
            3:  'Y',
            5:  'Z',
            7:  'START',
        }
        self._setupReverseMaps()


# Gamepad settings
gamepadType = GCN
gamepad = gamepadType()

# Wait for a connection
if not gp.available():
    print('Please connect your GCN controller...')
    while not Gamepad.available():
        time.sleep(1.0)
print('Controller connected!')


N = int(input("How many rapid fire inputs do you want to practice? "))
input_pattern = ([True, False] * (N - 1)) + [True]

print("\nExit by pressing the X button, ██ is for a button press, ░░ for a release, holding drift at the end is allowed.")
print("A " + Fore.GREEN + "green " + Fore.RESET + "square is correct, a " + Fore.RED + "red" + Fore.RESET + " square is incorrect!")
print("\n- Desired inputs:")
print("> ", end='')

#print the guide for how many buttons to press
for i in range(N - 1):
    print(Fore.BLUE + "██", end = '')
    print(Fore.WHITE + " - ", end = '')
    print(Fore.LIGHTBLACK_EX + "░░", end = '')
    print(Fore.WHITE + " - ", end = '')

print(Fore.BLUE + "██", end='')

#edge case handling for N = 1, it will ask you to do a single frame hop input as a result of below code
if N == 1:
    print(Fore.WHITE + " - ", end = '')
    print(Fore.LIGHTBLACK_EX + "░░", end='')
    input_pattern.append(False)
sys.stdout.flush()

#start polling the controlller
gamepad.startBackgroundUpdates()

#on gcn you can hop with either the Trigger or the B button
def get_inputs():
    input_string = ''
    if gamepad.isPressed('B'): 
        input_string += 'B'

    if (gamepad.axis('R-TRIGGER') >= TRIGGERTRHESHOLD):
        input_string += 'R'

    #dumb way to return the proper case (this space is needed later to not mess up the spacing)
    if input_string == '':
        input_string = ' '

    return input_string

try:
    while gamepad.isConnected():
        if gamepad.beenPressed('X'):
            break

        print(Fore.RESET + "\n> ", end='')
        sys.stdout.flush()

        #start playing on first hop
        while get_inputs() == ' ':
            playing = False
        playing = True

        start = time.time()
        loops = 0
        input_sequence = [] #the input sequence that will be recorded
        hop_sequence = [] #the resulting hop sequence
        success = True #if not set to false later

        while playing:
            current_inputs = get_inputs()
            input_sequence.append(current_inputs)
            if (('R' in current_inputs) or ('B' in current_inputs)):
                hop_sequence.append(True)
                char = "██"
            else: 
                hop_sequence.append(False)
                char = "░░"

            if loops < len(input_pattern):   
                if hop_sequence[loops] == input_pattern[loops]:
                    output_color = Fore.GREEN
                else:
                    output_color = Fore.RED
                    success = False
            else:
                output_color = Fore.WHITE
                
            print(output_color + char, end=' ')
            print(Fore.WHITE + "-", end=' ')
            sys.stdout.flush()

            time.sleep(INTERVAL)
            loops += 1
            #allow a couple extra inputs to be recorded at the end to make it clear that you are allowed to hold drift on end
            if (time.time() - start) >= 3 * N * INTERVAL:
                playing = False

        if success:
            print(Fore.CYAN + "You did it!!!")
        else:
            print(Fore.LIGHTRED_EX + "Better luck next time!")
        
        print('  ', end='')
        for i in input_sequence:
            print(Fore.BLUE + i, end=' -  ')
        sys.stdout.flush()
        
        time.sleep(0.5)
finally:
    # Ensure the background thread is always terminated when we are done
    gamepad.disconnect()
