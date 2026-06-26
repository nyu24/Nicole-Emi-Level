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

    # FUNCTIONS FOR DRAG AND DROP
    def put_in_bag(drags, drop):
        if drop:
            return True
        else: 
            return

    #for evid in evids.values():
    #    evidence.add_to_inventory(evid)

# some notes:
# anything labeled 'ATTENTION' requires manually change

define n = Character(name=("Nina"), image="nina")

default got_intro = False
default button_yes = False
default backbuttonenable = True
default bagging = False
default current_bag_item = ""
default click_object = ""
default last_area = ""
default last_action = ""
# for fingerprinting
default can_fingerprint = ["mug", "weedbag", "pill", "pilltop"]
default fingerprint1_stuff = ["mug", "pill", "pilltop"]
default fingerprint2_stuff = ["weedbag"]
default dusted = {"mug": False, "weedbag": False, "pill": False, "pilltop": False}
default uvd = {"mug": False, "weedbag": False, "pill": False, "pilltop": False}
default scalebard = {"mug": False, "weedbag": False, "pill": False, "pilltop": False}
default taped = {"mug": False, "weedbag": False, "pill": False, "pilltop": False}
default backed = {"mug": False, "weedbag": False, "pill": False, "pilltop": False}
default num_evidence = 0
# for bagged evidence
default collected_objs = {"weedbag": False, "pill": False, "brownie": False}
default pill_status = 0 # even default, odd top

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

#screen bagitup():
#    frame:
#        xalign 0.5
#        yalign 0.5
#        xsize 1920
#        ysize 1080
#        background Solid("#0000003b")


screen browniecollect():
    zorder -1
    if collected_objs["brownie"] == False:
        textbutton "Collect item?":
            style_prefix "textB"
            text_idle_color "#ffffffff"
            text_hover_color "#35ffe4ff"
            background "#696969ff"
            xalign 0.85
            yalign 0.85
            action Jump("browniecollected")
            sensitive button_yes
screen weedbagcollect():
    zorder -1
    if collected_objs["weedbag"] == False and backbuttonenable == True:
        textbutton "Collect item?":
            style_prefix "textB"
            text_idle_color "#ffffffff"
            text_hover_color "#35ffe4ff"
            background "#696969ff"
            xalign 0.85
            yalign 0.85
            action Jump("weedbagcollected")
            sensitive button_yes
screen pillcollect():
    zorder -1
    if collected_objs["pill"] == False and backbuttonenable == True:
        # button to turn the pill bottle
        imagebutton:
            auto "images/Environment Items/turn-%s.png"
            xalign 0.65
            yalign 0.3
            action Jump("pillturned")
            sensitive button_yes
        textbutton "Collect item?":
            style_prefix "textB"
            text_idle_color "#ffffffff"
            text_hover_color "#35ffe4ff"
            background "#696969ff"
            xalign 0.85
            yalign 0.85
            action Jump("pillcollected")
            sensitive button_yes


# drag screens
screen tape_drag_screen():
    zorder -1
    draggroup:
        drag:
            drag_name "evidence_bag"
            draggable False
            droppable True
            dropped put_in_bag
            xpos 1000 ypos 100
            child "images/evidence/openbag.png"
        drag:
            drag_name "evidence_tape"
            draggable True
            droppable False
            xpos 300 ypos 300
            drag_raise True
            child "images/Environment Items/tet.png"

screen item_deposit_screen():
    zorder -1
    draggroup:
        drag:
            drag_name "bag_drop"
            droppable True
            draggable False
            dropped put_in_bag
            xpos 1000 ypos 100
            child "images/evidence/openbag.png"
        drag:
            drag_name "item_drag"
            draggable True
            droppable False
            xpos 300 ypos 300
            drag_raise True
            if("finger" in current_bag_item):
                child "images/Environment Items/backing fingerprint.png"
            elif(current_bag_item == "brownie"):
                child "images/Environment Items/brownie_idle.png"
            elif(current_bag_item == "weedbag"):
                child "images/Environment Items/weedbag-idle.png"
            elif(current_bag_item == "pill"):
                child "images/Environment Items/pill-idle.png"

# To display the screen in your script:
# call screen drag_screen


# LABELS ------------------------------------------------------------------------
label start:
    scene kitchen
    $ last_area = ""
    show screen kitchenInteractables
    if(got_intro == False):
        # INSERT DIALOGUE HERE, have a dependency variable
        show nina normal1
        n "You're finally here!"
        n "Here's a rundown of the scene."
        show nina thinknote1
        n "Around an hour ago a man passed away at this house party."
        n "His friends don't know what happened besides him suddenly collapsing. Though one did mention that drugs were on the premises."
        show nina talk
        n "So, an otherwise healthy male in his 20s suddenly dies. Curious huh?"
        show nina thinknote1
        n "Oh! by the way, the body's already on its way to the morgue. So you'll be able to do an autopsy later at the lab."
        show nina normal1
        n "I need you to collect evidence and do a sweep of the kitchen to help determine the cause of death."
        n "Remember your training. And goodluck."
        hide nina normal1
        $ got_intro = True
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
    scene black
    $ click_object = "brownie"
    if collected_objs["brownie"] == False:
        show brownie_idle:
            xalign 0.5
            yalign 0.5
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
    scene black 
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
    hide screen inventory
    $ button_yes = True
    $ last_area = "trash"
    scene black 
    if collected_objs["pill"] == False:
        show screen pillcollect
        # if status is even, show the side view/default of the pill bottle
        if(pill_status % 2 == 0):
            $ click_object = "pill"
            show pill-idle:
                xalign 0.5
                yalign 0.5
            if dusted.get(click_object) == True:
                show fingerprint1_black:
                    zoom 0.08
                    xalign 0.58
                    yalign 0.4
                    alpha 0.75
            elif uvd.get(click_object) == False:
                show fingerprint1_idle:
                    zoom 0.08
                    xalign 0.58
                    yalign 0.4
                    alpha 0.3
            elif uvd.get(click_object) == True:
                show fingerprint1_white:
                    zoom 0.08
                    xalign 0.58
                    yalign 0.4
            if scalebard.get(click_object) == True:
                show scale:
                    zoom 0.16
                    xalign 0.54
                    yalign 0.4
                    anchor (0.5, 0.5)
                    rotate 280
            if taped.get(click_object) == True:
                show tapepiece:
                    zoom 0.1
                    xalign 0.58
                    yalign 0.4
            if backed.get(click_object) == True:
                hide tapepiece
                hide scale
                hide fingerprint1_black
        elif (pill_status%2 == 1):
            $ click_object = "pilltop"
            show pill-top:
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
label pillturned:
    $ pill_status += 1
    jump expression last_action


label mugaction:
    $ last_area = "countertop"
    scene black 
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
        if (click_object in can_fingerprint):
            jump useMagneticPowder
        else:
            "There are no fingerprints here."
            jump expression last_action
    elif bagging == True:
        "Please select a piece of evidence"
        jump askWhatToBag

label useMagneticPowder:
    if click_object in fingerprint1_stuff:
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
            if click_object in fingerprint1_stuff:
                $ uvd[click_object] = True
                hide fingerprint1_idle
                jump expression last_action
            elif click_object in fingerprint2_stuff:
                $ uvd[click_object] = True
                hide fingerprint2_idle
                jump expression last_action
    elif bagging == True:
        "Please select a piece of evidence"
        jump askWhatToBag

label useScaleBar: # (not required to bag evidence) CURRENTLY THE IMG IS ALWAYS WITH SCALEBAR
    if bagging == False:
        if (click_object in can_fingerprint):
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
        if (click_object in can_fingerprint):
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
        if (click_object in can_fingerprint):
            if backed[click_object] == True or taped[click_object] == False:
                "There's nothing to use this on."
                jump expression last_action
            elif taped[click_object] == True:
                $ backed[click_object] = True
                # ATTENTION! FOR THIS SECTION NEW FINGERPRINTS NEED TO BE ADDED MANUALLY
                # TODO: can make changes here for more sophisticated fingerprinting
                "Evidence added to inventory"
                if click_object == "mug":
                    $ evidence.add_to_inventory(evids["Fingerprint 1"])
                elif click_object == "weedbag":
                    $ evidence.add_to_inventory(evids["Fingerprint 2"])
                elif click_object == "pilltop":
                    $ evidence.add_to_inventory(evids["Fingerprint 3"])
                elif click_object == "pill":
                    # ATTENTION! might need to change this dialogue AND for end game, minus 1 point or smthg idk
                    n "More than half of the print is missing from the tape."
                    n "It seems like the textured surface interfered with the sample. We can't use this as evidence."
                    $ num_evidence -= 1
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
    scene black
    hide screen weedbagcollect
    hide screen pillcollect
    hide screen browniecollect
    if num_evidence != 0:
        $ bagging = True
        $ backbuttonenable = False
        show openbag:
            xpos 1000 
            ypos 100
        "Please select the evidence you would like to bag from your inventory."
        call screen inventory
    else:
        "There's nothing in your inventory to bag. Collect it first."
        jump expression last_action
label useTamperTape:
    if current_bag_item != "":
        if current_bag_item == "fingerprint1":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Fingerprint 1"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            #hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "fingerprint2":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Fingerprint 2"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "fingerprint3":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Fingerprint 3"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "brownie":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Brownie"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "weedbag":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100
            $ evidence.add_to_inventory(evids["Bag Plastic bag"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
        elif current_bag_item == "pill":
            call screen tape_drag_screen
            hide openbag
            show sealedbag:
                xpos 1000 
                ypos 100R
            $ evidence.add_to_inventory(evids["Bag Pill bottle"])
            "Bagged evidence has been added to your inventory"
            $ num_evidence -= 1
            hide screen bag_drag_screen
            $ backbuttonenable = True
            $ bagging = False
            $ current_bag_item = ""
            jump expression last_action
    else:
        "Please put evidence in an evidence bag first."
        jump expression last_action

label remove_item:
    hide screen item_deposit_screen
    jump expression last_action

label bagItem1:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "fingerprint1"
        call screen item_deposit_screen
        $ evidence.delete_from_inventory(evids["Fingerprint 1"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!1"
        call screen inventory
    else:
        jump expression last_action
label bagItem2:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "fingerprint2"
        call screen item_deposit_screen
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
        call screen item_deposit_screen
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
        call screen item_deposit_screen
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
        call screen item_deposit_screen
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
        call screen item_deposit_screen
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