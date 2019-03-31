import scipy.io.wavfile as siw
import scipy as sp
from scipy.signal import decimate
import numpy
import matplotlib.pyplot as plt
import copy
import sys
import warnings

# wyłączenie warningów
warnings.filterwarnings("ignore")

BORDER = 175

def loadAudio(filename):
    w, signal = siw.read(filename)
    return w, signal

# wycina fragment od 1/3 do 2/3 długości całego dźwięku
def trimSignal(signal):
    return signal[int(len(signal) / 3): int(len(signal) / 3 * 2)]


def main():
    if len(sys.argv) < 2:
        print("podaj sciezke do pliku!")
        exit()
    filename = sys.argv[1]
    w, signal = loadAudio(filename)

    # bierzemy tylko jeden kanał
    if isinstance(signal[0], numpy.ndarray):
        signal = [s[0] for s in signal]

    # przycinanie sygnału
    while len(signal) > 35000:
        signal = trimSignal(signal)

    signal1 = sp.fft(signal)
    signal1 = abs(signal1)
    signal2 = copy.copy(signal1)

    n = len(signal1)

    signal1decimated = copy.copy(signal1)
    for i in range(2,4):
        signal1decimated = decimate(signal1decimated, i)
        signal2[:len(signal1decimated)] *= signal1decimated

    freq50Hz = int(50*float(n)/w) # indeks odpowiadający 50Hz w sygnale; częstotliwość(50)->indeks
    signalOver50Hz = signal2[freq50Hz:] # sygnał z odciętą częścią <50Hz
    peakid = numpy.argmax(signalOver50Hz) # znajduje peak
    f = (freq50Hz + peakid)/(float(n))*w # uzupelnienie indeksu o odcieta część i obliczenie częstotliwości; indeks->częstotliwość
    # print("f = ",f)

    if f <= BORDER:
        gender = 'M' # mężczyzna
    else:
        gender = 'K' # kobieta
    print(gender)


if __name__ == '__main__':
    main()