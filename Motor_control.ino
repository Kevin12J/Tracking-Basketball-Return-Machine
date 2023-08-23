int pos=0;
void setup() {
  // put your setup code here, to run once:
pinMode(9,OUTPUT); // set Pin9 as PUL
pinMode(8,OUTPUT); // set Pin8 as DIR
Serial.begin(115200);
Serial.setTimeout(1);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(!Serial.available());
  int x=Serial.readString().toInt();
  if(x<0){
    reverse(x,1);
  }
  if(x>0){
    forward(x,1);
  }
    
  //exit(0);
}

void forward(int steps, int pause){
  if(pos-steps>800){
    return NULL;
  }
  int i;
  int x=1000/pause;
  digitalWrite(8,HIGH);
  for(i=0;i<steps;i++){
    digitalWrite(9,HIGH);
    delayMicroseconds(x);
    digitalWrite(9,LOW); // Output low
    delayMicroseconds(x);
  }
  pos+=steps;
}

void reverse(int steps, int pause){
  if(pos-steps<-800){
    return NULL;
  }
  int i;
  int x=1000/pause;
  digitalWrite(8,LOW);
  for(i=0;i<steps;i++){
    digitalWrite(9,HIGH);
    delayMicroseconds(x); // set rotate speed
    digitalWrite(9,LOW); // Output low
    delayMicroseconds(x);
  }
  pos-=steps;
}
