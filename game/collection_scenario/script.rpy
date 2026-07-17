init python:
    import json

    tools = load_items("jsons/toolbox.json")
    # GLOVES
    toolbox.add_to_inventory(tools["gloves"])
    # FINGERPRINT STUFF
    toolbox.add_to_inventory(tools["Backing Card"])
    toolbox.add_to_inventory(tools["Scalebar"])
    toolbox.add_to_inventory(tools["Magnetic Powder"])
    toolbox.add_to_inventory(tools["Tape"])
    # EVIDNECE BAG
    toolbox.add_to_inventory(tools["Evidence Bag"])
    toolbox.add_to_inventory(tools["Tamper Evident Tape"])

    evids = load_items("jsons/evidence.json")

    # FUNCTION FOR DRAG AND DROP
    def put_in_bag(drags, drop):
        if drop:
            return True
        else: 
            return

define n = Character(name=("Nina"), image="nina")

# HOSPITAL VARS
default got_testimony = {"parents": False, "friends": False}
default want_collection_scenario = False    # USED FOR GIVING PHOTOS OF THE HOUSE PARTY
default parent_count = {"1": 0, "2": 0, "3": 0}
default friend_count = {"1": 0, "2": 0, "3": 0}
default parent_1 = ""
default parent_2 = ""
default parent_3 = ""
default friend_1 = ""
default friend_2 = ""
default friend_3 = ""
# HOUSE VARS
default got_intro = False
default button_yes = False
default backbuttonenable = True
default bagging = False
default current_bag_item = ""
default click_object = ""
default last_area = ""
default last_action = ""
default put_gloves = False
# for fingerprinting
default fingerprint_toback = ""
default can_fingerprint = ["weedbag", "pill", "pilltop"]
default fingerprint1_stuff = ["pill", "pilltop"]
default fingerprint2_stuff = ["weedbag"]
default dusted = {"weedbag": False, "pill": False, "pilltop": False}
default uvd = {"weedbag": False, "pill": False, "pilltop": False}
default scalebard = {"weedbag": False, "pill": False, "pilltop": False}
default taped = {"weedbag": False, "pill": False, "pilltop": False}
default backed = {"weedbag": False, "pill": False, "pilltop": False}
default num_evidence = 0
default sf = False
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
    imagebutton:
        auto "images/Environment Items/counterleft-%s.png"
        xalign 0.13
        yalign 0.5
        action Jump("countertopleft")
        sensitive button_yes

screen trashInteractables():
    if collected_objs["weedbag"] == False:
        imagebutton:
            auto "images/Environment Items/weedbag-%s.png"
            xalign 0.5
            yalign 0.3
            action Jump("weedbagaction")
            sensitive button_yes

screen topInteractables():
    imagebutton:
        auto "images/Environment Items/brownies-%s.png"
        xalign 0.999
        yalign 0.7
        action Jump("brownieaction")
        sensitive button_yes
    imagebutton:
        auto "images/Environment Items/juice-%s.png"
        xalign 0.3
        yalign 0
        action Jump("countertop")
        sensitive button_yes

screen topleftInteractables():
    if collected_objs["pill"] == False:
        imagebutton:
            auto "images/Environment Items/pill-%s.png"
            xalign 0.4
            yalign 0.4
            action Jump("pillaction")
            sensitive button_yes

screen backButton():
    if last_area != "" and backbuttonenable == True and sf == False:
        imagebutton:
            auto "images/Environment Items/back_button_%s.png"
            xalign 0.99
            yalign 0.1
            if last_area == "countertop":
                action Jump("countertop")
            elif last_area == "kitchen":
                action Jump("house")
            elif last_area == "trash":
                action Jump("trashbin")
            elif last_area == "houseoutside":
                action Jump("houseoutside")
            elif last_area == "countertopleft":
                action Jump("countertopleft")
            sensitive button_yes

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

screen hospitaloutsideInteractables():
    zorder -1
    imagebutton:
        auto "images/Environment Items/hospitaloutside-%s.png"
        xalign 0.05
        yalign 0.5
        action Jump("insidehospital")
        at Transform(zoom=1.2)

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

screen finger_drag():
    zorder -1
    draggroup:
        drag:
            drag_name "backing_drop"
            droppable True
            draggable False
            dropped put_in_bag
            xpos 1000 ypos 100
            child "images/Environment Items/backing_card.png"
        drag:
            drag_name "item_drag"
            draggable True
            droppable False
            xpos 300 ypos 300
            drag_raise True
            if("finger2 NS" == fingerprint_toback):
                child "images/Environment Items/finger2NS.png"
            elif("finger2 S" == fingerprint_toback):
                child "images/Environment Items/finger2S.png"
            elif("finger1 NS" == fingerprint_toback):
                child "images/Environment Items/finger1NS.png"
            elif("finger1 S" == fingerprint_toback):
                child "images/Environment Items/finger1S.png"

screen write_drag():
    zorder -1
    draggroup:
        drag:
            drag_name "backing_drop"
            droppable True
            draggable False
            dropped put_in_bag
            xpos 1000 ypos 100
            if("finger2 NS" == fingerprint_toback):
                child "images/Environment Items/finger2_noscale.png"
            elif("finger2 S" == fingerprint_toback):
                child "images/Environment Items/finger2_scale.png"
            elif("finger1 NS" == fingerprint_toback):
                child "images/Environment Items/finger1_noscale.png"
            elif("finger1 S" == fingerprint_toback):
                child "images/Environment Items/finger1_scale.png"
        drag:
            drag_name "item_drag"
            draggable True
            droppable False
            xpos 300 ypos 300
            drag_raise True
            if("finger2 NS" == fingerprint_toback):
                child "images/Environment Items/R.png"
            elif("finger2 S" == fingerprint_toback):
                child "images/Environment Items/R.png"
            elif("finger1 NS" == fingerprint_toback):
                child "images/Environment Items/L.png"
            elif("finger1 S" == fingerprint_toback):
                child "images/Environment Items/L.png"

# LABELS ------------------------------------------------------------------------
# HOSPITAL SECTION -------------------------------------------------------------------------------------------------------------
#
#
# -------------------------------------------------------------------------------------------------------------
label start:
    scene hospitaloutside
    # brief on the scenario + testimona
    show nina normal1
    n "You might be wondering why I've brought you to the hospital."
    n "Well, there's a new case."
    n "A few hours ago, a 25 year old male collapsed during a house party. He died an hour ago here at the hospital."
    show nina thinknote1
    n "Hospital staff has confirmed that the man died from overdosing on his blood pressure medication."
    n "However, we've been called in because his parents are adamant about his death being some sort of malicious plot."
    n "According to the parents, their son was a happy man and would never commit suicide..."
    show nina talk
    n "The staff has already given me 2 blood samples, one taken pre-mortem, the other post-mortem. In addition I have the man's medical history and the hospital report."
    n "I'll give them to you at the lab."
    n "Right now, I need you to go inside and get testimony statements from the parents and the other party go-er."
    n "Once you're done, meet me out here for the next steps."
    hide nina talk
    call screen hospitaloutsideInteractables
label insidehospital:
    scene hospital
    "Whose testimony do you want to get?"
    menu:
        "Parents" if got_testimony["parents"] != True:
            jump parents_testimony
        "Friend" if got_testimony["friends"] != True:
            jump friends_testimony
        "Return to Nina":
            jump return_to_nina

label parents_testimony:
    show parents
    "What do you want to ask?"
    menu:
        "[parent_1] About your son...":
            jump MDson
        "[parent_2] About what happened at the party...":
            jump MDparty
        "[parent_3] About Alastor Brahe's medical history...":
            jump MDmedhist
        "Thank them for their time and give out condolences." if (parent_count["1"] >= 1 and parent_count["2"] >= 1 and parent_count["3"] >= 1):
            hide parents
            "Parents testimony has been added to your inventory."
            $ evidence.add_to_inventory(evids["Parents Testimony"])
            $ got_testimony["parents"] = True
            jump insidehospital
label MDson:
    "Mrs Brahe: *sniff* Alastor was always such a happy child... Giggling over everything he found funny..."
    "Mrs Brahe: I don't understand how this could've happened! *sobsob*"
    "Mr Brahe: Alastor had his entire life in front of him. There's no way he would've overdosed on purpose!"
    "Mr Brahe: I don't know care about what the medical personnel here are saying, he wouldn't have killed himself!!!"
    "Mr Brahe: Someone must have done something to him at the party!"
    $ parent_count["1"] += 1
    $ parent_1 = "*DONE*"
    jump parents_testimony
label MDparty:
    "Mrs Brahe: *sobsob* He wanted to celebrate with his friends about getting into a masters program... All I know is that he invited a few people..."
    "Mr Brahe: We don't know exactly what happened at the party, I think you're better off asking someone who was there."
    $ parent_count["2"] += 1
    $ parent_2 = "*DONE*"
    jump parents_testimony
label MDmedhist:
    "Mrs Brahe: *sniff* He's complained about bad headaches and dizziness back in his undergraduate years... But he told me he went to the doctor's and is managing it."
    "Mr Brahe: Last time we asked about it, he mentioned something about a new medication he was taking, we don't know what it is though."
    "Mr Brahe: If you're wondering about mental illness, he's has no history of it. No depression, nothing."
    "Mr Brahe: So it doesn't make sense for him to have overdosed!"
    $ parent_count["3"] += 1
    $ parent_3 = "*DONE*"
    jump parents_testimony

label friends_testimony:
    show friend
    "What do you want to ask?"
    menu:
        "[friend_1] About their friend...":
            jump Ffriend
        "[friend_2] About what happened at the party...":
            jump Fparty
        "[friend_3] About Alastor Brahe's medical history...":
            jump Fmedhist
        "Thank them for their time and give out condolences." if (friend_count["1"] >= 1 and friend_count["2"] >= 1 and friend_count["3"] >= 1):
            hide friend
            "Friend testimony has been added to your inventory."
            $ evidence.add_to_inventory(evids["Friend Testimony"])
            $ got_testimony["friends"] = True
            jump insidehospital
label Ffriend:
    "Friend: Alastor was a good friend... I just can't believe this is happening, he was just fine at the party!"
    $ friend_count["1"] += 1
    $ friend_1 = "*DONE*"
    jump friends_testimony
label Fparty:
    "Friend: Besides him collapsing all of a sudden, he acted normally."
    "Friend: We were all drinking and having fun, and like usual Alastor only drank mocktails, we were joking around and baking..."
    "Friend: ... Listen, everyone brought something for the party, juices, alcohol, and someone even brought weed."
    "Friend: We all decided to bake some brownies with it, but I know it wasn't enough to cause Alastor to collapse. We didn't even put the whole bag in!"
    $ friend_count["2"] += 1
    $ friend_2 = "*DONE*"
    jump friends_testimony
label Fmedhist:
    "Friend: I don't know too much about his medical history... He prefered to keep that private."
    "Friend: But he has mentioned in the past about not being able to drink because of some medication he was on."
    "Friend: He also mentioned something about not being able to eat licorice?"
    "Friend: But I'm pretty sure he hated that stuff anyway."
    $ friend_count["3"] += 1
    $ friend_3 = "*DONE*"
    jump friends_testimony

label return_to_nina: 
    scene hospitaloutside
    show nina normal1
    n "Back already?"
    n "Well, now that you've gotten the testimonies, we should go to the lab and analyse the blood samples to double check for anything out of the ordinary."
    show nina thinknote1
    n "Normally, we wouldn't go back to the scene of the incident since there's no evidence of malicious intent..."
    n "But if you'd like to go and look around the party for possible causes of the man's death, I won't stop you."
    show nina talk
    n "Remember to follow protocol and bag everything up properly."
    n "Note that you won't be able to head there if you decide to go to the lab first."
    show nina normal1
    n "So, do you want to head straight to the lab? Or do you want to check the house party first?"
    menu:
        "Head to the house party":
            $ want_collection_scenario = True
            jump houseoutside
        "Head to the lab":
            $ want_collection_scenario = False
            hide nina normal1
            jump lab
    return
# CODE BELOW IS FOR THE LAB ------------------------------------------------------------------------------------------
# 
#
# -------------------------------------------------------------------------------------------------------------
# LAB VARS -----
default in_lab = False
# SPE
default has_SPE_pre = False
default has_SPE_post = False
default step_SPE = ""
default step_num_SPE = 1 # see ipad notes for specifics
default inv_call_SPE = ""
default choice_SPE = ""
# GC-MS

# LAB SCREENS ------

# LAB LABELS ----------
label lab:
    scene black
    $ in_lab = True
    #removing previous toolbox items
    $ toolbox.delete_from_inventory(tools["gloves"])
    $ toolbox.delete_from_inventory(tools["Backing Card"])
    $ toolbox.delete_from_inventory(tools["Scalebar"])
    $ toolbox.delete_from_inventory(tools["Magnetic Powder"])
    $ toolbox.delete_from_inventory(tools["Tape"])
    $ toolbox.delete_from_inventory(tools["Evidence Bag"])
    $ toolbox.delete_from_inventory(tools["Tamper Evident Tape"])

    # adding correct toolbox items
    $ toolbox.add_to_inventory(tools["100% Methanol"])
    $ toolbox.add_to_inventory(tools["Water"])
    $ toolbox.add_to_inventory(tools["1% Formic acid"])
    $ toolbox.add_to_inventory(tools["0.1% Formic acid"])
    $ toolbox.add_to_inventory(tools["Methanol and 5% Ammonium Hydroxide"])

    "What would you like to start with?"
    jump lab_choice
label lab_choice: # may add GC-MS and GC-headspace, but these are the minimum requirements to analyse
    scene black
    menu:
        "Solid phase extraction [choice_SPE]":
            jump solid_phase_extraction
        "LC-MS":
            jump lc_ms
        "Fingerprinting Analysis":
            jump fingerprint_analysis
        "Blender":
            jump blender
        "Vortex mixer":
            jump vortexmixer
        "Centrifuge":
            jump centrifuge
    return
# SOLID PHASE EXTRACTION CODE
label solid_phase_extraction:
    #PRE-TREATMENT
    scene spe11
    show nina talk
    n "Before you do anything, you'll need to pre-treat your sample and dilute it 1:1 with an acidic buffer."
    n "Which blood sample do you want to dilute?"
    hide nina talk
    menu:
        "Post-mortem blood sample" if not has_SPE_post:
            $ evidence.add_to_inventory(evids["Post blood sample"])
        "Pre-mortem blood sample" if not has_SPE_pre:
            $ evidence.add_to_inventory(evids["Pre blood sample"])
    "!!!!this is text for now I'll add photos + inventory functions later"
    jump SPE_dilute_question
label SPE_dilute_question:
    "What will you use to dilute the blood sample?"
    menu:
        "Formic acid in water":
            show nina normal1
            n "Alright! Now that you have your diluted mixture you can start the solid phase extraction."
            hide nina normal1
            jump SPE_condition
        "Methanol":
            "That doesn't sound right."
            hide nina thinknote1
            jump SPE_dilute_question
        "Just water":
            "That doesn't sound right."
            hide nina thinknote1
            jump SPE_dilute_question
    return
label SPE_condition:
    $ inv_call_SPE = "SPE_condition"
    $ step_SPE = "SPE_condition1"
    call screen inventory
label SPE_condition1:
    scene spe12
    $ step_num_SPE = 2 # catridge has been reinsed with methanol waiting for 2
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            jump SPE_condition2
        "1 mL/minute":
            "Wrong."
            jump SPE_condition1
label SPE_condition2:
    $ inv_call_SPE = "SPE_condition2"
    $ step_SPE = "SPE_condition3" #1% formic acid or water
    scene spe13
    call screen inventory
label SPE_condition3:
    scene spe14
    $ step_num_SPE = 3 # catridge has been reinsed with formic or water waiting for loading
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            jump SPE_loading
        "1 mL/minute":
            "Wrong."
            jump SPE_condition3

label SPE_loading:
    scene spe13
    $ renpy.pause(0.5, hard=True)
    scene spe21
    $ inv_call_SPE = "SPE_loading"
    $ step_SPE = "SPE_loading1"
    call screen inventory
label SPE_loading1:
    scene spe22
    $ step_num_SPE = 4 # blood in, next wash w/formic
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_loading1
        "1 mL/minute":
            jump SPE_washing

label SPE_washing:
    scene spe23
    $ renpy.pause(0.5, hard=True)
    scene spe31
    $ inv_call_SPE = "SPE_washing"
    $ step_SPE = "SPE_washing1"
    call screen inventory
label SPE_washing1:
    scene spe32
    $ step_num_SPE = 5 # washg fromic, next wash w/methanol
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_washing1
        "1 mL/minute":
            jump SPE_washing2
label SPE_washing2:
    scene spe33
    $ inv_call_SPE = "SPE_washing2"
    $ step_SPE = "SPE_washing3" #methanol
    call screen inventory
label SPE_washing3:
    scene spe34
    $ step_num_SPE = 6 # 5% ammonium hydroxide ELUTION
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_washing3
        "1 mL/minute":
            jump SPE_elution

label SPE_elution:
    scene spe33
    $ renpy.pause(0.5, hard=True)
    scene spe41
    $ inv_call_SPE = "SPE_elution"
    $ step_SPE = "SPE_elution1"
    call screen inventory
label SPE_elution1:
    scene spe42
    "Vacuum update to what flow rate?"
    menu:
        "5 mL/minute":
            "Wrong."
            jump SPE_elution1
        "1 mL/minute":
            jump SPE_elution2
label SPE_elution2:
    scene spe43
    "What temperature should the mixture be dried at?"
    # can add the timer, so like, do fingerprinting analysis while the mixture dries
    menu:
        "37 Celsius":
            scene spe44
            "You've obtained the prepared sample."
            if(has_SPE_post):
                $ evidence.add_to_inventory(evids["Prepared post blood sample"])
            else:
                $ evidence.add_to_inventory(evids["Prepared pre blood sample"])
            if(has_SPE_post and has_SPE_pre):
                $ choice_SPE = "COMPLETED"
            $ step_num_SPE = 1
            jump lab_choice
        # can add other choices here

# toolbox stuffs for SPE
label use5Amm:
    "How much will you add?"
    menu:
        "1 mL":
            if(step_num_SPE == 6):
                jump expression step_SPE
            else:
                "Wrong compound!"
                jump expression inv_call_SPE
        # can add other options here
label use01Formic:
    "How much will you add?"
    menu:
        "1 mL":
            if(step_num_SPE == 4):
                jump expression step_SPE
            else:
                "Wrong compound!"
                jump expression inv_call_SPE
        # can add other options here
label useMethanol:
    "How much will you add?"
    menu:
        "1 mL":
            if(step_num_SPE == 1 or step_num_SPE == 5):
                jump expression step_SPE
            else:
                "Wrong compound!"
                jump expression inv_call_SPE
        # can add other options here
label useStep3:
    "How much will you add?"
    menu:
        "1 mL":
            if(step_num_SPE == 2):
                jump expression step_SPE
            else:
                "Wrong compound!"
                jump expression inv_call_SPE
        # can add other options here
label usePost:
    $ has_SPE_post = True
    if(step_num_SPE == 3):
        $ evidence.delete_from_inventory(evids["Post blood sample"])
        jump expression step_SPE
    else:
        "Wrong compound!"
        jump expression inv_call_SPE
label usePre:
    $ has_SPE_pre = True
    if(step_num_SPE == 3):
        $ evidence.delete_from_inventory(evids["Pre blood sample"])
        jump expression step_SPE
    else:
        "Wrong compound!"
        jump expression inv_call_SPE

# LC-MS CODE --------------------------------------------------
label lc_ms:

label usePpostBS:

label usePpreBS:

# FOR BROWNIE CODE --------------------------------------------------
label blender:

label vortexmixer:

label centrifuge:
    
# FINGERPRINT ANALYSIS --------------------------------------------------
label fingerprint_analysis:
# i will copy and paste tutorial stuff

# CODE BELOW IS THE COLLECTION SCENARIO  ---------------------------------------------------------------------------
#
#
# -------------------------------------------------------------------------------------------------------------
label houseoutside:
    scene houseoutside
    $ last_area = ""
    if(got_intro == False):
        show nina normal1
        n "Feel free to peruse the area and bag anything you find suspicious or potentially helpful."
        n "Once you're done return here and we'll head to the lab for analysis."
        hide nina normal1
        $ got_intro = True
    else:
        show nina normal1
        n "Ready to leave?"
        menu:
            "Yes, let's go to the labs":
                hide nina normal1
                jump lab
            "No, I'll look around some more":
                n "Alright, take your time."
                hide nina normal1
                jump house

label house:
    hide screen inventory
    if collected_objs["pill"] == True:
        scene bk_kitchen_nopill
    else: 
        scene kitchen
    $ last_area = "houseoutside"
    show screen kitchenInteractables
    $ button_yes = True
    show screen backButton
    call screen kitchenInteractables

label trashbin:
    hide screen inventory
    hide screen weedbagcollect
    $ last_area = "kitchen"
    $ button_yes = False
    scene trashinside
    $ button_yes = True
    call screen trashInteractables

label countertop:
    hide screen inventory
    hide screen browniecollect
    $ last_area = "kitchen"
    $ button_yes = False
    scene countertop
    $ button_yes = True
    call screen topInteractables

label countertopleft:
    hide screen inventory
    hide screen pillcollect
    $ last_area = "kitchen"
    $ button_yes = False
    scene countertopleft
    $ button_yes = True
    call screen topleftInteractables

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
    "Are you sure you would like to collect this? Doing so prevents you from doing any in field tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory":
            $ collected_objs["brownie"] = True
            "A sample of the brownie has been added to your inventory."
            $ evidence.add_to_inventory(evids["Brownie"])
            $ num_evidence += 1
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
    "Are you sure you would like to collect this? Doing so prevents you from doing any in field tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory":
            $ collected_objs["weedbag"] = True
            "Evidence has been added to your inventory."
            $ evidence.add_to_inventory(evids["Plastic bag"])
            $ num_evidence += 1
            jump expression last_action
        "No":
            jump expression last_action

label pillaction:
    hide screen inventory
    $ button_yes = True
    $ last_area = "countertopleft"
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
                    xalign 0.5
                    yalign 0.25
                    alpha 0.75
            elif uvd.get(click_object) == False:
                show fingerprint1_idle:
                    zoom 0.08
                    xalign 0.5
                    yalign 0.25
                    alpha 0.3
            elif uvd.get(click_object) == True:
                show fingerprint1_white:
                    xalign 0.5
                    yalign 0.25
                    yalign 0.4
            if scalebard.get(click_object) == True:
                show scale:
                    zoom 0.16
                    xalign 0.54
                    yalign 0.25
                    anchor (0.5, 0.5)
                    rotate 280
            if taped.get(click_object) == True:
                show tapepiece:
                    zoom 0.1
                    xalign 0.5
                    yalign 0.25
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
    "Are you sure you would like to collect this? Doing so prevents you from doing any in field tests."
    $ button_yes = False
    menu:
        "Yes - Store in inventory":
            $ collected_objs["pill"] = True
            "Evidence has been added to your inventory."
            $ evidence.add_to_inventory(evids["Pill bottle"])
            $ num_evidence += 1
            jump expression last_action
        "No":
            jump expression last_action
label pillturned:
    $ pill_status += 1
    jump expression last_action

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
        else:
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

label useScaleBar: # (not required to bag evidence)
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
                if click_object == "weedbag":
                    if scalebard[click_object] == True:
                        $ fingerprint_toback = "finger2 S"
                        call sophisticatedFinger
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 2 S"])
                    else:
                        $ fingerprint_toback = "finger2 NS"
                        call sophisticatedFinger
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 2 NS"])
                elif click_object == "pilltop":
                    if scalebard[click_object] == True:
                        $ fingerprint_toback = "finger1 S"
                        call sophisticatedFinger
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 1 S"])
                    else:
                        $ fingerprint_toback = "finger1 NS"
                        call sophisticatedFinger
                        "Evidence added to inventory"
                        $ evidence.add_to_inventory(evids["Fingerprint 1 NS"])
                elif click_object == "pill":
                    "More than half of the print is missing from the tape."
                    "It seems like the textured surface interfered with the sample. This can't be used as evidence now."
                    $ num_evidence -= 1
                $ num_evidence += 1
                jump expression last_action
        else:
            "There's nothing to use this on."
            jump expression last_action
    elif bagging == True:
        "Please select a piece of evidence"
        jump askWhatToBag

label sophisticatedFinger:
    $ sf = True
    scene black
    hide screen weedbagcollect
    hide screen pillcollect
    hide screen browniecollect
    call screen finger_drag
    if("finger2 NS" == fingerprint_toback):
        show finger2_noscale:
            xpos 1000 
            ypos 100
    elif("finger2 S" == fingerprint_toback):
        show finger2_scale:
            xpos 1000 
            ypos 100
    elif("finger1 NS" == fingerprint_toback):
        show finger1_noscale:
            xpos 1000 
            ypos 100
    elif("finger1 S" == fingerprint_toback):
        show finger1_scale:
            xpos 1000 
            ypos 100
    call screen write_drag
    $ sf = False
    return

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
                ypos 100
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
        if(scalebard["pilltop"] == True):
            $ evidence.delete_from_inventory(evids["Fingerprint 1 S"])
        else:
            $ evidence.delete_from_inventory(evids["Fingerprint 1 NS"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!"
        call screen inventory
    else:
        "You need an evidence bag!"
        jump expression last_action
label bagItem2:
    if bagging == True and current_bag_item == "":
        $ current_bag_item = "fingerprint2"
        call screen item_deposit_screen
        if(scalebard["weedbag"] == True):
            $ evidence.delete_from_inventory(evids["Fingerprint 2 S"])
        else:
            $ evidence.delete_from_inventory(evids["Fingerprint 2 NS"])
        call screen inventory
    elif current_bag_item != "":
        "You've already put something in the evidence bag!"
        call screen inventory
    else:
        "You need an evidence bag!"
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
        "You need an evidence bag!"
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
        "You need an evidence bag!"
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
        "You need an evidence bag!"
        jump expression last_action

label useGlove:
    if not put_gloves:
        "You've put gloves on."
        $ put_gloves = True
        jump expression last_action
    else:
        "You already have gloves on!"
        jump expression last_action