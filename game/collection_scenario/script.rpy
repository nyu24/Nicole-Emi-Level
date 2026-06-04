init python:
    import json

    tools = load_items("jsons/toolbox.json")
    # FINGERPRINT STUFF
    toolbox.add_to_inventory(tools["Backing Card"])
    toolbox.add_to_inventory(tools["Scalebar"])
    toolbox.add_to_inventory(tools["Magnetic Powder"])
    toolbox.add_to_inventory(tools["Tape"])
    # EVIDNECE BAG
    toolbox.add_to_inventory(tools["Evidence Bag"])
    toolbox.add_to_inventory(tools["Tamper Evident Tape"])
    # SWABBING
    toolbox.add_to_inventory(tools["Swab Pack"])
    toolbox.add_to_inventory(tools["Tube"])
    toolbox.add_to_inventory(tools["UV Light"])
    

    evids = load_items("jsons/evidence.json")

    #for evid in evids.values():
    #    evidence.add_to_inventory(evid)


define n = Character(name=("Nina"), image="nina")
default button_yes = False
# SCREENS -----------------------------------------------------------------
screen kitchenInteractables():
    imagebutton:
        auto "images/Environment Items/trash-%s.png"
        xalign 0
        yalign 0.999999999
        action Jump("trashbin")
        sensitive button_yes
    imagebutton:
        auto "images/Environment Items/counter-%s.png"
        xalign 0.999999999
        yalign 0.999999999
        action Jump("countertop")
        sensitive button_yes

screen trashInteractables():
    imagebutton:
        auto "images/Environment Items/weedbag-%s.png"
        xalign 0.1
        yalign 0.3
        action Jump("start") # CHANGE ACTION TO CORRECT STEPS
        sensitive button_yes
    imagebutton:
        auto "images/Environment Items/pill-%s.png"
        xalign 0.75
        yalign 0.85
        action Jump("start") # CHANGE ACTION TO CORRECT STEPS
        sensitive button_yes

screen topInteractables():
    imagebutton:
        auto "images/Environment Items/brownies-%s.png"
        xalign 0.5
        yalign 0
        action Jump("start") # CHANGE ACTION TO CORRECT STEPS
        sensitive button_yes
    imagebutton:
        auto "images/Environment Items/mug-%s.png"
        xalign 0.9999
        yalign 0.7
        action Jump("start") # CHANGE ACTION TO CORRECT STEPS
        sensitive button_yes

# LABELS ------------------------------------------------------------------------
label start:
    scene kitchen
    show screen kitchenInteractables
    # INSERT DIALOGUE HERE, have a dependency variable
    $ button_yes = True
    call screen kitchenInteractables
    pause

label trashbin:
    $ button_yes = False
    scene trashinside
    # INSERT DIALOGUE HERE, have a dependency variable
    $ button_yes = True
    call screen trashInteractables
    pause

label countertop:
    $ button_yes = False
    scene countertop
    # INSERT DIALOGUE HERE, have a dependency variable
    $ button_yes = True
    call screen topInteractables
    pause




    #show nina normal1
    #n "This is a template project that you can use to create your levels!"
    #n "My name is Nina and I'm usually in the evidence collection level."
    #n "This level is where you collect evidence to be later analyzed in the lab."
    #show nina talk
    #n "All code related to this level should be placed under the collection_scenario folder."
    #n "You can have as many subdirectories as you'd like underneath it!"
    #show nina normal1
    #n "There will be three levels in your game: the evidence collection level, the lab level, and the courtroom level."
    #n "There's one directory for each level."
    #n "All levels use an inventory system which will be shown on the left-hand side."
    #show nina thinknote1
    #n "Try playing around with it!"
    #call screen inventory
    

#label sample:
    #show nina normal1
    #n "Great job!"
    #show nina talk
    #n "There are more detailed instructions on how to use the inventory in inventory.rpy, so make sure to check that out!"
    #n "Now, back to the overall structure of the game!"
    #show nina thinknote1
    #n "Once the player has finished collecting all their evidence, we should move on to the lab level for analysis."
    #n "This won't be covered until later on though. For now, give yourselves a pat on the back!"
    #return