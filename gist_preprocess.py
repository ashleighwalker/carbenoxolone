import numpy as np
from scipy.signal import butter, filtfilt

def preprocess_motor_pattern(self, high=300, tau=50, time_slice=None):
        # preprocess a numpy array containing motor pattern signals 
        # (chan x samples)
        if time_slice is None:
            start, stop = self.t_start, self.t_stop
        else:
            start, stop = time_slice
        if self.motor is None:
            if self.reader.sln:
                self.motor = self.reader.get_motor_pattern(time_slice=(start, stop), remove_artifacts=True)
            else:
                self.motor = self.reader.get_motor_pattern(time_slice=(start, stop))
        if not self.fs:
            self.get_fs()
        if not self.integrated_motor_pattern:
            b, a = butter(3, high, btype = 'highpass', fs=self.fs)
            high_pass_motor_pattern = filtfilt(b, a, self.motor)
            wn = int(tau * 1e-3 * self.fs)
            b = 1/wn * np.ones(wn)
            a = 1
            self.motor = filtfilt(
                b, a, np.abs(high_pass_motor_pattern), padtype='even')
            # self.integrated_motor_pattern = True
            return self.integrated_motor_pattern
        else:
            return None