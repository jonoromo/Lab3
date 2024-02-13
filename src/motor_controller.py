class Controller:
    
    def __init__(self, k_p, sp):
        self.k_p = k_p
        self.sp = sp
        
    def run(self, sp, act):
        PWM = self.k_p*(sp - act)
        return PWM
    
    def set_setpoint(self, sp):
        self.sp = sp
        
    def set_Kp(self, k_p):
        self.k_p = k_p
    
if __name__ == "__main__":
    import motor_driver as moto
    import encoder_reader
    import utime
    
    enPin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP) # Initialize pin en_pin (PA10)
    in2_pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP) # Initialize pin in2_pin (PB5)
    in1_pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP) # Initialize pin in1_pin (PB4)
    timmy = pyb.Timer(3, freq=20000) # Initialize timer
    ch_pos = timmy.channel(2, pyb.Timer.PWM, pin=in2_pin) # Initialize positive direction timer channel
    ch_neg = timmy.channel(1, pyb.Timer.PWM, pin=in1_pin) # Initialize negative direction timer channel
    
    moe = moto.MotorDriver(enPin, in2_pin, in1_pin, timmy, ch_pos, ch_neg)
    
    pinA = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=pyb.Pin.AF1_TIM2)
    pinB = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=pyb.Pin.AF1_TIM2)

    timer = pyb.Timer(8, prescaler=1, period=65535)
    chan_A = timer.channel(1, pyb.Timer.ENC_AB, pin=pinA)
    chan_B = timer.channel(2, pyb.Timer.ENC_AB, pin=pinB)
    
    enc = encoder_reader.Encoder(pinA, pinB, timer, chan_A, chan_B)
    
    con = Controller(0.1, 10000)
    while True:
        moe.set_duty_cycle(con.run(10000,enc.read()))
        utime.sleep_ms(10)
        