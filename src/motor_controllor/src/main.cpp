    //------------------------------------------------------------------------------
    // INCLUDES
    //------------------------------------------------------------------------------
    #include <Arduino.h>
    #include <config.h>

    //------------------------------------------------------------------------------
    // global variables
    //------------------------------------------------------------------------------
    long pos[NUM_MOTORS] = {0, 0, 0, 0, 0, 0};
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

    uint8_t bitFlip2(int n, uint8_t pre_flag) {
        return pre_flag & ~(0b1 << n);
    }

    boolean checkflag(uint8_t flag) {
        return (flag & 0b111111) != 0;
    }

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

    void distang2pos(long *distang, long *steps) {
        for (int i = 0; i < NUM_MOTORS; i++) {
            if (i < 3) {
                steps[i] = dist2pos(distang[i]);
                steps[i] = constrain(steps[i], 0, MAX_STEPS_LINEAR);
            } else {
                steps[i] = ang2pos(distang[i]);
                steps[i] = constrain(steps[i], 0, MAX_STEPS_ANGULAR);
            }
        }
    }

    int xIndex(long x) {
        int index = x / (field_size[0] / 6);
        return index;
    }

    long y2pos(long y) {
        long y_tmp = y % (field_size[1] / 3);
        long position = y_tmp - player_size / 2;
        position = constrain(position, 0, max_y);
        return position;
    }

    void stepMotor(int motor, long steps, int dir) {
        for (long i = 0; i < steps; i++) {
            switch (motor) {
                case 1: m1step(dir); break;
                case 2: m2step(dir); break;
                case 3: m3step(dir); break;
                case 4: m4step(dir); break;
                case 5: m5step(dir); break;
                case 6: m6step(dir); break;
            }
            delayMicroseconds(500);
        }
    }

    void setMotorPosition(int motor, long targetPosition) {
        long currentPosition = pos[motor - 1];
        long max_steps = (motor <= 3) ? MAX_STEPS_LINEAR : MAX_STEPS_ANGULAR;
        targetPosition = constrain(targetPosition, 0, max_steps);

        long steps = abs(targetPosition - currentPosition);
        int direction = (targetPosition > currentPosition) ? 1 : 0;

        if (steps > 0) {
            stepMotor(motor, steps, direction);
            pos[motor - 1] = targetPosition;
        }
    }

    void updateMotors() {
        long target_steps[NUM_MOTORS];
        distang2pos(target_pos, target_steps);

        for (int i = 0; i < NUM_MOTORS; i++) {
            setMotorPosition(i + 1, target_steps[i]);
        }
    }

    //------------------------------------------------------------------------------
    // main functions
    //------------------------------------------------------------------------------

    void defense(long y, int x_index) {
        int motor_num = (x_index - 1) / 2;
        motor_num = constrain(motor_num, 0, 2);

        for (int i = 3; i > motor_num; i--) {
            target_pos[i + 3] = 45;
        }

        for (int i = motor_num; i >= 0; i--) {
            target_pos[i + 3] = 75;
            target_pos[i] = y2pos(y);
        }

        updateMotors();
    }

    void kick(uint8_t motors) {
        motors = motors & 0b111000;
        long take_back_angle = 45;
        long follow_through_angle = 130;

        for (int i = 3; i < 6; i++) {
            if (checkBit(i, motors)) {
                target_pos[i] = take_back_angle;
            }
        }
        updateMotors();
        delay(100);

        for (int i = 3; i < 6; i++) {
            if (checkBit(i, motors)) {
                target_pos[i] = follow_through_angle;
            }
        }
        updateMotors();
    }

    void offense(long y, int x_index) {
        int motor_num = x_index / 2;
        motor_num = constrain(motor_num, 0, 2);

        for (int i = 3; i > motor_num; i--) {
            target_pos[i + 3] = 30;
        }

        for (int i = motor_num - 1; i >= 0; i--) {
            target_pos[i + 3] = 90;
        }

        target_pos[motor_num] = y2pos(y);

        if (checkBit(motor_num + 3, kick_motors) == 0) {
            kick_motors = bitFlip(motor_num + 3, kick_motors);
        }

        updateMotors();

        if (checkflag(kick_motors)) {
            kick(kick_motors);
            kick_motors = 0b000000;
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

    //------------------------------------------------------------------------------
    // Arduino functions
    //------------------------------------------------------------------------------

    void setup() {
        Serial.begin(9600);
        setup_controller();

        long initial_pos[NUM_MOTORS] = {30, 30, 30, 90, 90, 90};
        array_copy(initial_pos, target_pos, NUM_MOTORS);
        updateMotors();


        long initial_steps[NUM_MOTORS];
        distang2pos(target_pos, initial_steps);
        array_copy(initial_steps, pos, NUM_MOTORS);
    }

    void loop() {
        // TODO: Implement the main loop
        long x = 90;
        long y = 60;
        command(x, y);

        delay(2000);
    }
