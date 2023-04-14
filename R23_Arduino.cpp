// Robothon 2023 Team RobotechX MDX
// by Judhi Prasetyo 06/04/2023
// This is the code for controlling the gripper and getting distance from LIDAR
// expecting command from Python: G0/G50/G100 for gripper opening percentage
// Serial speed to PC is 9600, CR/LF does not matter

#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

String msg;
uint16_t dist;

int minAngle = 0;   // gripper fully open
int maxAngle = 180;  // gripper fully closed

Servo myservo;

void setup() {
  myservo.attach(9, 500, 2500);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("Middlesex");
  lcd.setCursor(2, 1);
  lcd.print("University");
  delay(2000);
    lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("Robothon");
  lcd.setCursor(7, 1);
  lcd.print("2023");
  delay(2000);
  lcd.clear();
  delay(4000);
  Serial.begin(9600);
  // check the servo opening & closing
  myservo.write(maxAngle);
  Serial.println("Fully closed");
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Fully closed");
  delay(1000);
  myservo.write(minAngle);
  Serial.println("Gripper fully opened");
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Fully opened");
  Serial.println("Ready, enter command (eg: 'G0/G50/G100')");  // case insensitive
}

void loop() {
  // put your main code here, to run repeatedly:

  while (Serial.available()) {
    msg = "Invalid command";
    String command = Serial.readString();
    command.trim();         // get rid of extra spaces or CR/LF if there's any
    command.toLowerCase();  // always convert to lowercase (case insensitive)

    if (command == "gripper 0" || command == "g0") {  // fully open
      myservo.write(0);
      msg = "Fully opened";
    }
    if (command == "gripper 50" || command == "g50") {
      myservo.write(90);
      msg = "Half opened";
    }
    if (command == "gripper 100" || command == "g100") {
      myservo.write(165);
      msg = "Fully closed";
    }
    Serial.println(msg);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(msg);
  }
  delay(10);
}