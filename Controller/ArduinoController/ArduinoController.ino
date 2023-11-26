int angles[4] = {0,0,0,0};
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
}
void readAngles(){
  while (Serial.available()) {
    int i=0;
    String data_string = Serial.readStringUntil(',');

    // Convert the string to a float
    float data_value = data_string.toInt();
    angles[i++] = data_value;
    Serial.print(angles[i-1]);
    Serial.print(" ");
  }  
}
// Receive data from Python
void loop() {
  readAngles();
  delay(10);
}
