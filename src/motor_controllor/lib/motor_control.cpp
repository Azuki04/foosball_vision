#include <Arduino.h>
#include <config.h>

// Motor configuration
#define NUM_MOTORS 6
#define STEPS_PER_ROTATION 200
#define LINEAR_MOVEMENT_ROTATIO 40

class MotorControl {
  private:
    long pos[NUM_MOTORS];
    long pos_copy[NUM_MOTORS];
    uint8_t non_error_motors;
    uint8_t error_motion;
    long error_recovery_speed[NUM_MOTORS];
    long reset_pos[NUM_MOTORS];
    long reset_pos2[NUM_MOTORS];
    uint8_t kick_motors;
    long field_size[2];
    long max_y;
    long player_size;
    long param[NUM_MOTORS];

    long dist2pos(long distance) {
      return STEPS_PER_ROTATION * distance / LINEAR_MOVEMENT_ROTATIO;
    }

    long ang2pos(long angle) {
      return STEPS_PER_ROTATION * angle / 360;
    }

    long pos2dist(long position) {
      return position * LINEAR_MOVEMENT_ROTATIO / STEPS_PER_ROTATION;
    }

    long pos2ang(long position) {
      return position * 360 / STEPS_PER_ROTATION;
    }

    void distang2pos(long *distang) {
      for (int i = 0; i < NUM_MOTORS; i++) {
        if (i < 3) {
          Serial.println(distang[i]);
          distang[i] = dist2pos(distang[i]);
        } else {
          distang[i] = ang2pos(distang[i]);
        }
      }
    }

    void pos2distang(long *position) {
      for (int i = 0; i < NUM_MOTORS; i++) {
        if (i < 3) {
          position[i] = pos2dist(position[i]);
        } else {
          position[i] = pos2ang(position[i]);
        }
      }
    }

    bool checkBit(int bit, uint8_t byte) {
      return (byte & (1 << bit)) != 0;
    }

    uint8_t bitFlip(int bit, uint8_t byte) {
      return byte ^ (1 << bit);
    }

    bool checkflag(uint8_t flag) {
      return flag != 0;
    }

    int xIndex(long x) {
      return x / (field_size[0] / 6); // get the index of the x position
    }

    long y2pos(long y) {
      long y_tmp = y % (field_size[1] / 3); 
      return min(max(y_tmp - player_size / 2, 0), max_y);  // get the y position
    }

    void sendSerialCommand(String command) {
      // Implement serial communication if needed
      Serial.println(command);
    }

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

    void setMotorPosition(int motor, long position) {
      long currentPosition = pos[motor - 1];
      sendSerialCommand("Current position of motor " + String(motor) + ": " + String(currentPosition));
      sendSerialCommand("Setting position of motor " + String(motor) + " to: " + String(position));
      long steps = abs(position - currentPosition); // get absolute value of the steps
      int direction = position > currentPosition ? 1 : 0;
    
      for (long i = 0; i < steps; i++) {
        stepMotor(motor, direction);
        delayMicroseconds(500); 
      }

      pos[motor - 1] = position;
    }

    void defense(long y, int x_index) {
      int motor_num = (x_index - 1) / 2; 
      for (int i = 3; i > motor_num; i--) {
        pos[i + 3] = 45;
      }
      for (int i = motor_num; i >= 0; i--) {
        pos[i + 3] = 75;
        pos[i] = y2pos(y);
      }
      array_copy(pos, pos_copy, NUM_MOTORS);
      distang2pos(pos);
      uint8_t non_kick_motors = ~kick_motors & non_error_motors;
      for (int i = 0; i < NUM_MOTORS; i++) {
        if (checkBit(i, non_kick_motors)) {
          setMotorPosition(i + 1, pos[i]);
        }
      }
      array_copy(pos_copy, pos, NUM_MOTORS);
      sendSerialCommand("DEFENSE " + String(x_index) + " " + String(y));
    }

    void kick(uint8_t motors) {
      motors = motors & 0b111000; // for safety
      long take_back = ang2pos(45);
      long follow_through = ang2pos(130);
      for (int i = 0; i < NUM_MOTORS; i++) {
        if (checkBit(i + 1, motors)) {
          setMotorPosition(i + 1, take_back);
          delay(500); // Wait for the first movement to complete
          setMotorPosition(i + 1, follow_through);
        }
      }
      sendSerialCommand("KICK " + String(take_back) + " " + String(follow_through));
    }

    void offense(long y, int x_index) {
      int motor_num = xIndex(x_index) / 2;
      Serial.println(motor_num + " test" + motor_num);
      for (int i = 3; i > motor_num; i--) {
        pos[i + 3] = 30;
      }
      for (int i = motor_num - 1; i >= 0; i--) {
        pos[i + 3] = 90;
      }
      pos[motor_num] = y2pos(y);
      if (!checkBit(motor_num + 3, kick_motors)) {
        kick_motors = bitFlip(motor_num + 3, kick_motors);
      }
      uint8_t non_kick_motors = ~kick_motors & non_error_motors;

      array_copy(pos, pos_copy, NUM_MOTORS);
      distang2pos(pos);
      for (int i = 0; i < NUM_MOTORS; i++) {
        if (checkBit(i, non_kick_motors)) {
          setMotorPosition(i + 1, pos[i]);
        }
      }
      if (checkflag(kick_motors)) {
        kick(kick_motors);
        kick_motors = 0b0;
      }
      array_copy(pos_copy, pos, NUM_MOTORS);
      sendSerialCommand("OFFENSE " + String(x_index) + " " + String(y));
    }

    void command(long x, long y) {
      y = field_size[1] - y;
      int x_index = xIndex(x);
      if (x_index % 2 == 1) {
        defense(y, x_index);
      } else {
        offense(y, x_index);
      }
    }

    void error_recovery_motion(uint8_t motors, long *speed) {
      uint8_t rot_motors = motors & 0b111000;
      uint8_t lin_motors = motors & 0b000111;
      if (checkflag(rot_motors)) {
        for (int i = 0; i < NUM_MOTORS; i++) {
          if (checkBit(i, rot_motors)) {
            setMotorPosition(i + 1, 400); // Use speed as a placeholder here
          }
        }
      }
      if (checkflag(lin_motors)) {
        for (int i = 0; i < NUM_MOTORS; i++) {
          if (checkBit(i, lin_motors)) {
            setMotorPosition(i + 1, 400); // Use speed as a placeholder here
          }
        }
      }
      sendSerialCommand("ERROR_RECOVERY " + String(motors));
    }

  
    void initial_setup() {
      uint8_t motors = 0b111111;
      long speed[NUM_MOTORS] = {1000, 1000, 1000, 1000, 1000, 1000};
      error_recovery_motion(motors, speed);
      delay(5000); // Wait for motors to initialize

      // Set initial positions
      long initial_pos[NUM_MOTORS] = {30, 30, 30, 90, 90, 90};
      array_copy(initial_pos, pos, NUM_MOTORS); // Update pos array
      for (int i = 0; i < NUM_MOTORS; i++) {
        setMotorPosition(i + 1, pos[i]); // Move motors to initial positions
      }
      array_copy(pos, pos_copy, NUM_MOTORS); // Copy to pos_copy
    }
  

    void array_copy(long *src, long *dst, int length) {
      for (int i = 0; i < length; i++) {
        dst[i] = src[i];
      }
    }

  public:
    MotorControl() :
        non_error_motors(0b111111),
        error_motion(0b000000), // Initialize error_motion to 0
        kick_motors(0b000000), // Initialize kick_motors to 0
        field_size{590, 345},
        max_y(80), // Initialize max_y to 80 [mm]
        player_size(field_size[1] / 3 - max_y // Initialize player_size 345 / 3 - 80 = 85 [mm] the player size
        ) {
      // Initialize motor positions and error recovery speeds
      for (int i = 0; i < NUM_MOTORS; i++) {
        pos[i] = 0;
        pos_copy[i] = 0;
        error_recovery_speed[i] = (i < 3) ? 1000 : 500;
        reset_pos[i] = 0;
        reset_pos2[i] = (i < 3) ? 5 : 10;
      }
    }

    void setup() {
      Serial.begin(9600);
      distang2pos(reset_pos);
      distang2pos(reset_pos2);

      setup_controller(); // Initialize motor control pins

      initial_setup(); // Initialize motor positions

      // TODO: Implement serial communication (Python script)
      sendSerialCommand("INIT");
    }

    void stepper_loop() {
      // Implement stepper motor control loop
      pos2distang(param);
    }
    void loop() {
     stepper_loop();
     
   
    Serial.println( "test " + checkBit(NUM_MOTORS+3, kick_motors));
    kick_motors = bitFlip(NUM_MOTORS + 3,kick_motors);
    Serial.println(kick_motors);
    kick_motors = 0b0;
    
    
    }
};

MotorControl motorControl;

void setup() {
  motorControl.setup();
}

void loop() {
  motorControl.loop();
}
