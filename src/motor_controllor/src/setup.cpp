//------------------------------------------------------------------------------
// INCLUDES
//------------------------------------------------------------------------------
#include <Arduino.h>

//------------------------------------------------------------------------------
// KONSTANTEN
//------------------------------------------------------------------------------

    #define M1_STEP 2
    #define M1_DIR  5

    #define M2_STEP 4
    #define M2_DIR  7

    #define M3_STEP 9
    #define M3_DIR  8

    #define M4_STEP 11
    #define M4_DIR  10

    #define M5_STEP 3
    #define M5_DIR  6

    #define M6_STEP 12 
    #define M6_DIR  13

//------------------------------------------------------------------------------
// Method Declaration for Motor Control
//------------------------------------------------------------------------------

void m1step(int dir) {
    digitalWrite(M1_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M1_STEP, HIGH);
    delayMicroseconds(1);
    digitalWrite(M1_STEP, LOW);
    delayMicroseconds(1);
}

void m2step(int dir) {
    digitalWrite(M2_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M2_STEP, HIGH);
    delayMicroseconds(1);
    digitalWrite(M2_STEP, LOW);
    delayMicroseconds(1);
}

void m3step(int dir) {
    digitalWrite(M3_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M3_STEP, HIGH);
    delayMicroseconds(1);
    digitalWrite(M3_STEP, LOW);
    delayMicroseconds(1);
}

void m4step(int dir) {
    digitalWrite(M4_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M4_STEP, HIGH);
    delayMicroseconds(1);
    digitalWrite(M4_STEP, LOW);
    delayMicroseconds(1);
}

void m5step(int dir) {
    digitalWrite(M5_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M5_STEP, HIGH);
    delayMicroseconds(1);
    digitalWrite(M5_STEP, LOW);
    delayMicroseconds(1);
}

void m6step(int dir) {
    digitalWrite(M6_DIR, dir == 1 ? HIGH : LOW);
    digitalWrite(M6_STEP, HIGH);
    delayMicroseconds(1);
    digitalWrite(M6_STEP, LOW);
    delayMicroseconds(1);
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