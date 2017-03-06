import mp7

##############################################################################
# Standard menu for running
# *IMPORTANT:* Reduce master latency by 2 BX (12 frames) for this menu!
# 2 bank ids                         
# 2 modes
# - mode 0 every 107th event
# - mode 1 all events
standardMenu = mp7.ReadoutMenu(4,2,4)

standardMenu.bank(1).wordsPerBx = 6
standardMenu.bank(2).wordsPerBx = 6

# First Mode
# Triggers every 107th event
mode = standardMenu.mode(0)

mode.eventSize = 0
mode.eventToTrigger = 107
mode.eventType = 0xd1
mode.tokenDelay = 70


# Even, bank id 1, +0bx
c = mode[0]
c.enable = True
c.id = 0x1
c.bankId = 0x1
c.length = 5
c.delay = 0 
c.readoutLength = 30

c = mode[1]
c.enable = True
c.id = 0x2
c.bankId = 0x2
c.length = 5
c.delay = 0
c.readoutLength = 30


# Second Mode
mode = standardMenu.mode(1)

mode.eventSize = 0
mode.eventToTrigger = 1
mode.eventType = 0xd0
mode.tokenDelay = 70


# Even, bank id 1, +/-1bx
c = mode[0]
c.enable = True
c.id = 0x1
c.bankId = 0x1
c.length = 3
c.delay = 1 #2 # 0+1 bx
c.readoutLength = 18

c = mode[1]
c.enable = True
c.id = 0x2
c.bankId = 0x2
c.length = 5
c.delay = 0
c.readoutLength = 30

##############################################################################
# Minimal menu for testing.
# 1 mode, 1 capture
# No delay
smallMenu = mp7.ReadoutMenu(4,2,4)

smallMenu.bank(1).wordsPerBx = 6

# Triggers on every event
mode = smallMenu.mode(0)

mode.eventSize = 0
mode.eventToTrigger = 1
mode.eventType = 0xc0
mode.tokenDelay = 70

# Even, bank id 1, +0bx
c = mode[0]
c.enable = True
c.id = 0x1
c.bankId = 0x1
c.length = 1
c.delay = 0
c.readoutLength = 6

##############################################################################
# To be used for timein tests. Apply only to few channels 
# *IMPORTANT*: Adjust master latency to move central event.
# 1 mode, 1 capture
# No delay
timeinMenu = mp7.ReadoutMenu(4,2,4)

timeinMenu.bank(1).wordsPerBx = 6

# Triggers on every event
mode = timeinMenu.mode(0)

mode.eventSize = 0
mode.eventToTrigger = 1
mode.eventType = 0xc0
mode.tokenDelay = 70

# Even, bank id 1, +0bx
c = mode[0]
c.enable = True
c.id = 0x1
c.bankId = 0x1
c.length = 15
c.delay = 0
c.readoutLength = 90 

# Even, bank id 2, +0bx
c = mode[1]
c.enable = True
c.id = 0x2
c.bankId = 0x2
c.length = 15
c.delay = 0
c.readoutLength = 90 

##############################################################################
# zero suppression menus
zsStandardMenu = mp7.ZeroSuppressionMenu()

zsStandardMenu.setValidationMode(0xd1) # validation every 107th event
zsStandardMenu[0].enable = False
zsStandardMenu[0].data = [0xffffffff]*6

zsStandardMenu[1].enable = True
zsStandardMenu[1].data = [0x1ff, 0x0]*3

zsStandardMenu[2].enable = True
zsStandardMenu[2].data = [0x3fc00, 0x0]*3

zsStandardMenu[3].enable = False
zsStandardMenu[3].data = [0xffffffff]*6

zsStandardMenu[4].enable = False
zsStandardMenu[4].data = [0xffffffff]*6

zsStandardMenu[5].enable = False
zsStandardMenu[5].data = [0xffffffff]*6

zsStandardMenu[6].enable = False
zsStandardMenu[6].data = [0xffffffff]*6

zsStandardMenu[7].enable = False
zsStandardMenu[7].data = [0xffffffff]*6

zsStandardMenu[8].enable = False
zsStandardMenu[8].data = [0xffffffff]*6

zsStandardMenu[9].enable = False
zsStandardMenu[9].data = [0xffffffff]*6

zsStandardMenu[10].enable = False
zsStandardMenu[10].data = [0xffffffff]*6

zsStandardMenu[11].enable = False
zsStandardMenu[11].data = [0xffffffff]*6

zsStandardMenu[12].enable = False
zsStandardMenu[12].data = [0xffffffff]*6

zsStandardMenu[13].enable = False
zsStandardMenu[13].data = [0xffffffff]*6

zsStandardMenu[14].enable = False
zsStandardMenu[14].data = [0xffffffff]*6

zsStandardMenu[15].enable = False
zsStandardMenu[15].data = [0xffffffff]*6

