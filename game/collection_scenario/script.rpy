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
default backbuttonenable = True
default bagging = False
default current_bag_item = ""
default click_object = ""
default last_area = ""
default last_action = ""
default dusted = {"mug": False, "weedbag": False, "pill": False}
default uvd = {"mug": False, "weedbag": False, "pill": False}
default scalebard = {"mug": False, "weedbag": False, "pill": False}
default taped = {"mug": False, "weedbag": False, "pill": False}
default backed = {"mug": False, "weedbag": False, "pill": False}
default num_evidence = 0
default collected_objs = {"weedbag": False, "pill": False, "brownie": False}

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
    if collected_objs["weedbag"] == False:
        imagebutton:
            auto "images/Environment Items/weedbag-%s.png"
            xalign 0.1
            yalign 0.3
            action Jump("weedbagaction")
            sensitive button_yes
    if collected_objs["pill"] == False:
        imagebutton:
            auto "images/Environment Items/pill-%s.png"
            xalign 0.75
            yalign 0.85
            action Jump("pillaction")
            sensitive button_yes

screen topInteractables():
    imagebutton:
        auto "images/Environment Items/brownies-%s.png"
        xalign 0.3
        yalign 0
        action Jump("brownieaction")
        sensitive button_yes
    imagebutton:
        auto "images/Environment Items/mug-%s.png"
        xalign 0.9999
        yalign 0.8
        action Jump("mugaction")
        sensitive button_yes

screen backButton():
    if last_area != "" and backbuttonenable == True:
        imagebutton:
            auto "images/Environment Items/back_button_%s.png"
            xalign 0.99
            yalign 0.1
            if last_area == "countertop":
                action Jump("countertop")
            elif last_area == "kitchen":
                action Jump("start")
            elif last_area == "trash":
                action Jump("trashbin")
            sensitive button_yes

screen bagitup():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1920
        ysize 1080
        background Solid("#0000003b")

# ADD A 'Are you sure you would like to collect this evidence?' when tap
screen browniecollect():
    zorder -1
    if collected_objs["brownie"] == False:
        imagebutton:
            auto "images/Environment Items/brownie-%s.png"
            xalign 0.5
            yalign 0.5
            action Jump("browniecollected")
            sensitive button_yes
screen weedbagcollect():
    zorder -1
    if collected_objs["weedbag"] == False:
        imagebutton:
            hover "images/Environment Items/weedbag-clear.png"
            idle "images/Environment Items/weedbag-full.png"
            xalign 0.5
            yalign 0.5
            action Jump("weedbagcollected")
            sensitive button_yes
screen pillcollect():
    zorder -1
    if collected_objs["pill"] == False:
        imagebutton:
            hover "images/Environment Items/pill-clear.png"
            idle "images/Environment Items/pill-full.png"
            xalign 0.5
            yalign 0.5
            action Jump("pillcollected")
            sensitive button_yes
# LABELS ------------------------------------------------------------------------
label start:
    scene kitchen
    $ last_area = ""
    show screen kitchenInteractables
    # INSERT DIALOGUE HERE, have a dependency variable
    $ button_yes = True
    show screen backButton
    call screen kitchenInteractables
    pause

label trashbin:
    hide screen weedbagcollect
    hide screen pillcollect
    $ last_area = "kitchen"
    $ button_yes = False
    scene trashinside
    # INSERT DIALOGUE HERE, have a dependency variable
    $ button_yes = True
    call screen trashInteractables
    pause

label countertop:
    hide screen browniecollect
    $ last_area = "kitchen"
    $ button_yes = False
    scene countertop
    # INSERT DIALOGUE HERE, have a dependency variable
    $ button_yes = True
    call screen topInteractables
    pause

# OBJECT ACTIONS -------------------------------------------
label brownieaction:
    $ button_yes = True
    $ last_area = "countertop"
    scene black # CHANGE TO COUNTER PNG LATER
    $ click_object = "brownie"
    if collected_objs["brownie"] == False:
        show screen browniecollect
    $ last_action = "brownieaction"
    call screen inventory
label browniecollected:
    "Are you sure you would like to collect this? Doing so prevents you from doing any tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory":
            $ collected_objs["brownie"] = True
            "A sample of the brownie has been added to your inventory."
            $ evidence.add_to_inventory(evids["Brownie"])
            $ num_evidence += 1
            #$ backbuttonenable = False
            jump expression last_action
        "No":
            jump expression last_action

label weedbagaction:
    $ button_yes = True
    $ last_area = "trash"
    scene black # CHANGE TO COUNTER PNG LATER
    $ click_object = "weedbag"
    if collected_objs["weedbag"] == False:
        show weedbag-idle:
            xalign 0.5
            yalign 0.5
        show screen weedbagcollect
        if dusted.get(click_object) == True:
            show fingerprint2_black:
                zoom 0.2
                xalign 0.4
                yalign 0.4
                alpha 1
        elif uvd.get(click_object) == False:
            show fingerprint2_idle:
                zoom 0.2
                xalign 0.4
                yalign 0.4
                alpha 0.7
        elif uvd.get(click_object) == True:
            show fingerprint2_white:
                zoom 0.2
                xalign 0.4
                yalign 0.4
        if scalebard.get(click_object) == True:
            show scale:
                zoom 0.3
                xalign 0.465
                yalign 0.4
                anchor (0.5, 0.5)
                rotate 280
        if taped.get(click_object) == True:
            show tapepiece:
                zoom 0.2
                xalign 0.4
                yalign 0.4
        if backed.get(click_object) == True:
            hide tapepiece
            hide scale
            hide fingerprint2_black
    $ last_action = "weedbagaction"
    call screen inventory
label weedbagcollected:
    "Are you sure you would like to collect this? Doing so prevents you from doing any tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory":
            $ collected_objs["weedbag"] = True
            "Evidence has been added to your inventory."
            $ evidence.add_to_inventory(evids["Plastic bag"])
            $ num_evidence += 1
            #$ backbuttonenable = False
            jump expression last_action
        "No":
            jump expression last_action

label pillaction:
    $ button_yes = True
    $ last_area = "trash"
    scene black # CHANGE TO COUNTER PNG LATER
    $ click_object = "pill"
    if collected_objs["pill"] == False:
        show screen pillcollect
        show pill-idle:
            xalign 0.5
            yalign 0.5
        if dusted.get(click_object) == True:
            show fingerprint1_black:
                zoom 0.1
                xalign 0.5
                yalign 0.5
                alpha 0.75
        elif uvd.get(click_object) == False:
            show fingerprint1_idle:
                zoom 0.1
                xalign 0.5
                yalign 0.5
                alpha 0.3
        elif uvd.get(click_object) == True:
            show fingerprint1_white:
                zoom 0.1
                xalign 0.5
                yalign 0.5
        if scalebard.get(click_object) == True:
            show scale:
                zoom 0.16
                xalign 0.465
                yalign 0.5
                anchor (0.5, 0.5)
                rotate 280
        if taped.get(click_object) == True:
            show tapepiece:
                zoom 0.1
                xalign 0.5
                yalign 0.5
        if backed.get(click_object) == True:
            hide tapepiece
            hide scale
            hide fingerprint1_black
    $ last_action = "pillaction"
    call screen inventory
label pillcollected:
    "Are you sure you would like to collect this? Doing so prevents you from doing any tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory":
            $ collected_objs["pill"] = True
            "Evidence has been added to your inventory."
            $ evidence.add_to_inventory(evids["Pill bottle"])
            $ num_evidence += 1
            #$ backbuttonenable = False
            jump expression last_action
        "No":
            jump expression last_action

label mugaction:
    $ last_area = "countertop"
    scene black # CHANGE TO COUNTER PNG LATER
    $ click_object = "mug"
    show mug-idle:
        zoom 2
        xalign 0.5
    if dusted.get(click_object) == True:
        show fingerprint1_black:
            zoom 0.1
            xalign 0.65
            yalign 0.5
            alpha 0.75
    elif uvd.get(click_object) == False:
        show fingerprint1_idle:
            zoom 0.1
            xalign 0.65
            yalign 0.5
            alpha 0.75
    elif uvd.get(click_object) == True:
        show fingerprint1_white:
            zoom 0.1
            xalign 0.65
            yalign 0.5
    if scalebard.get(click_object) == True:
        show scale:
            zoom 0.2
            xalign 0.68
            yalign 0.5
            anchor (0.5, 0.5)
            rotate 270
    if taped.get(click_object) == True:
        show tapepiece:
            zoom 0.2
            xalign 0.7
            yalign 0.5
    if backed.get(click_object) == True:
        hide tapepiece
        hide scale
        hide fingerprint1_black
    $ last_action = "mugaction"
    call screen inventory

# EVIDENCE STUFF ACTIONS -------------------------------------
# FINGERPRINTS _____
label canMagneticPowder:
    if bagging == False:
        if (click_object == "mug") or (click_object == "pill") or (click_object == "weedbag"):
            jump useMagneticPowder
        else:
            "There are no fingerprints here."
            jump expression last_action
    elif bagging == True:
        "Please select a piece of evidence"
        jump askWhatToBag

label useMagneticPowder:
    if click_object == "mug" or click_object == "pill":
        hide fingerprint1_idle
        hide fingerprint1_white
    else: #weedbag
        hide fingerprint2_idle
        hide fingerprint2_white
    if dusted.get(click_object) == True:
        "You've already dusted the fingerprints on this object."
    $ dusted[click_object] = True
    jump expression last_action

label useUVLight: # OPTIONAL, cant use after dusted
    if bagging == False:
        if dusted.get(click_object) == True:
            "You've already dusted the fingerprints on this object."
            jump expression last_action
        else: # MAY MODIFY THIS SECTION TO ALLOW FOR THE HOVER STUFF
            if click_object == "mug" or click_object == "pill":
                $ uvd[click_object] = True
                hide fingerprint1_idle
                jump expression last_action
            elif click_object == "weedbag":
                $ uvd[click_object] = True
                hide fingerprint2_idle
                jump expression last_action
    elif bagging == True:
        "Please select a piece of evidence"
        jump askWhatToBag

label useScaleBar: # (not required to bag evidence) CURRENTLY THE IMG IS ALWAYS WITH SCALEBAR
    if bagging == False:
        if (click_object == "mug") or (click_object == "pill") or (click_object == "weedbag"):
            if scalebard[click_object] == True or dusted[click_object] == False:
                "There's nothing to use this on."
                jump expression last_action
            elif taped[click_object] == True:
                "You can't use a scale bar."
                jump expression last_action
            elif dusted[click_object] == True:
                $ scalebard[click_object] = True
                jump expression last_action
        else:
            "There's nothing to use this on."
            jump expression last_action
    elif bagging == True:
        "Please select a piece of evidence"
        jump askWhatToBag

label useTape: 
    if bagging == False:
        if (click_object == "mug") or (click_object == "pill") or (click_object == "weedbag"):
            if taped[click_object] == True or dusted[click_object] == False:
                "There's nothing to use this on."
                jump expression last_action
            elif dusted[click_object] == True: # change this to scaled[click_object] == True for scalebar to be required
                $ taped[click_object] = True
                jump expression last_action
        else:
            "There's nothing to use this on."
            jump expression last_action
    elif bagging == True:
        "Please select a piece of evidence"
        jump askWhatToBag

label useBackingcard:
    if bagging == False:
        if (click_object == "mug") or (click_object == "pill") or (click_object == "weedbag"):
            if backed[click_object] == True or taped[click_object] == False:
                "There's nothing to use this on."
                jump expression last_action
            elif taped[click_object] == True:
                $ backed[click_object] = True
                "Evidence added to inventory"
                if click_object == "mug":
                    $ evidence.add_to_inventory(evids["Fingerprint 1"])
                elif click_object == "weedbag":
                    $ evidence.add_to_inventory(evids["Fingerprint 2"])
                elif click_object == "pill":
                    $ evidence.add_to_inventory(evids["Fingerprint 3"])
                $ num_evidence += 1
                jump expression last_action
        else:
            "There's nothing to use this on."
            jump expression last_action
    elif bagging == True:
        "Please select a piece of evidence"
        jump askWhatToBag
# END OF FINGERPRINTS _____
# EVIDENCE BAG ___________________
label askWhatToBag:
    if num_evidence != 0:
        hide screen bagitup
        show screen bagitup
        $ bagging = True
        $ backbuttonenable = False
        show openbag:
            xalign 0.5
            yalign 0.5
        "Please select the evidence you would like to bag from your inventory."
        call screen inventory
    else:
        "There's nothing in your inventory to bag. Collect it first."
        jump expression last_action
label useTamperTape:
    if current_bag_item != "":
        if current_bag_item == "fingerprint1":
            $ evidence.add_to_inventory(evids["Bag Fingerprint 1"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bagitup
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "fingerprint2":
            $ evidence.add_to_inventory(evids["Bag Fingerprint 2"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bagitup
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "fingerprint3":
            $ evidence.add_to_inventory(evids["Bag Fingerprint 3"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bagitup
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "brownie":
            $ evidence.add_to_inventory(evids["Bag Brownie"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bagitup
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "weedbag":
            $ evidence.add_to_inventory(evids["Bag Plastic bag"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bagitup
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "pill":
            $ evidence.add_to_inventory(evids["Bag Pill bottle"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bagitup
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
    else:
        "Please put evidence in an evidence bag first."
        jump expression last_action

label bagItem1:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "fingerprint1"
        "Item has been placed in the evidence bag."
        $ evidence.delete_from_inventory(evids["Fingerprint 1"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!"
        call screen inventory
    else:
        jump expression last_action
label bagItem2:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "fingerprint2"
        "Item has been placed in the evidence bag."
        $ evidence.delete_from_inventory(evids["Fingerprint 2"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!"
        call screen inventory
    else:
        jump expression last_action
label bagItem3:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "fingerprint3"
        "Item has been placed in the evidence bag."
        $ evidence.delete_from_inventory(evids["Fingerprint 3"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!"
        call screen inventory
    else:
        jump expression last_action
label bagItem4:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "brownie"
        "Item has been placed in the evidence bag."
        $ evidence.delete_from_inventory(evids["Brownie"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!"
        call screen inventory
    else:
        jump expression last_action
label bagItem5:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "weedbag"
        "Item has been placed in the evidence bag."
        $ evidence.delete_from_inventory(evids["Plastic bag"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!"
        call screen inventory
    else:
        jump expression last_action
label bagItem6:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "pill"
        "Item has been placed in the evidence bag."
        $ evidence.delete_from_inventory(evids["Pill bottle"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!"
        call screen inventory
    else:
        jump expression last_action




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