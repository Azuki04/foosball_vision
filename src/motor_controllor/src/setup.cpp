//------------------------------------------------------------------------------
// INCLUDES
//------------------------------------------------------------------------------
#include <Arduino.h>

//------------------------------------------------------------------------------
// CONSTANTS
//------------------------------------------------------------------------------
#define M1_STEP 2
#define M1_DIR  5
#define M1_ENA  0

#define M2_STEP 3
#define M2_DIR  6
#define M2_ENA  0

#define M3_STEP 4
#define M3_DIR  7
#define M3_ENA  0

#define M4_STEP 12
#define M4_DIR  13
#define M4_ENA  0

#define M5_STEP 9
#define M5_DIR  8
#define M5_ENA  0

#define M6_STEP 11
#define M6_DIR  10
#define M6_ENA  0



//------------------------------------------------------------------------------
// GLOBALS
//------------------------------------------------------------------------------
  
//------------------------------------------------------------------------------
// METHODS
//------------------------------------------------------------------------------

void m1step(int dir) {
  digitalWrite(M1_ENA, LOW);
  digitalWrite(M1_DIR, dir == 1 ? HIGH : LOW);
  digitalWrite(M1_STEP, HIGH);
  digitalWrite(M1_STEP, LOW);
}

void m2step(int dir) {
  digitalWrite(M2_ENA, LOW);
  digitalWrite(M2_DIR, dir == 1 ? HIGH : LOW);
  digitalWrite(M2_STEP, HIGH);
  digitalWrite(M2_STEP, LOW);
}

void m3step(int dir) {
  digitalWrite(M3_ENA, LOW);
  digitalWrite(M3_DIR, dir == 1 ? HIGH : LOW);
  digitalWrite(M3_STEP, HIGH);
  digitalWrite(M3_STEP, LOW);
}

void m4step(int dir) {
  digitalWrite(M4_ENA, LOW);
  digitalWrite(M4_DIR, dir == 1 ? HIGH : LOW);
  digitalWrite(M4_STEP, HIGH);
  digitalWrite(M4_STEP, LOW);
}

void m5step(int dir) {
  digitalWrite(M5_ENA, LOW);
  digitalWrite(M5_DIR, dir == 1 ? HIGH : LOW);
  digitalWrite(M5_STEP, HIGH);
  digitalWrite(M5_STEP, LOW);
}

void m6step(int dir) {
  digitalWrite(M6_ENA, LOW);
  digitalWrite(M6_DIR, dir == 1 ? HIGH : LOW);
  digitalWrite(M6_STEP, HIGH);
  digitalWrite(M6_STEP, LOW);
}

void disable() {
  digitalWrite(M1_ENA, HIGH);
  digitalWrite(M2_ENA, HIGH);
  digitalWrite(M3_ENA, HIGH);
  digitalWrite(M4_ENA, HIGH);
  digitalWrite(M5_ENA, HIGH);
  digitalWrite(M6_ENA, HIGH);
}

void setup_controller() {
  pinMode(M1_ENA, OUTPUT);
  pinMode(M2_ENA, OUTPUT);
  pinMode(M3_ENA, OUTPUT);
  pinMode(M4_ENA, OUTPUT);
  pinMode(M5_ENA, OUTPUT);
  pinMode(M6_ENA, OUTPUT);
  
  pinMode(M1_STEP, OUTPUT);
  pinMode(M2_STEP, OUTPUT);
  pinMode(M3_STEP, OUTPUT);
  pinMode(M4_STEP, OUTPUT);
  pinMode(M5_STEP, OUTPUT);
  pinMode(M6_STEP, OUTPUT);
  
  pinMode(M1_DIR, OUTPUT);
  pinMode(M2_DIR, OUTPUT);
  pinMode(M3_DIR, OUTPUT);
  pinMode(M4_DIR, OUTPUT);
  pinMode(M5_DIR, OUTPUT);
  pinMode(M6_DIR, OUTPUT);
}

