fall_samples_number = 10 #Number of samples to filter the average
fall_samples_delay = 1 #delay of 1 second between each measurement
fall_channel = 2 #ADS1115 Channel for the Fall Sensor
GAIN = 1 #ADS1115 Gain for values between +/- 4.096V


#-----------------------------FallSensor()----------------------------------------#
#Alert function for the fall sensor to detect if the user fell from the wheelchair#
#---------------------------------------------------------------------------------#
def FallSensor():
    fall_sum = 0.0 #Sum of the 10 samples in each loop
    for i in range(fall_samples_number):
        fall_adc_read = Adafruit_ADS1x15.ADS1115() #Read function for the ADS1115 ADC
        fall_value = fall_adc_read.read_adc(fall_channel, gain = GAIN) #Store value taken from the ADC
        fall_sum += fall_value
        time.sleep(fall_samples_delay)

    fall_avg = fall_sum/fall_samples_number #Average filter
    if fall_avg <= 50:#Calibration for the piezoelectric preassure sensor
        return 1 #Alert patient fall!
    else:
        return 0 #Normal status
