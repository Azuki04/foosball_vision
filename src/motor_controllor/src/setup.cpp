//------------------------------------------------------------------------------
// INCLUDES
//------------------------------------------------------------------------------
#include <Arduino.h>

//------------------------------------------------------------------------------
// CONSTANTS (MOTOR PINS)
//------------------------------------------------------------------------------
    
// Configuration for Bar 1 (M1 - M4)

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