 void m1step(int dir);
 void m2step(int dir);
 void m3step(int dir);
 void m4step(int dir);
 void m5step(int dir);
 void m6step(int dir);
 void setup_controller();
//------------------------------------------------------------------------------
// Constants for Motor Control
//------------------------------------------------------------------------------
#define NUM_MOTORS 6

long field_size[2] = {600, 345}; //[mm] (width, height)
long maxY = 90;                 //[mm] max travel distance in y direction
long playerSize = field_size[1] / 3 - maxY; //[35 mm] size of the player

// Parameters for the conversion
const int STEPS_PER_ROTATION = 200;    // Steps per revolution of the motor
const int LINEAR_MOVEMENT_ROTATION = 40; // Movement in mm per revolution for linear motors
const int MAX_STEPS_LINEAR = 450;
const int MAX_STEPS_ANGULAR = 130;  // For 360-degree rotation


// Rotation (M4)
#define M4_STEP 5
#define M4_DIR  4

// Linear (M1)
#define M1_STEP 3
#define M1_DIR  2

// Configuration for Bar 2 (M5 - M2)

// Rotation (M5)
#define M5_STEP 9
#define M5_DIR  8

// Linear (M2)
#define M2_STEP 7
#define M2_DIR  6

// Configuration for Bar 3 (M6 - M3)

// Rotation (M6)
#define M6_STEP 10
#define M6_DIR  12

// Linear (M3)
#define M3_STEP 11
#define M3_DIR  13
 

//------------------------------------------------------------------------------
// Method Declaration for Motor Control
//------------------------------------------------------------------------------

void m1step(int dir) {
    digitalWrite(M1_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M1_STEP, HIGH);
    delayMicroseconds(400);
    digitalWrite(M1_STEP, LOW);
    delayMicroseconds(400);
}

void m2step(int dir) {
    digitalWrite(M2_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M2_STEP, HIGH);
    delayMicroseconds(400);
    digitalWrite(M2_STEP, LOW);
    delayMicroseconds(400);
}

void m3step(int dir) {
    digitalWrite(M3_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M3_STEP, HIGH);
    delayMicroseconds(400);
    digitalWrite(M3_STEP, LOW);
    delayMicroseconds(400);
}

void m4step(int dir) {
    digitalWrite(M4_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M4_STEP, HIGH);
    delayMicroseconds(500);
    digitalWrite(M4_STEP, LOW);
    delayMicroseconds(500);
}

void m5step(int dir) {
    digitalWrite(M5_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M5_STEP, HIGH);
    delayMicroseconds(500);
    digitalWrite(M5_STEP, LOW);
    delayMicroseconds(500);
}

void m6step(int dir) {
    digitalWrite(M6_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M6_STEP, HIGH);
    delayMicroseconds(500);
    digitalWrite(M6_STEP, LOW);
    delayMicroseconds(500);
}

void setup_controller() {
    pinMode(M1_STEP, OUTPUT);
    pinMode(M1_DIR, OUTPUT);

    pinMode(M2_STEP, OUTPUT);
    pinMode(M2_DIR, OUTPUT);

    pinMode(M3_STEP, OUTPUT);
    pinMode(M3_DIR, OUTPUT);

    pinMode(M4_STEP, OUTPUT);
    pinMode(M4_DIR, OUTPUT);

    pinMode(M5_STEP, OUTPUT);
    pinMode(M5_DIR, OUTPUT);

    pinMode(M6_STEP, OUTPUT);
    pinMode(M6_DIR, OUTPUT);
}

    //------------------------------------------------------------------------------
    // global variables
    //------------------------------------------------------------------------------
    long currentPos[NUM_MOTORS] = {0, 0, 0, 0, 0, 0};
    long targetPos[NUM_MOTORS] = {0, 0, 0, 0, 0, 0};

    //------------------------------------------------------------------------------
    // helper functions
    //------------------------------------------------------------------------------

    void array_copy(long *src, long *dst, int length) {
        for (int i = 0; i < length; i++) {
            dst[i] = src[i];
        }
    }

    long dist2pos(long distance) {
        return (STEPS_PER_ROTATION * distance) / LINEAR_MOVEMENT_ROTATION;
    }

    long ang2pos(long angle) {
        return (STEPS_PER_ROTATION * angle) / 360;
    }

    long pos2dist(long position) {
        return position * LINEAR_MOVEMENT_ROTATION / STEPS_PER_ROTATION;
    }

    long pos2ang(long position) {
        return (position) * 360 / STEPS_PER_ROTATION;
    }

    
    void defaultDefens(int y_cordinate){
      int rotationReset = 90;
      int targetPosition = calculateYPositionInSector(y_cordinate);

      for (int i = 0; i < 3; ++i) {
          targetPos[i] = targetPosition;
      }
      
      for (int i = 3; i < 6; ++i) {
          targetPos[i] = rotationReset;
      }
      
      updateMotors();
    }

    long calculateYPositionInSector(long Ycordinate) {
        long sectorRelativeY = Ycordinate % (field_size[1] / 3);
        long position = sectorRelativeY - playerSize / 2;
        position = constrain(position, 0, maxY);
        return position;
    }

    void stepMotor(int motor, long steps, int dir) {
        for (long i = 0; i < steps; i++) {
            switch (motor) {
                case 0: m1step(dir); break;
                case 1: m2step(dir); break;
                case 2: m3step(dir); break;
                case 3: m4step(dir); break;
                case 4: m5step(dir); break;
                case 5: m6step(dir); break;
            }
        }
    }

    void setLinearMotorPosition(int motorIndex) {
        long currentPosition = currentPos[motorIndex];
        long targetPosition = targetPos[motorIndex];
        
        long steps = dist2pos(abs(targetPosition - currentPosition));
        int direction =  (targetPosition > currentPosition) ? 0 : 1; // 0 = forward, 1 = backward

        if (steps > 0) { 
           stepMotor(motorIndex, steps, direction);
           currentPos[motorIndex] = targetPos[motorIndex];
        }
    }

     void setRotationMotorPosition(int motorIndex) {
        long currentPosition = currentPos[motorIndex];
        long targetPosition = targetPos[motorIndex];

        long steps =  ang2pos(abs(targetPosition - currentPosition));
        int direction =  (targetPosition > currentPosition) ? 0 : 1; // 0 = forward, 1 = backward

        if (steps > 0) {    
           stepMotor(motorIndex, steps, direction);
           currentPos[motorIndex] = targetPos[motorIndex];
        }
    }

    void updateMotors() {
      for (int i = 0; i < NUM_MOTORS; i++) {
        if (i <= 2){
            setLinearMotorPosition(i);
          }
        else{
            setRotationMotorPosition(i);
        }
      }
    }

    void updateMotor(int motorIndex, long position) {
        targetPos[motorIndex] = position;
        if (motorIndex <= 2){
            setLinearMotorPosition(motorIndex);
        }
        else {
            setRotationMotorPosition(motorIndex);
        }
    }

    //------------------------------------------------------------------------------
    // main functions
    //------------------------------------------------------------------------------


    void moveLinearMotor1(long position){
      updateMotor(0, position);
    }

    void moveLinearMotor2(long position){
      updateMotor(1, position);
    }
    void moveLinearMotor3(long position){
      updateMotor(2, position);
    }

    void moveRotationMotor1(long position)
    {
      updateMotor(3, position);
    }

    void moveRotationMotor2(long position)
    {
      updateMotor(4, position);
    }

     void moveRotationMotor3(long position)
    {
      updateMotor(5, position);
    }

    void offensRow1(long position){

      moveRotationMotor2(10);
      moveRotationMotor3(10);

      moveLinearMotor1(position);
      kick(3);
    }


    void offensRow2(long position){
       moveRotationMotor3(10);

      moveLinearMotor2(position);
      kick(4);
    }

    void offensRow3(long position){
      moveLinearMotor2(position);
      kick(5);
    }

    void defensRow1(long position) {
      moveRotationMotor1(90);
      moveLinearMotor1(position);
    }

    void defensRow2(long position){
      moveRotationMotor2(90);
      moveLinearMotor2(position);
      defensRow1(position);
    }

    void defensRow3(long position){
      moveRotationMotor3(90);
      moveLinearMotor3(position);
      defensRow2(position);
    }
    

    void kick(int motor_index) {
            updateMotor(motor_index, 45);

            updateMotor(motor_index, 135);

            updateMotor(motor_index, 90);
      }

    void command(long ballPositionX, long ballPositionY) {
        int targetPosition = calculateYPositionInSector(ballPositionY);
        
        if (ballPositionX >= 30 && ballPositionX <= 110){
         offensRow1(ballPositionY);
        }
        else if (ballPositionX >= 111 && ballPositionX <= 209){
         defensRow1(ballPositionY);
        }
        else if (ballPositionX >= 210 && ballPositionX <= 290){
         offensRow2(ballPositionY);
        }
        else if (ballPositionX >= 291 && ballPositionX <= 400){
          defensRow2(ballPositionY);
        }
        else if (ballPositionX >= 401 && ballPositionX <= 480){
          offensRow3(ballPositionY);
        }
        else if (ballPositionX >= 481 && ballPositionX <= 580){
          defensRow3(ballPositionY);
        }
        else {
          defaultDefens(ballPositionY);
        }
    }
   
    //------------------------------------------------------------------------------
    // Arduino functions
    //------------------------------------------------------------------------------

    void setup() {
        Serial.begin(9600);
        setup_controller();

        long initialPos[NUM_MOTORS] = {0, 0, 0, 90, 90, 90};
        array_copy(initialPos, targetPos, NUM_MOTORS);
        updateMotors();
       
    }

    void loop() {
        if (Serial.available()) {
            String data = Serial.readStringUntil('\n');
            int commaIndex = data.indexOf(',');
            if (commaIndex != -1) {
                String xString = data.substring(0, commaIndex);
                String yString = data.substring(commaIndex + 1);

                int x = xString.toInt();
                int y = yString.toInt();

                command(x, y);
            }
        }
     }


    //------------------------------------------------------------------------------
    // Simulator Test Loop
    //------------------------------------------------------------------------------
     
    
        //  void loop() {
        //     delay(5000);
        //     Serial.println("======150/300======");
        //     command2(150,300);
        //     delay(5000);
        //     Serial.println("======450/160======");            
        //     command2(260,160);
        //     delay(5000);
        //     Serial.println("======150/300======");
        //     command2(260,300);
        //     Serial.println("======Done======");
        //     delay(20000);
        //     return;
        // }
           
     


