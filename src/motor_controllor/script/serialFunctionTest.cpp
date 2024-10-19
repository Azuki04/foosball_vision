void setup() {
  Serial.begin(9600);
  // Motor 1
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  digitalWrite(4, LOW);

  // Motor 2
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  digitalWrite(8, LOW);

  // Motor 3
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(12, LOW);

  // Motor 4
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  digitalWrite(2, LOW);

  // Motor 5
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(6, LOW);

  // Motor 6
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  digitalWrite(10, LOW);
}

void command(){
  digitalWrite(5, HIGH);
  digitalWrite(9, HIGH);
  digitalWrite(13, HIGH);
  delayMicroseconds(1000);
  digitalWrite(5, LOW);
  digitalWrite(9, LOW);
  digitalWrite(13, LOW);
  delayMicroseconds(1000);

  digitalWrite(2, LOW);
  digitalWrite(6, LOW);
  digitalWrite(10, LOW);

  for (int i = 0; i < 50; i++) {
    digitalWrite(5, HIGH);
    digitalWrite(9, HIGH);
    digitalWrite(13, HIGH);

    digitalWrite(3, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(11, HIGH);
    delayMicroseconds(1000);

    digitalWrite(5, LOW);
    digitalWrite(9, LOW);
    digitalWrite(13, LOW);
    digitalWrite(3, LOW);
    digitalWrite(7, LOW);
    digitalWrite(11, LOW);
    delayMicroseconds(1000);
  }

  delay(500);

  digitalWrite(2, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(10, HIGH);
  for (int i = 0; i < 50; i++) {
    digitalWrite(5, HIGH);
    digitalWrite(9, HIGH);
    digitalWrite(13, HIGH);

    digitalWrite(3, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(11, HIGH);
    delayMicroseconds(1000);


    digitalWrite(5, LOW);
    digitalWrite(9, LOW);
    digitalWrite(13, LOW);
    digitalWrite(3, LOW);
    digitalWrite(7, LOW);
    digitalWrite(11, LOW);
    delayMicroseconds(1000);
  }

  delay(500);
}


void loop() {
    if(Serial.available()){
    command();
    }
}


