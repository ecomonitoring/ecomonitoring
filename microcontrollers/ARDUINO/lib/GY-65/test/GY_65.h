#include "GY_65.cpp"

class GY_65{
private:
    int temperature;
    long pressure;
    uint8_t addr;
    
    const unsigned char oversampling_setting = 3; //oversampling for measurement
    const unsigned char pressure_conversiontime[4] = {5, 8, 14, 26};
    int ac1;
    int ac2; 
    int ac3; 
    unsigned int ac4;
    unsigned int ac5;
    unsigned int ac6;
    int b1; 
    int b2;
    int mb;
    int mc;
    int md;
    
    void getCalibrationData();
    void writeRegister(unsigned char r, unsigned char v);
    int readIntRegister(unsigned char r);
    long readUP();
    unsigned int readUT();
    

public:
    GY_65(uint8_t adress): addr(adress){Wire.begin();};
    void begin(){ getCalibrationData();}
    void readSensor();
    
    int getTemperature(){ return temperature;}
    long getPressure(){ return pressure;}
    
    
    
    
    
};
