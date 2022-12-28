import numpy as np
import cv2
import cmath


def get_spectrum(frame):
    #frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_CUBIC)

    ft_frame = np.fft.fftshift(np.fft.fft2(frame))
    ft_frame = np.log(np.abs(ft_frame))
    ft_frame = np.ubyte(255*ft_frame/np.max(ft_frame))

    return ft_frame
