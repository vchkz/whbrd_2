
#include <GyverMotor.h>
GMotor motor1(DRIVER2WIRE, 45, 46, HIGH); // мотор1
GMotor motor2(DRIVER2WIRE, 6, 7, HIGH); // мотор2
#define LED_PIN  33      // номер выхода,подключенного к светодиоду
#define  INTERVAL 200UL  
 
void setup() {
  Serial.begin(9600);
  pinMode(37, INPUT_PULLUP); // концевик открытия 1
  pinMode(36, INPUT_PULLUP); // концевик закрытия 1
  
  pinMode(35, INPUT_PULLUP); // концевик открытия 2
  pinMode(34, INPUT_PULLUP); // концевик закрытия 2
  motor1.setMode(AUTO);
  motor1.setSpeed(0);
  motor1.setDeadtime(2);
  motor2.setMode(AUTO);
  motor2.setSpeed(0);
  motor2.setDeadtime(2);
  pinMode(LED_PIN, OUTPUT);
  pinMode(32, INPUT_PULLUP);
  digitalWrite(LED_PIN, LOW);
  
}

bool door_close = true;
uint32_t btnTimer = 0;
bool flag = false;
void loop() {
    if (Serial.available() > 0) {
      int Number = Serial.read() - '0';
      switch (Number) {
        case 1:
          door_close = opening();
          break;
        case 0:
          break;
        default:
          Serial.write(Number);
          break;
      }
    }



  
   // читаем инвертированное значение для удобства
  bool btnState = !digitalRead(32);
  
  if (btnState && !flag && millis() - btnTimer > 100) {
    btnTimer = millis();
    flag = true;
    door_close = closing();
    
  }
  if (!btnState && flag && millis() - btnTimer > 100) {
    flag = false;
    btnTimer = millis();
    //Serial.println("release");
  }
}


int opening() {
  bool mt1 = true;
  bool mt2 = true;
  motor1.setSpeed(200);
  motor2.setSpeed(200);
  while (mt1 or mt2){
    if (!digitalRead(37) == true){motor1.setSpeed(0);mt1 = false;}
    if (!digitalRead(35) == true){motor2.setSpeed(0);mt2 = false;}
    static unsigned long previousMillis = 0;
    if(millis() - previousMillis > INTERVAL) {
      previousMillis = millis();  
      digitalWrite(LED_PIN,!digitalRead(LED_PIN));
  }

    }
   motor1.setSpeed(0);
   digitalWrite(LED_PIN, LOW);
   motor2.setSpeed(0);
   return (false);
   
}

int closing() {
  

  bool mt1 = true;
  bool mt2 = true;
  
  motor1.setSpeed(-254);
  motor2.setSpeed(-254);

  while (mt1 or mt2){
    if (!digitalRead(36) == true){motor1.setSpeed(0);mt1 = false;}
    if (!digitalRead(34) == true){motor2.setSpeed(0);mt2 = false;}
    static unsigned long previousMillis = 0;
    if(millis() - previousMillis > INTERVAL) {
      previousMillis = millis();  
      digitalWrite(LED_PIN,!digitalRead(LED_PIN));
    }
   } 
   motor1.setSpeed(0);
   motor2.setSpeed(0);
   digitalWrite(LED_PIN, LOW);
   return (true);
}
   
