import madmom as mm
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile


np.set_printoptions(precision=4, linewidth=256,suppress=True,threshold=1500)


# samples, rate = mm.audio.ffmpeg.load_ffmpeg_file('The_Wolf.m4a')
rate, samples = scipy.io.wavfile.read('output.wav')
# rate, samples = scipy.io.wavfile.read('SunStormWater.wav')

print "Samples :\n", samples.shape

# remixSamples = samples

# remixSamples = mm.audio.signal.remix(samples[2425500:2646000], 1)
remixSamples = mm.audio.signal.remix(samples[:rate*10], 1)

print "remixSamples :\n", remixSamples.shape

spec = mm.audio.spectrogram.Spectrogram(remixSamples)

# filt_spec = mm.audio.spectrogram.FilteredSpectrogram(spec, filterbank=mm.audio.filters.LogFilterbank, num_bands=24)

print "spec.shape :\n", spec.shape
specf = mm.features.onsets.spectral_flux(spec)
sf = mm.features.onsets.superflux(spec)

print "sf.shape :\n", sf.shape

proc = mm.features.beats.RNNBeatProcessor()

beats = proc(remixSamples)
print "beats.shape :\n", beats.shape
print "np.amax(beats) :\n", np.amax(beats)
print "beats :\n", beats

# plt.figure()
# plt.imshow(filt_spec.T, origin='lower', aspect='auto')
# plt.title("Filtered Spectogram")

plt.show()
plt.plot(beats/ beats.max())
plt.title("Beats by RNN")

plt.figure()
plt.imshow(spec[:, :200].T, origin='lower', aspect='auto')
plt.title("Spectogram")

plt.figure()
plt.plot(specf / specf.max())
plt.title("Spectral flux")

plt.figure()
plt.plot(sf / sf.max())
plt.title("Super flux")

plt.show()
