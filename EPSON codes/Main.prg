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
	SpeedS 20
	AccelS 20, 20
	
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
   
   ' Mapping from world coordinate to local
   If indata$(0) = "C" Then
     	x1 = Val(Trim$(indata$(1)))
    	y1 = Val(Trim$(indata$(2)))
     	x2 = Val(Trim$(indata$(3)))
    	y2 = Val(Trim$(indata$(4)))
   		Print "Mapping"
   	    
		' mapping code here   		
		P111 = XY(100, 100, 100, 0) ' warning: mock up data
		P112 = XY(200, 200, 100, 0) ' ====
		P211 = XY(0, 0, 0, 0)
		P212 = XY(300, 300, 300, 0)
        Local 1,(P111:P211),(P112:P212)
		
   EndIf
   
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
   
   If LCase$(indata$(0)) = "c" Then
     	px1$ = Trim$(indata$(1))
        py1$ = Trim$(indata$(2))
        px1$ = Trim$(indata$(3))
        py1$ = Trim$(indata$(4))
        
   		Print "Mapping local coordinate to: ", px1$, ",", py1$
   		'Local 1,(blue_point:Door_Orginal_Pick),(door_point:Home_Pos)
   		'Local 1, (blue_point : int(py$))), (door_point : here :x(int(px2$)) :y(int(py2$)))
	   	Go P(PNumber(p$))
   EndIf
   
   If LCase$(indata$(0)) = "click_m5" Then
   		go_click_m5
   	EndIf
   
	P333 = Here
	Print #201, P333
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
Function mapping
	Real WorldBBX, WorldBBY, WorldKnobX, WorldKnobY
'	Real LocalBBX, LocalBBY, LocalKnobX, LocalKnobY, WorldBBX, WorldBBY, WorldKnobX, WorldKnobY, dZ, dU, dV
'	WorldBBX = -533
'	WorldBBY = 289
'	WorldKnobX = -535
'	WorldKnobY = 137
'	LocalBBX = 149.385
'	LocalBBY = 26.285
'	LocalKnobX = 166.023
'	LocalKnobY = 172.310
'
'	dZ = 600
'	dU = 3.174
'	dV = -178.16
''	P(440) = XY(149.385, 26.285, 600, 79.302, 3.174, -178.165, 1) ' Blue button local
''	P(441) = XY(166.023, 172.310, 600, 79.302, 3.174, -178.165, 1) ' Door knob local
'	P(450) = XY(102.389, 53.257, 600, 79.302, 3.174, -178.165) ' Blue button world
'	P(451) = XY(214.938, 157.945, 600, 79.302, 3.174, -178.165) ' Door knob local
'	SavePoints "robot1.pts"

'	P330 = XY(-553.833, 281.953, 524.696, -90)
'	P331 = XY(-535.787, 137.820, 534.730, -90)
'	P332 = Here :X(-553.833) :Y(280.155)
'	P333 = Here :X(-535.094) :Y(137.820)
	P332 = Here :X(-404.57) :Y(306.76) :Z(521) ' blue
	P333 = Here :X(-505.9) :Y(204.18) :Z(521) ' knob
	'Local 3,(P330:P332),(P331:P333)
	Local 3,(LBB:P332),(LK:P333)
	
Fend
Function go_click_m5
	Go Approach_M5
	Go Click_M5
	Wait (0.5)
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
	Wait (0.5)
	Go Approach_Button
Fend

Function go_open_door
	Go Approach_Door_OrginalPos
	Go Door_Orginal_Pick
	Go Door_Open1
	Go Door_Open2 CP
	Go Door_Open3 CP
	Go Door_Open4 CP
	Go Door_Open5 CP
	Go Door_Open6
	Go Door_Open7 CP
	Go Door_Open8
Fend
Function go_probe1
	' make sure gripper is open g0
	Go Approach_probe
	Go Probe_Pick0
	' close the gripper here
Fend
Function go_probe2
	Go probe_pick1
	Go probe_pick2
	Go probe_pick3
	Go probe_pick4
	Go probe_pick5
	Wait (2)
	Go probe_pick6
	Wait (1)
	Go Probe_Pick7
	Go probe_pick4
	Go probe_place1
	Go probe_place2
	Go probe_place3
Fend
Function go_probe_drop
	Go probe_place1
	Go probe_place2
	Go probe_place3
Fend
Function go_approach_plug1
    Go Approach_Plug_orginalPos
	Go Plug_OrginalPos
	'Close the Gripper
	
Fend
Function go_approach_plug2
	Go Unplug_OrginalPos
	Go Approach_Plug_DestinationPos
	Go Plug_DestinationPos
	Go Plug_DestinationTurn
	' Open the Gripper
Fend
Function go_approach_plug3
	Go Plug_FinishedUp
Fend
	
Function go_approach_cable
	' must open g50
	Go Approach_Cable
	Go Approach_Grabbing_Cable
Fend
Function go_wind_cable
	Go Cable1
	Go Cable2
	Go Cable3
	Go Cable4
	Go Cable5
	Go Cable6
	Go Cable7
	Go Cable8
	Go Cable9
	Go Cable10
	Go Cable11
	Go Cable12
	Go Cable4
	Go Cable5
	Go Cable6
	Go Cable7
	Go Cable8
	Go Cable9
	Go Cable10
	Go Cable11
	'Go Cable12
	'Go Cable4
	'Go Cable5
	'Go Cable6
	'Go Cable7
	'Go AlignProbe1
	'Go AlignProbe2
	'Go AlignProbe3
	' open g70 from here and continue with catch probe
Fend
Function go_catch_probe
	Go CatchProbe1
	Go CatchProbe2
	' close g80 here and continue with stow
Fend
Function go_stow
	Go Stow1
	Go Stow2
	Go Stow3
	Go Stow4
	Go Stow5
	'Go Stow6
	'Wait (1)
	'Go Stow7
	' open g0
Fend
Function go_press_red_button
	' make sure gripper is closed g80
	Go Stow_Finished
	Go Approach_Button
	Go Press_Red
	Wait (0.5)
	Go Approach_Button
Fend
Function slide(distance As Int32)
	Go Here +X(distance)
Fend
	


