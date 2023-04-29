# List of task functions
# ======================
# go_click_m5
# go_press_blue_button
# go_check_display
# go_slide(mm)
# go_approach_plug1
# go_approach_plug2
# go_approach_plug3
# go_open_door
# go_probe_1
# go_probe_2
# go_probe_drop
# go_approach_cable
# go_wind_cable
# go_catch_probe
# go_stow
# go_press_red_button

from Robothon2023.SendToEpson import sendToEpson


######################
# Step-1 : Connect to Robot, connect to Servo, Open camera

# Step-2: Capture image and get world coordinate of BlueButton and Knob (loop)

# Step-2 : if good, send coordinates to Robot for local mapping sendEpson("t BBX BBY KX KY")

# Step-3 : go_click_m5
sendToEpson("go_click_m5")
# Step-4 : go_press_blue_button
sendToEpson("go_press_blue_button")
# Step-5 : go_check_display
sendToEpson("go_check_display")
# Step-6 : take the first target
ret, image = vid.read()
target = getTarget(image,0)
sendToEpson("")