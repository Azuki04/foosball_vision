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

long FIELD_SIZE[2] = {590, 345}; //[mm] (width, height)
long MAX_TRAVEL_DISTANCE = 90;   //[mm] max travel distance in y direction
long max_rotation = 130;         //[degree] max rotation angle
long PLAYER_SIZE = FIELD_SIZE[1] / 3 - MAX_TRAVEL_DISTANCE; //[25 mm] size of the player with bumper

// Parameters for the conversion
const int STEPS_PER_ROTATION = 200; // Steps per revolution of the motor
const int LINEAR_MOVEMENT_ROTATION = 40; // Movement in mm per revolution for linear motors
const int MAX_STEPS_LINEAR = (STEPS_PER_ROTATION * MAX_TRAVEL_DISTANCE) / LINEAR_MOVEMENT_ROTATION;
const int MAX_STEPS_ANGULAR = (position) * 360 / STEPS_PER_ROTATION;

#endif