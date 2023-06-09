Global Integer Xmax, Xmin, Ymax, Ymin, Zmin, xpos, ypos, gap, radius, x, y, z, u, x1, x2, y1, y2
Global String p$, px1$, px2$, py1$, py2$

Function main
	String indata$(0), receive$
  	Integer i, camX, camY, camZ

	Motor On
	Power High
	Speed 20
	SpeedR 20
	Accel 20, 20
	AccelR 20, 20
	SpeedS 20
	AccelS 20, 20
	AutoLJM On
	
' going to camera position
  Go Camera_Pos

'  SetNet #201, "192.168.150.2", 2001, CRLF
  SetNet #201, "127.0.0.1", 2001, CRLF
  OpenNet #201 As Server
  Print "Robot ready, listening to network"
  WaitNet #201
  OnErr GoTo ehandle

  Do
   Input #201, receive$
   ParseStr receive$, indata$(), " " ' convert to lower case
   Print "Received message: ", receive$
   
  
   ' if the command is jump3
   If indata$(0) = "jump3" Then
     	x = Val(Trim$(indata$(1)))
    	y = Val(Trim$(indata$(2)))
	    z = Val(indata$(3))
	    u = Val(indata$(4))
    
   		Print "Jumping to x=", x, " y=", y, " z=", z
	   	Jump3 Here +Z(50), Here :X(0) :Y(y) :Z(z + 50), Here :X(x) :Y(y) :Z(z) :U(u)
   EndIf
   
   If LCase$(indata$(0)) = "go" Then
     	x = Val(Trim$(indata$(1)))
    	y = Val(Trim$(indata$(2)))
	    z = Val(indata$(3))
    
   		Print "Going to x=", x, " y=", y, " z=", z
	   	Go Here :X(x) :Y(y) :Z(z)
   EndIf
   
   If LCase$(indata$(0)) = "m" Then
     	p$ = Trim$(indata$(1))
    
   		Print "Going to ", p$
	   	Go P(PNumber(p$))
   EndIf
   
   If LCase$(indata$(0)) = "p" Then
   		P333 = Here
   		Print "Current location is ", P333
	   	Print #201, P333
   EndIf
   
   If LCase$(indata$(0)) = "local" Then ' map to local coordinate
   		Real px1, py1, px2, py2
     	px1 = Val(Trim$(indata$(1)))
        py1 = Val(Trim$(indata$(2)))
        px2 = Val(Trim$(indata$(3)))
        py2 = Val(Trim$(indata$(4)))
        
   		Print "Mapping world coordinate to local"
   		Print "Blue button:", px1, ",", py1, "  Knob:", px2, ",", px2
		Real ZOffset
		ZOffset = 522
		P332 = Here :X(px1) :Y(py1) :Z(ZOffset) ' blue	
		P333 = Here :X(px2) :Y(py2) :Z(ZOffset) ' knob
		Local 3,(LBB:P332),(LK:P333) ' map those points to Local BB and Local Knob at z=521
		Power High
		Speed 20
		SpeedR 20
		Accel 20, 20
		AccelR 20, 20
		SpeedS 20
		AccelS 20, 20
   EndIf
   
 
	' --------- tasks -------
	If LCase$(indata$(0)) = "go_click_m5" Then
   		go_click_m5
   	EndIf
   	
	If LCase$(indata$(0)) = "go_press_blue_button" Then
		Speed 50
   		go_press_blue_button
   	EndIf

   	
	If LCase$(indata$(0)) = "go_approach_slider" Then
		Speed 15
		Real starting_pos
		starting_pos = Val(Trim$(indata$(1)))
   		go_approach_slider(starting_pos)
   	EndIf
   	
	If LCase$(indata$(0)) = "go_check_display" Then
		Speed 50
   		go_check_display
   	EndIf
   	
	If LCase$(indata$(0)) = "go_slide" Then
		Speed 20
		Real mm
		mm = Val(Trim$(indata$(1)))
   		go_slide(mm)
   	EndIf
   	
 	If LCase$(indata$(0)) = "go_tool_up" Then
   		go_tool_up
   	EndIf

   	If LCase$(indata$(0)) = "go_approach_plug1" Then
   		go_approach_plug1
   	EndIf
   	
   	If LCase$(indata$(0)) = "go_approach_plug2" Then
   		go_approach_plug2
   	EndIf
   	
   	If LCase$(indata$(0)) = "go_approach_plug3" Then
   		go_approach_plug3
   	EndIf
   	
	If LCase$(indata$(0)) = "go_open_door" Then
   		go_open_door
   	EndIf
   	
	If LCase$(indata$(0)) = "go_probe1" Then
   		go_probe1
   	EndIf
   	
	If LCase$(indata$(0)) = "go_probe2" Then
   		go_probe2
   	EndIf
   	
	If LCase$(indata$(0)) = "go_probedrop" Then
   		go_probedrop
   	EndIf
   	   	
   	If LCase$(indata$(0)) = "go_approach_cable" Then
   		go_approach_cable
   	EndIf

   	If LCase$(indata$(0)) = "go_wind_cable" Then
   		go_wind_cable
   	EndIf

	If LCase$(indata$(0)) = "go_catch_probe" Then
   		go_catch_probe
   	EndIf
   	
	If LCase$(indata$(0)) = "go_stow" Then
   		go_stow
   	EndIf

	If LCase$(indata$(0)) = "go_stow_finished" Then
   		go_stow_finished
   	EndIf
   	
	If LCase$(indata$(0)) = "go_press_red_button" Then
   		go_press_red_button
   	EndIf
	' --------- end tasks -------
   
    ' ---- demo ---
 	If LCase$(indata$(0)) = "approaching_meter" Then
   		approaching_meter
   	EndIf
 	If LCase$(indata$(0)) = "turn_meter" Then
   		turn_meter
   	EndIf
 	If LCase$(indata$(0)) = "approaching_probe" Then
   		approaching_probe
   	EndIf
 	If LCase$(indata$(0)) = "probing" Then
   		probing
   	EndIf
 	If LCase$(indata$(0)) = "probe_done" Then
   		probe_done
   	EndIf
   	
   
	P777 = Here
	Print #201, P777
	
  Loop

  Exit Function

  ehandle:
	Call ErrFunc
    EResume Next
Fend
Function ErrFunc

  Print ErrMsg$(Err(0))
  Select Err(0)
   Case 2902
     OpenNet #201 As Server
     WaitNet #201

   Case 2910
     OpenNet #201 As Server

     WaitNet #201

   Default
     Error Err(0)

  Send
Fend

Function drawCircle
	Arc3 Here -X(radius), Here -X(radius) +Y(radius) CP
	Arc3 Here +X(radius), Here +X(radius) -Y(radius) CP
Fend

Function go_click_m5
	Speed 60
	Go Approach_M5
	Speed 20
	Go Click_M5
	Wait (0.2)
	Go Approach_M5
Fend
Function go_press_buttons
	Go Approach_Button
	Go Press_Blue
	Wait (0.5)
	Go Approach_Button
	Go Press_Red
	Wait (0.5)
	Go Approach_Button
Fend
Function go_press_blue_button
	Go Approach_Button
	Go Press_Blue
	Wait (0.2)
	Go Approach_Button
Fend
Function go_open_door
	Power High
	AutoLJM On
	Speed 60
	Go Approach_Door_OrginalPos
	Speed 50
	Go Door_Orginal_Pick
	Go DOor_Open1 CP
	Go Door_Open2 CP
	Go Door_Open3 CP
	Go Door_Open4 CP
	Go Door_Open5 CP
	Go Door_Open6 CP
	Go Door_Open7 CP
	Go Door_Open8 CP
	Go Door_Finished
	Speed 30
Fend
Function go_probe1
	AutoLJM On
	' make sure gripper is open g0
	Go Approach_probe
	Go Probe_Pick0
	' close the gripper here
Fend
Function go_probe2
	AutoLJM On
	Go probe_pick1
	Go probe_pick2
	Go probe_pick3
	Go probe_pick4
	Go probe_pick5
	Wait (2)
	Go probe_pick6
	Wait (1)
	Go Probe_Pick5
	Go probe_pick3
	Go probe_place1
	Go probe_place2
	Go Probe_Place3A
	Go probe_place3
Fend
Function go_probedrop
	' make sure gripper is open g50
	Go probe_place3A  ' slightly above probe_place3
	Go Probe_Place4
Fend
Function go_approach_plug1
	Speed 20
    Go Approach_Plug_orginalPos
	Go Plug_OrginalPos
	'Close the Gripper	
Fend
Function go_approach_plug2
	Go Unplug_OrginalPos
	Go Plug_and_cable1
	Go Approach_Plug_DestinationPos
	Go Plug_DestinationPos
	' no need this anymore Go Plug_DestinationTurn
	' Open the Gripper
Fend
Function go_approach_plug3
	Go Plug_FinishedUp
Fend
	
Function go_approach_cable
	' must open g50
	Go Approach_Cable
	Go Approach_Grabbing_Cable
	' should close after
Fend
Function go_wind_cable
	' gripper should be closed 100
	Speed 5
	Go Cable1
	Go Cable2
	Go Cable3
	Go Cable4
	Go Cable5
	Go Cable6
	Go Cable7
	' open g70 from here and continue with catch probe
Fend

Function go_catch_probe
	Speed 40
	' open gripper 0
	Go cable_finished
	Go Catching_Probe1
	Go Probe_Place3A
	Go catching_probe2
	Go catching_probe2a ' Z down
	' close g100 here and continue with stow
Fend
Function go_stow
	Speed 20
	' make sure gripper is closed g100
	Go Catching_Probe2 ' Z up
	Go Catching_Probe3
	Go Catching_Probe4
	
	Go Stow1
	Go Stow2
	Go Stow3
	Go Stow4
	Wait (1)
	Go Stow5
	Wait (1)
Fend
Function go_stow_finished
	' make sure gripper is open g50
	Speed 20
	Go Stow_Finished
Fend
Function go_press_red_button
	' make sure gripper is closed g80
	Speed 60
	Go Approach_Button
	Go Press_Red
	Wait (0.5)
	Go Approach_Button
Fend
Function go_slide(distance As Real)
	Speed 20
	Real d
	If distance >= 2 And distance <= 28 Then
		For d = distance - 0.5 To distance + 1.6 Step 0.2
			Go Slider_StartPos +X(d) :Z(-2.49) CP
			Wait (0.3)
		Next
		Wait (0.5)
		Go Slider_StartPos +X(d) :Z(-2.49)
	EndIf
Fend
Function go_check_display
'	Go Display_Pic
	Go Display_Pic2
	
Fend
Function go_approach_slider(StartPoint As Real)
	' make sure gripper is open
	If StartPoint >= 0 And StartPoint < 31 Then
		Go Approach_Slider +X(StartPoint)
		Wait (0.5)
        Go Approach_Slider +X(StartPoint) -Z(29)
	EndIf
Fend
Function go_tool_up
	' make sure the gripper is open 
		Go Here +Z(26.5)
Fend
Function approaching_meter
	Go start
	Go approach_meter
	Go meter_down
Fend

Function turn_meter
	' g70
	Go meter_on
Fend

Function approaching_probe
	' g0
	Go meter_on_up
	Go probe_approach
	Go probe_pick
Fend

Function probing
	' g100
	Go probe_up
	Go point_approach
	Go point_approach2
	Go point_touch
	Wait (2)
	Go point_approach2
	Go point_approach
	Go probe_up
	Go probe_pick
Fend

Function probe_done
	' g0
	Go probe_up
Fend


