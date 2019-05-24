void setup() {
  char cards[5][16] = {"127FB2B6", "E47F410E", "ACFA5B47", "A455420E", "F458430E"};;

  Serial.begin(9600);
  randomSeed(analogRead(A0));
  Serial.println(cards[random(0,5)]);
}

void loop() {

}
