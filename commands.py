import time
import keyboard
import fivem as f
import random as rand
from termcolor import colored
import basic_func as base
import inspect

magicball = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
movements = [
    "me shakes their leg.",
    "me bounces their foot.",
    "me taps their fingers.",
    "me adjusts their glasses.",
    "me scratches their head.",
    "me stretches their arms.",
    "me rolls their shoulders.",
    "me takes a deep breath.",
    "me chews on their lip.",
    "me taps their chin thoughtfully.",
    "me cracks their knuckles.",
    "me fidgets nervously.",
    "me hums a tune.",
    "me whistles softly.",
    "me scratches their beard.",
    "me sighs heavily.",
    "me leans back and stretches.",
    "me rubs their eyes.",
    "me snaps their fingers.",
    "me taps their knee.",
    "me checks their watch.",
    "me taps their foot impatiently.",
    "me flexes their fingers.",
    "me shakes their head.",
    "me twirls a strand of hair.",
    "me scratches the back of their neck.",
    "me rubs their forehead.",
    "me kicks the air gently.",
    "me stretches their legs.",
    "me stomps their foot lightly.",
    "me adjusts their clothing.",
    "me rubs their hands together.",
    "me scratches their ear.",
    "me scratches their back.",
    "me claps their hands lightly.",
    "me rolls their neck slowly.",
    "me shifts their weight from foot to foot.",
    "me stretches their back.",
    "me twirls a coin between fingers.",
    "me stamps their foot in rhythm.",
    "me bends forward slightly.",
    "me leans side to side.",
    "me yawns and stretches arms.",
    "me shakes off dust from clothing.",
    "me lifts one leg and balances.",
    "me jumps lightly in place."
]
divider = colored("--------------------------------------------------------\n", 'cyan', attrs=['bold'])


cm =f.ConnectionManager()

key_start_time = None


def timer(e):
    global key_start_time

    print(colored(f"Key: '{e.name}' Detected! Running: '{inspect.currentframe().f_code.co_name}'",'yellow'))

    if key_start_time is not None:
        elapsed_time = time.time() - key_start_time
        cm.send_message(f"me stops stopwatch and reads {elapsed_time:.2f} seconds.")
        key_start_time = None
    else:
        key_start_time = time.time()
        cm.send_message("me Starts Stopwatch.")
    print(divider)

def diceRoll(e):
    print(colored(f"Key: '{e.name}' Detected! Running: '{inspect.currentframe().f_code.co_name}'",'yellow'))

    roll = rand.randint(1, 20)
    if roll == 20:
        cm.send_message(f"me rolls a d20... natural 20! Critical Success!")
    elif roll == 1:
        cm.send_message(f"me rolls a d20... natural 1! Critical Failure!")
    else:
        cm.send_message(f"me rolls a d20... {roll}.")
    print(divider)

def magic8ball(e):
    print(colored(f"Key: '{e.name}' Detected! Running: '{inspect.currentframe().f_code.co_name}'",'yellow'))
    response = rand.choice(magicball)
    cm.send_message(f"me shakes the magic 8-ball... '{response}'")
    print(divider)

def coinflip(e):
    print(colored(f"Key: '{e.name}' Detected! Running: '{inspect.currentframe().f_code.co_name}'",'yellow'))
    cm.send_message(f"me flips a coin... {rand.choice(['Heads', 'Tails'])}.")
    print(divider)

def bodyFidget(e):
    print(colored(f"Key '{e.name}' Detected! Running: '{inspect.currentframe().f_code.co_name}'",'yellow'))
    cm.send_message(f"{rand.choice(movements)}")
    print(divider)







keyboard.on_release_key('f16', timer)
keyboard.on_release_key('f17', bodyFidget)
keyboard.on_release_key('f13', diceRoll)
keyboard.on_release_key('f14', coinflip)
keyboard.on_release_key('f15', magic8ball)


print(colored(base.box_text("Script Loaded."), 'green'))
print(divider)



keyboard.wait()

