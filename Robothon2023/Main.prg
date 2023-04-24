Global Integer Xmax, Xmin, Ymax, Ymin, Zmin, xpos, ypos, gap, radius, x, y, z, u, x1, x2, y1, y2
Global String p$

Function Main
	String indata$(0), receive$
  	Integer i, camX, camY, camZ
  	
  	camX = 0
  	camY = 450
  	camZ = 850

	Motor On
	Power High
	Speed 50
	SpeedR 50
	Accel 50, 50
	SpeedS 50
	AccelS 50, 50
	
' going to camera position
  Go Here :X(camX) :Y(camY) :Z(camZ) :U(0) :V(0) :W(180)
  SetNet #201, "192.168.150.2", 2001, CRLF
'  SetNet #201, "127.0.0.1", 2001, CRLF
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
   
   Print #201, "SUCCESS"
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
'Function OpenDoor
'	'gripper open
'	Go Door0
'	Go Door1
'	Go Door2 CP
'	Go Door3 CP
'	Go Door5 CP
'	Go Door6 CP
'	Go Door6 -X(60) CP
'	Go Door4 CP
'	Go Door5
'	Go Door6
'Fend
Function mapping
	Real LocalBBX, LocalBBY, LocalKnobX, LocalKnobY, WorldBBX, WorldBBY, WorldKnobX, WorldKnobY, dZ, dU, dV
	WorldBBX = 102.389
	WorldBBY = 63.257
	WorldKnobX = 214.938
	WorldKnobY = 157.945
	LocalBBX = 149.385
	LocalBBY = 26.285
	LocalKnobX = 166.023
	LocalKnobY = 172.310
	dZ = 600
	dU = 3.174
	dV = -178.16
'	P(440) = XY(149.385, 26.285, 600, 79.302, 3.174, -178.165, 1) ' Blue button local
'	P(441) = XY(166.023, 172.310, 600, 79.302, 3.174, -178.165, 1) ' Door knob local
	P(450) = XY(102.389, 53.257, 600, 79.302, 3.174, -178.165) ' Blue button world
	P(451) = XY(214.938, 157.945, 600, 79.302, 3.174, -178.165) ' Door knob local
	SavePoints "robot1.pts"
	
	Local 1,(BBlocal:WorldBB),(DKlocal:WorldDK)
	
Fend
