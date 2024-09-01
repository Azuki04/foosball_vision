#ifndef CONFIG_H
#define CONFIG_H

//------------------------------------------------------------------------------
// METHODS DECLARATION FOR MOTOR CONTROL
//------------------------------------------------------------------------------
extern void m1step(int dir);
extern void m2step(int dir);
extern void m3step(int dir);
extern void m4step(int dir);
extern void m5step(int dir);
extern void m6step(int dir);
extern void disable();
extern void setup_controller();


#endif