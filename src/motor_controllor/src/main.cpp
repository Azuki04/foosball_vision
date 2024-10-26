    //------------------------------------------------------------------------------
    // INCLUDES
    //------------------------------------------------------------------------------
    #include <Arduino.h>
    #include <config.h>

    //------------------------------------------------------------------------------
    // global variables
    //------------------------------------------------------------------------------
    long current_pos[NUM_MOTORS] = {0, 0, 0, 0, 0, 0};
    long target_pos[NUM_MOTORS] = {0, 0, 0, 0, 0, 0};
    uint8_t kick_motors = 0b000000;

    //------------------------------------------------------------------------------
    // helper functions
    //------------------------------------------------------------------------------

    int checkBit(int n, uint8_t a) {
        return (a >> n) & 0b1;
    }

    uint8_t bitFlip(int n, uint8_t pre_flag) {
        return pre_flag | (0b1 << n);
    }

    boolean checkflag(uint8_t flag) {
        return (flag & 0b111111) != 0;
    }

    void array_copy(long *src, long *dst, int length) {
        for (int i = 0; i < length; i++) {
            dst[i] = src[i];
        }
    }

    long convertDistanceToSteps(long distance) {
        return constrain((STEPS_PER_ROTATION * distance) / LINEAR_MOVEMENT_ROTATION, 0, MAX_STEPS_LINEAR); // [0 ... 450]
    }

    long convertAngleToSteps(long angle) {
        return constrain((STEPS_PER_ROTATION * angle) / 360, 0, MAX_STEPS_ANGULAR); // [0 ... 126]
    }

    void convertDistanceAndAngleToSteps(long *distanceAndAngle, long *motorSteps) {
        for (int motorIndex = 0; motorIndex < NUM_MOTORS; motorIndex++) {
            if (motorIndex < 3) {
                motorSteps[motorIndex] = convertDistanceToSteps(distanceAndAngle[motorIndex]);
                motorSteps[motorIndex] = constrain(motorSteps[motorIndex], 0, MAX_STEPS_LINEAR);
            } else {
                motorSteps[motorIndex] = convertAngleToSteps(distanceAndAngle[motorIndex]);
                motorSteps[motorIndex] = constrain(motorSteps[motorIndex], 0, MAX_STEPS_ANGULAR);
            }
        }
    }

    int xIndex(long x) {
        int index = x / (FIELD_SIZE[0] / 6);
        return index;
    }

    long calculatePlayerPosition(long y) {
          long sectionOffset = y % (FIELD_SIZE[1] / 3);
          long centeredPosition = sectionOffset - PLAYER_SIZE / 2;
          centeredPosition = constrain(centeredPosition, 0, MAX_TRAVEL_DISTANCE);
          return centeredPosition;
    }

    void stepMotor(int motor, long steps, int dir) {

        void (*motorStepFunctions[])(int) = {m1step, m2step, m3step, m4step, m5step, m6step};

        if (motor < 1 || motor > 6) {
            return;
        }
        for (long i = 0; i < steps; i++) {
            motorStepFunctions[motor - 1](dir);
            // delayMicroseconds(500);
        }
    }

    void setMotorPosition(int motor, long targetPosition) {
        long currentPosition = current_pos[motor - 1];

        long stepsRequired = (motor <= 3)
                    ? convertDistanceToSteps(abs(targetPosition - currentPosition))
                    : convertAngleToSteps(abs(targetPosition - currentPosition));

        int direction = (targetPosition > currentPosition) ? 0 : 1; // 0 = forward, 1 = backward

        if (stepsRequired > 0) {
            stepMotor(motor, stepsRequired, direction);
            current_pos[motor - 1] = target_pos[motor - 1];
        }
    }

    void updateMotors() {
        for (int motorIndex = 0; motorIndex < NUM_MOTORS; motorIndex++) {
            setMotorPosition(motorIndex + 1, target_pos[motorIndex]);
        }
    }

    //------------------------------------------------------------------------------
    // main functions
    //------------------------------------------------------------------------------

    void defense(long y, int x_index) {
        // Index [1,3,5] for defense
        int lin_motor_num = (x_index - 1) / 2; // Possible values [0,1,2]
        lin_motor_num = constrain(lin_motor_num, 0, 2);

        // Set rotational motors up for the ball shoot
        for (int i = 2; i > lin_motor_num; i--) { // [5,4]
            target_pos[i + 3] = 45;
        }

        // Set rotational motors down for the ball shoot and linear motors to the ball position
        for (int i = lin_motor_num; i >= 0; i--) {
            target_pos[i + 3] = 75;
            target_pos[i] = calculatePlayerPosition(y);
        }

        updateMotors();
    }

    void kick(uint8_t motors) {
        motors = motors & 0b111000;
        long take_back_angle = 45;
        long follow_through_angle = 130;

        for (int i = 3; i < 5; i++) {
            if (checkBit(i, motors)) {
                target_pos[i] = take_back_angle;
            }
        }

        updateMotors();
        delay(100);

        for (int i = 3; i < 5; i++) {
            if (checkBit(i, motors)) {
                target_pos[i] = follow_through_angle;
            }
        }
        updateMotors();
    }

    void offense(long y, int x_index) {
        int lin_motor_num = x_index / 2; // [0,1,2]
        lin_motor_num = constrain(lin_motor_num, 0, 2);

        for (int i = 2; i > lin_motor_num; i--) {
            target_pos[i + 3] = 30;
        }

        for (int i = lin_motor_num - 1; i >= 0; i--) {
            target_pos[i + 3] = 90;
        }

        target_pos[lin_motor_num] = calculatePlayerPosition(y);

        if (checkBit(lin_motor_num + 3, kick_motors) == 0) {
            kick_motors = bitFlip(lin_motor_num + 3, kick_motors);
        }

        updateMotors();

        if (checkflag(kick_motors)) {
            kick(kick_motors);
            kick_motors = 0b000000;
        }
    }

    void command(long x, long y) {
        //y = field_size[1] - y;
        int x_index = xIndex(x);

        if (x_index % 2 == 1) { // offense = odd index AND defense = even index
            defense(y, x_index);
        } else {
            offense(y, x_index);
        }
    }


    void resetSystem() {
        memset(pos, 0, sizeof(pos));
        memset(target_pos, 0, sizeof(target_pos));
        kick_motors = 0b000000;

        long max_pos[NUM_MOTORS];
        for (int i = 0; i < NUM_MOTORS; i++) {
            if (i < 3) {
                max_pos[i] = MAX_STEPS_LINEAR;
            } else {
                max_pos[i] = MAX_STEPS_ANGULAR;
            }
        }
        array_copy(max_pos, target_pos, NUM_MOTORS);
        updateMotors();

        long max_steps[NUM_MOTORS];
        convertDistanceAndAngleToSteps(target_pos, max_steps);
        array_copy(max_steps, pos, NUM_MOTORS);

        delay(1000);

        long zero_pos[NUM_MOTORS] = {0, 0, 0, 0, 0, 0};
        array_copy(zero_pos, target_pos, NUM_MOTORS);
        updateMotors();

        long zero_steps[NUM_MOTORS];
        convertDistanceAndAngleToSteps(target_pos, zero_steps);
        array_copy(zero_steps, pos, NUM_MOTORS);

        delay(1000);

        long initial_pos[NUM_MOTORS] = {30, 30, 30, 90, 90, 90};
        array_copy(initial_pos, target_pos, NUM_MOTORS);
        updateMotors();

        long initial_steps[NUM_MOTORS];
        convertDistanceAndAngleToSteps(target_pos, initial_steps);
        array_copy(initial_steps, pos, NUM_MOTORS);

        delay(1000); 
    }

    //------------------------------------------------------------------------------
    // Arduino functions
    //------------------------------------------------------------------------------

    void setup() {
        Serial.begin(9600);
        setup_controller();

        long initial_pos[NUM_MOTORS] = {0, 0, 0, 90, 90, 90};
        array_copy(initial_pos, target_pos, NUM_MOTORS);
        updateMotors();


        long initial_steps[NUM_MOTORS];
        convertDistanceAndAngleToSteps(target_pos, initial_steps);
        array_copy(initial_steps, pos, NUM_MOTORS);


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
     /*
         void loop() {
            long x = 90;
            long y = 60;
            command(x, y);
            delay(2000);
        }
     */
