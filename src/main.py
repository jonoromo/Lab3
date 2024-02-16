import motor_driver
import encoder_reader
import motor_controller
import utime

"""!
This main file is to be uploaded to the nucleo board and run by writing a Ctrl-D from
the GUI. The code defines the encoder and the motor pins, sets their correspondng timers,
and instantiates a motor driver and encoder reader. The motor controller is also
instantiated and a step response test is run. The step response repeatedly sets the motor
duty cycle with the PWM signal from the closed loop proportional control from the motor
controller run method. Every 10 ms the time and encoder position are recorded. This cycle runs
for 60 iterations, providing enough time for the step response to reach steady state. Once the
test has finished, the time and position are printed, which is read by the GUI and plotted.
"""

enPin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
in2_pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
in1_pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
timmy = pyb.Timer(3, freq=20000)
ch_pos = timmy.channel(2, pyb.Timer.PWM, pin=in2_pin)
ch_neg = timmy.channel(1, pyb.Timer.PWM, pin=in1_pin)

moe = motor_driver.MotorDriver(enPin, in2_pin, in1_pin, timmy, ch_pos, ch_neg)

pinA = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=pyb.Pin.AF1_TIM2)
pinB = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=pyb.Pin.AF1_TIM2)

timer = pyb.Timer(8, prescaler=1, period=65535)
chan_A = timer.channel(1, pyb.Timer.ENC_AB, pin=pinA)
chan_B = timer.channel(2, pyb.Timer.ENC_AB, pin=pinB)

enc = encoder_reader.Encoder(pinA, pinB, timer, chan_A, chan_B)

con = motor_controller.Controller(0.5, 10000)
setpoint = 0
setpoint += 10000
for i in range(60):
    moe.set_duty_cycle(con.run(setpoint,enc.read()))
    con.meas_time(utime.ticks_ms())
    con.meas_pos(enc.read())
    utime.sleep_ms(10)
moe.set_duty_cycle(0)   
con.print_results()
    
