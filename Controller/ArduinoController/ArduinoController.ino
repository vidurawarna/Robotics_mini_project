// 6v motor pins
#define m1_pin 3
#define m2_pin 5
#define m3_pin 6

// 5v motor pins
#define m4_pin 9
#define m5_pin 10
#define gripper_pin 11

#define buzzer_pin 12

#define traj_time 2
#define time_step 50
#define motor_speed 30

#include <VarSpeedServo.h>

VarSpeedServo motor1,motor2,motor3,motor4,motor5,gripper;
VarSpeedServo joints[5] = {motor1,motor2,motor3,motor4,gripper};

int angles[5] = {90,90,90,90,90};
int previous_angles[5] = {90,90,90,90,90};
int targets[5] = {0,0,0,0,0};
int speeds[5] = {10,30,30,30,30};

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

//  for(int i=0;i<5;i++){
//      rotateJoint(i,angles[i]);
//      
//    }


//  motor4.slowmove(0);
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


void rotateJoint(int joint_id, int theta){
  int x = previous_angles[joint_id];
  while(x!=theta){
    if(x>theta){
      joints[joint_id].slowmove(--x,motor_speed);
    }
    else if(x<theta){
      joints[joint_id].slowmove(++x,motor_speed);
    }
    delay(20);
  }
  previous_angles[joint_id] = theta;
  delay(10);

}



void trajJointMove(int j){ 
  
  int current_angles[5];
  double t;
  bool changed = false;

  // Set current angles
  for(int i=0;i<j;i++){
    current_angles[i] = previous_angles[i];
  }

  // Set the targets
  for(int i=0;i<5;i++){
    targets[i] = angles[i] - previous_angles[i];
  }

  double start_t = millis();

  for(int i=0;i<5;i++){
    if(angles[i]!=previous_angles[i]){
      changed = true;
    }
  }

  if(changed){
//    joints[0].write(angles[0],speeds[0],false);
    // Start the control loop
    while(((millis()-start_t)/1000)<=traj_time){ 
//      Serial.println(t);
      // Turn each joint at time steps
      for(int i=0;i<j;i++){

        
        
        
        t = (millis() - start_t)/1000;
        
        // Calculate the tragectory function output
        int q = (int)(targets[i]*pow(t/traj_time,2)*(3 - 2*t/traj_time));
  
        // Turn the motor 
          
        joints[i].write(previous_angles[i] + q,speeds[i],false);
        
        // Update current angle
        current_angles[i] = previous_angles[i] + q;  
 
      }
      
      while((millis()-start_t)<=time_step){}
    }
    // Update previous angle list
    for(int i=0;i<j;i++){
      previous_angles[i] = angles[i];
    }
  }
}

// Receive data from Python
void loop() {
  readAngles();

  // rotate angles if data received
//  for(int i=0;i<5;i++){
//     rotateJoint(i,angles[i]);
//  }
  trajJointMove(5);
  //delay(10000);
}
