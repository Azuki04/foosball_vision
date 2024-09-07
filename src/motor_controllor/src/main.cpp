#include <Arduino.h>
#include <config.h>

// Motor configuration
#define NUM_MOTORS 6
#define STEPS_PER_ROTATION 200
#define LINEAR_MOVEMENT_ROTATION 40
#define MAX_LINEAR_DISTANCE 80 // Maximum linear distance in mm
#define MAX_STEPS_LINEAR (STEPS_PER_ROTATION * MAX_LINEAR_DISTANCE / LINEAR_MOVEMENT_ROTATION) // Maximum steps for linear movement
#define MAX_STEPS_ANGULAR (STEPS_PER_ROTATION) // Assuming 360 degrees is maximum for angular motors

class MotorControl {
  private:
    long pos[NUM_MOTORS];            // Current positions of the motors
    long target_pos[NUM_MOTORS];     // Target positions of the motors
    uint8_t kick_motors;             // Motors involved in the kick action
    long field_size[2];
    long max_y;
    long player_size;

    // setup controller
    long reset_pos[NUM_MOTORS];
    long reset_pos2[NUM_MOTORS];

    // Utility functions
    long ang2pos(long angle) {
      long pos = STEPS_PER_ROTATION * (angle) / 360;
      Serial.print("Angle: "); Serial.print(angle); Serial.print(" -> Position: "); Serial.println(pos);
      return constrain(pos, 0, MAX_STEPS_ANGULAR);
    }

    long dist2pos(long distance) {
      long pos = STEPS_PER_ROTATION * distance / LINEAR_MOVEMENT_ROTATION;
      Serial.print("Distance: "); Serial.print(distance); Serial.print(" -> Position: "); Serial.println(pos);
      return constrain(pos, 0, MAX_STEPS_LINEAR);
    }

    long pos2dist(long position) {
      return position * LINEAR_MOVEMENT_ROTATION / STEPS_PER_ROTATION;
    }

    long pos2ang(long position) {
      return (position) * 360 / STEPS_PER_ROTATION;
    }

    void distang2pos(long *distang) {
      for (int i = 0; i < NUM_MOTORS; i++) {
        if (i < 3) {
          distang[i] = dist2pos(distang[i]);  // Convert distances to motor steps
        } else {
          distang[i] = ang2pos(distang[i]);  // Convert angles to motor steps
        }
      }
    }

   void distang2posAng(long *distang) {
    // Nur die Winkel (i >= 3) in Motorpositionen umwandeln
    for (int i = 3; i < NUM_MOTORS; i++) {
        distang[i] = ang2pos(distang[i]);  // Winkel in Motorpositionen umwandeln
    }
}

    void pos2distang(long *position) {
      for (int i = 0; i < NUM_MOTORS; i++) {
        if (i < 3) {
          position[i] = pos2dist(position[i]); // Convert motor steps to distance
        } else {
          position[i] = pos2ang(position[i]);  // Convert motor steps to angles
        }
      }
    }

    // Motor movement function
    void stepMotor(int motor, int dir) {
      switch (motor) {
        case 1: m1step(dir); break;
        case 2: m2step(dir); break;
        case 3: m3step(dir); break;
        case 4: m4step(dir); break;
        case 5: m5step(dir); break;
        case 6: m6step(dir); break;
        default: break;
      }
    }

    // Set motor position with appropriate steps
    void setMotorPosition(int motor, long position) {
      long currentPosition = pos[motor - 1];
      position = constrain(position, 0, (motor <= 3) ? MAX_STEPS_LINEAR : MAX_STEPS_ANGULAR);

      Serial.print("Motor "); Serial.print(motor); Serial.print(" Current Position: "); Serial.print(currentPosition);
      Serial.print(", Target Position: "); Serial.println(position);

      long steps = abs(position - currentPosition);
      int direction = position > currentPosition ? 1 : 0;

      Serial.print("Steps: "); Serial.print(steps); Serial.print(", Direction: "); Serial.println(direction);

      // Move the motor in the required direction
      for (long i = 0; i < steps; i++) {
        stepMotor(motor, direction);
        delayMicroseconds(500); // Adjust for speed
      }

      // Update the current position
      pos[motor - 1] = position;
    }

    // Update motor positions
    void updateMotors() {
      Serial.println("----------- Update Motors -----------");
      Serial.println("Target Positions");
      for(int i = 0; i < NUM_MOTORS; i++) {
        // DEBUG
        Serial.print("Motor "); Serial.print(i + 1); Serial.print(": "); Serial.println(target_pos[i]);
      }

      // Convert angles to motor positions
     // distang2posAng(target_pos); 
     
      Serial.println("----------- Update Motors -----------");

      for(int i = 0; i < NUM_MOTORS; i++) {
        // DEBUG
        Serial.print("Motor "); Serial.print(i + 1); Serial.print(": "); Serial.println(target_pos[i]);
      }

      for (int i = 0; i < NUM_MOTORS; i++) {
        setMotorPosition(i + 1, target_pos[i]);
      }

      array_copy(target_pos, pos, NUM_MOTORS);
    }

    void array_copy(long *src, long *dst, int length) {
      for (int i = 0; i < length; i++) {
        dst[i] = src[i];
      }
    }

    void sendSerialCommand(String command) {
      Serial.println(command);  // Send command over serial
    }

  public:
    MotorControl() :
        kick_motors(0b000000),
        field_size{590, 345},
        max_y(80), // Initialize max_y to 80 [mm]
        player_size(field_size[1] / 3 - max_y) // Set player size based on field
    {
      for (int i = 0; i < NUM_MOTORS; i++) {
        pos[i] = 0;
        target_pos[i] = 0;
        reset_pos[i] = 0;
        reset_pos2[i] = (i < 3) ? 5 : 10;
      }
    }

    void setup() {
      Serial.begin(9600);
      // Initialize motor positions to 0
      distang2pos(reset_pos);
      // Initialize motor positions to 5 and 10
      distang2pos(reset_pos2);

      setup_controller(); // Initialize motor control pins

      initial_setup(); // Initialize motor positions
      sendSerialCommand("INIT");
    }

    void initial_setup() {
      long initial_pos[NUM_MOTORS] = {40, 40, 40, 90, 90, 90};
      array_copy(initial_pos, target_pos, NUM_MOTORS);
      updateMotors();
      delay(5000); // Wait for motors to initialize
    }

    void loop() {
      command(100, 100);
      delay(1000);
      command(100, 300);
      
    }

    
  void defense(long y, int x_index) {
  int motor_num = (x_index - 1) / 2;
  Serial.println("");
  Serial.println("Defense");
  Serial.print("Motor Num for Defense: "); Serial.println(motor_num);

   for (int i = 3; i > motor_num; i -= 1) { // Only 4, 5, 6 motors
    target_pos[i + 3] = 45;
    Serial.print("Defense Angle for Arm Motor "); Serial.print(i + 3); Serial.print("target_pos: "); Serial.println(target_pos[i + 3]); Serial.print("pos: ");Serial.println(pos[i + 3]);
  }
  Serial.println("");
     for (int i = motor_num; i >= 0; i -= 1) { // Only 1, 2, 3 motors
    target_pos[i + 3] = 75;
    target_pos[i] = y2pos(y);
    Serial.print("Defense Angle for Motor "); Serial.print(i + 3); Serial.print("target_pos: "); Serial.println(target_pos[i + 3]); Serial.print("pos: ");Serial.println(pos[i + 3]);
    Serial.print("Defense Distance for Motor "); Serial.print(i); Serial.print("target_pos: "); Serial.println(target_pos[i]); Serial.print("pos: ");Serial.println(pos[i]);
  }
  updateMotors();
  sendSerialCommand("DEFENSE " + String(x_index) + " " + String(y));
}

void kick(uint8_t motors) {
  motors &= 0b111000;
  long take_back = ang2pos(45);
  long follow_through = ang2pos(130);
  Serial.print("Kick Motor Positions: Take Back: "); Serial.print(take_back); Serial.print(", Follow Through: "); Serial.println(follow_through);

  for (int i = 3; i < NUM_MOTORS; i++) {
    if (checkBit(i - 3, motors)) {
      setMotorPosition(i + 1, take_back);
      delay(500);
      setMotorPosition(i + 1, follow_through);
    }
  }
  sendSerialCommand("KICK " + String(take_back) + " " + String(follow_through));
}

void offense(long y, int x_index) {
  int motor_num = x_index / 2;
  Serial.print("Motor Num for Offense: "); Serial.println(motor_num);

  for (int i = 3; i > motor_num; i -= 1) {
    target_pos[i + 3] = 30;
    Serial.print("Offense Angle for Motor "); Serial.print(i + 3); Serial.print(": "); Serial.println(target_pos[i + 3]);
  }
  for (int i = motor_num-1; i >= 0; i -= 1) {
    target_pos[i + 3] = 90;
    Serial.print("Offense Angle for Motor "); Serial.print(i + 3); Serial.print(": "); Serial.println(target_pos[i + 3]);
  }
  target_pos[motor_num] = y2pos(y);
  Serial.print("Offense Distance for Motor "); Serial.print(motor_num); Serial.print(": "); Serial.println(target_pos[motor_num]);

  kick_motors = bitFlip(motor_num + 3, kick_motors);
  updateMotors();

  if (checkflag(kick_motors)) {
    kick(kick_motors);
    kick_motors = 0b0;
  }
  sendSerialCommand("OFFENSE " + String(x_index) + " " + String(y));
}


    void command(long x, long y) {
      int x_index = xIndex(x);
      Serial.println("--------------------");
      Serial.println("Command: "); Serial.print(x); Serial.print(", "); Serial.println(y);
      Serial.println("X Index: "); Serial.println(x_index);
      Serial.println("--------------------");
      if (x_index % 2 == 1) {
        defense(y, x_index);
      } else {
          Serial.println("");
          Serial.println("Offense");
        offense(y, x_index);
      }
    }

    long y2pos(long y) {
      long y_tmp = y % (field_size[1] / 3);
      return min(max(y_tmp - player_size/2, 0), max_y); // Adjust y within bounds
    }

    int xIndex(long x) {
      return x / (field_size[0] / 6); // Map x to motor index
    }

    // Utility functions
    bool checkBit(int bit, uint8_t byte) {
      return (byte & (1 << bit)) != 0;
    }

    uint8_t bitFlip(int bit, uint8_t byte) {
      return byte ^ (1 << bit);
    }

    bool checkflag(uint8_t flag) {
      return flag != 0;
    }

};

MotorControl motorControl;

void setup() {
  motorControl.setup();
}

void loop() {
    motorControl.loop();
}
