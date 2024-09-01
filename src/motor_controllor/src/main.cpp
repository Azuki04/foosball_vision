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
      // Determine which section of the field the ball is in
      return x / (field_size[0] / 6);
    }

    void sendSerialCommand(String command) {
      // TODO: Implement serial communication
    }

     void stepMotor(int motor, int dir) {
      // Use the provided functions to step the motor
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
      int currentPosition = pos[motor - 1]; // Adjust for zero-based index
      int steps = abs(position - currentPosition);
      int direction = position > currentPosition ? 1 : 0;
      
      for (int i = 0; i < steps; i++) {
        stepMotor(motor, direction);
        delayMicroseconds(1000); // Adjust delay as necessary
      }
      
      pos[motor - 1] = position;
    }

    void executeCommand(String command) {
      int index1 = command.indexOf(' ');
      if (index1 == -1) return;
      String cmd = command.substring(0, index1);
      command = command.substring(index1 + 1);
      
      int index2 = command.indexOf(' ');
      if (index2 == -1) return;
      long y = command.substring(0, index2).toInt();
      int x_index = command.substring(index2 + 1).toInt();
      
      if (cmd == "DEFENSE") {
        defense(y, x_index);
      } else if (cmd == "OFFENSE") {
        offense(y, x_index);
      } else if (cmd == "KICK") {
        kick(y); // Assuming y contains the motors info in this case
      }
    }

  public:
    MotorControl()
      : non_error_motors(0b111111), 
        error_motion(0b000000),
        kick_motors(0b000000),
        field_size{590, 345} // Example values
    {
      // Initialize motor positions and error recovery speeds
      for (int i = 0; i < NUM_MOTORS; i++) {
        pos[i] = 0;
        pos_copy[i] = 0;
        error_recovery_speed[i] = (i < 3) ? 0x6000 : 0x3000;
        reset_pos[i] = 0;
        reset_pos2[i] = (i < 3) ? 5 : 10;
      }
    }

    void defense(long y, int x_index) {
      int motor_num = (x_index - 1) / 2;
      for (int i = 3; i > motor_num; i--) {
        pos[i + 3] = 45;
      }
      for (int i = motor_num; i >= 0; i--) {
        pos[i + 3] = 75;
        pos[i] = dist2pos(y);
      }
      for (int i = 1; i <= NUM_MOTORS; i++) {
        setMotorPosition(i, pos[i - 1]);
      }
      sendSerialCommand("DEFENSE " + String(x_index) + " " + String(y));
    }

    void kick(uint8_t motors) {
      motors = motors & 0b111000;
      long take_back = ang2pos(45);
      long follow_through = ang2pos(130);
      for (int i = 1; i <= NUM_MOTORS; i++) {
        if (checkBit(i - 1, motors)) {
          setMotorPosition(i, take_back);
          delay(1000); // Wait for the motor to reach position
          setMotorPosition(i, follow_through);
          delay(1000); // Wait for the motor to reach position
        }
      }
      sendSerialCommand("KICK " + String(take_back) + " " + String(follow_through));
    }

    void offense(long y, int x_index) {
      int motor_num = xIndex(x_index) / 2;
      for (int i = 3; i > motor_num; i--) {
        pos[i + 3] = 30;
      }
      for (int i = motor_num - 1; i >= 0; i--) {
        pos[i + 3] = 90;
      }
      pos[motor_num] = dist2pos(y);
      if (!checkBit(motor_num + 3, kick_motors)) {
        kick_motors = bitFlip(motor_num + 3, kick_motors);
      }
      for (int i = 1; i <= NUM_MOTORS; i++) {
        setMotorPosition(i, pos[i - 1]);
      }
      sendSerialCommand("OFFENSE " + String(x_index) + " " + String(y));
      if (checkflag(kick_motors)) {
        kick(kick_motors);
        kick_motors = 0b0;
      }
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
      sendSerialCommand("ERROR_RECOVERY " + String(motors));
    }

    void setup() {
      Serial.begin(9600);

      setup_controller(); // Initialize motor control pins

      // TODO: Implement serial communication (Python script)
      sendSerialCommand("INIT");
    }

    void loop() {
      // Simulate a ball detection with random coordinates
      long ball_x = random(0, field_size[0]); // Random X position
      long ball_y = random(0, field_size[1]); // Random Y position
    
      command(ball_x, ball_y);

      delay(2000); 
    }
};

MotorControl motorControl;

void setup() {
  motorControl.setup();
}

void loop() {
  motorControl.loop();
}
