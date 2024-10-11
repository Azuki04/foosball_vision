#ifndef CONFIG_H
#define CONFIG_H

//------------------------------------------------------------------------------
// Method Declaration for Motor Control
//------------------------------------------------------------------------------
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

long field_size[2] = {590, 345}; //[mm] (width, height)
long max_y = 80;                 //[mm] max travel distance in y direction
long player_size = field_size[1] / 3 - max_y; //[mm] size of the player

// Parameters for the conversion
const int STEPS_PER_ROTATION = 200;    // Steps per revolution of the motor
const int LINEAR_MOVEMENT_ROTATION = 40; // Movement in mm per revolution for linear motors
const int MAX_STEPS_LINEAR = (STEPS_PER_ROTATION * max_y) / LINEAR_MOVEMENT_ROTATION;
const int MAX_STEPS_ANGULAR = STEPS_PER_ROTATION;  // For 360-degree rotation

#endif