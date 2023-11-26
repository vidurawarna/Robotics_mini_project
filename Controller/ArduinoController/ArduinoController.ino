// 6v motor pins
#define m1_pin 3
#define m2_pin 5
#define m3_pin 6

// 5v motor pins
#define m4_pin 9
#define m5_pin 10
#define gripper_pin 11

#define buzzer_pin 12

#include <Servo.h>

Servo motor1,motor2,motor3,motor4,motor5,gripper;
Servo joints[5] = {motor1,motor2,motor3,motor4,gripper};

int angles[5] = {0,90,90,0,20};
int previous_angles[5] = {0,90,90,0,20};

bool receieved_data = false;
/*
 +---------+-------+-------+
 |Angle    | Min   | Max   |
 +---------+-------+-------+
 |angles[0]| 0     | 180   |
 +---------+-------+-------+
 |angles[1]| 0     | 180   |
 +---------+-------+-------+
 |angles[2]| -135  | 0     |
 +---------+-------+-------+
 |angles[3]| -90   | 90    |
 +---------+-------+-------+
*/

void setup() {
  Serial.begin(9600);
  delay(500);
  pinMode(buzzer_pin,OUTPUT);
  
  motor1.attach(m1_pin);
  motor2.attach(m2_pin);
  motor3.attach(m3_pin);
  motor4.attach(m4_pin);
  motor5.attach(m5_pin);
  gripper.attach(gripper_pin);

  for(int i=0;i<5;i++){
      rotateJoint(i,angles[i]);
      
    }


//  motor4.write(0);
  beep(2);  
}

void beep(int t){
  for(int i=0;i<t;i++){
    tone(buzzer_pin,1000);
    delay(100);
    noTone(buzzer_pin);
    delay(100);
  } 
}

void readAngles(){
  if(Serial.available()>0){
    String data = Serial.readStringUntil('\n');

    // Parse the data using strtok function
    char *ptr = strtok(const_cast<char *>(data.c_str()), ",");

    // Loop through the tokens and convert them to integers
    for (int i = 0; i < 5 && ptr != NULL; i++){
      angles[i] = atoi(ptr);
      ptr = strtok(NULL,",");
   }
  }
}

//void readAngles(){
//  int i=0;
//  while (Serial.available()) {
//    receieved_data = true;
//    
//    String data_string = Serial.readString();
//    if(data_string=="A"){
//      continue;
//    }
//    else if (data_string=="Z"){
//      break;
//    }
//    else{
//      float data_value = data_string.toInt();
//      angles[i++] = data_value;
//      if(i==4){break;}
//    }
//
//    Serial.print(angles[i-1]);
//    Serial.print(" ");
////    delay(10);
//  }  
// 
//}

void rotateJoint(int joint_id, int theta){
  int x = previous_angles[joint_id];
  while(x!=theta){
    if(x>theta){
      joints[joint_id].write(--x);
    }
    else if(x<theta){
      joints[joint_id].write(++x);
    }
    delay(20);
  }
  previous_angles[joint_id] = theta;
  delay(10);

}

// Receive data from Python
void loop() {
  readAngles();

  // rotate angles if data received
  for(int i=0;i<5;i++){
     rotateJoint(i,angles[i]);
  }

}
