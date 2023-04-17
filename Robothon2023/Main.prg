Global Integer Xmax, Xmin, Ymax, Ymin, Zmin, xpos, ypos, gap, radius, x, y, z, u, x1, x2, y1, y2

Function main
	String indata$(0), receive$
  	Integer i, camX, camY, camZ
  	
  	camX = 0
  	camY = 450
  	camZ = 850

	Motor On
	Power Low
	Speed 50
	SpeedR 50
	Accel 50, 50
	SpeedS 50
	AccelS 50, 50
	
' going to camera position
  Go Here :X(camX) :Y(camY) :Z(camZ) :U(0) :V(0) :W(180)

'  SetNet #201, "192.168.150.2", 2001, CRLF
  SetNet #201, "127.0.0.1", 2001, CRLF
  OpenNet #201 As Server
  Print "Robot ready, listening to network"
  WaitNet #201
  OnErr GoTo ehandle

  Do
   Input #201, receive$
   ParseStr LCase$(receive$), indata$(), " "
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
   
   If indata$(0) = "jump3" Then
     	x = Val(Trim$(indata$(1)))
    	y = Val(Trim$(indata$(2)))
	    z = Val(indata$(3))
	    u = Val(indata$(4))
    
   		Print "Jumping to x=", x, " y=", y, " z=", z
	   	Jump3 Here +Z(50), Here :X(0) :Y(y) :Z(z + 50), Here :X(x) :Y(y) :Z(z) :U(u)
   EndIf
   
   If indata$(0) = "go" Then
     	x = Val(Trim$(indata$(1)))
    	y = Val(Trim$(indata$(2)))
	    z = Val(indata$(3))
    
   		Print "Going to x=", x, " y=", y, " z=", z
	   	Go Here :X(x) :Y(y) :Z(z)
   EndIf
   
'   If indata$(0) = "M" Then
'     	p$ = Trim$(indata$(1))
'    
'   		Print "Going to ", p$
'	   	Go p$
'   EndIf
   
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

Function calibrate
	Motor On
	Power Low
	Speed 50
	SpeedR 50
	Accel 50, 50
	SpeedS 50
	AccelS 50, 50
	
	Xmax = 200
	Xmin = -200
	Ymax = 780
	Ymin = 380
	Zmin = 473.5
	radius = 25
	
	gap = 50
	
'	Move Here :X(Xmin) :Y(Ymin) :Z(Zmin)
'	Move Here :X(Xmin) :Y(Ymax) :Z(Zmin)
'	Move Here :X(Xmax) :Y(Ymax) :Z(Zmin)
'	Move Here :X(Xmax) :Y(Ymin) :Z(Zmin)
'	Move Here :X(Xmin) :Y(Ymin) :Z(Zmin)
'	
	For ypos = Ymin To Ymax Step gap
    	For xpos = Xmin To Xmax Step gap
        	Print "x:(", Trim$(Str$(xpos)), ") y:(", Trim$(Str$(ypos)), ")"
			Jump3 Here +Z(50), Here :X(xpos) :Y(ypos) :Z(Zmin + 50), Here :X(xpos) :Y(ypos) :Z(Zmin)
			'drawCircle
		Next
	Next
Fend
Function drawCircle
	Arc3 Here -X(radius), Here -X(radius) +Y(radius) CP
	Arc3 Here +X(radius), Here +X(radius) -Y(radius) CP
Fend

