import madmom as mm
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile

np.set_printoptions(precision=4, linewidth=256,suppress=True,threshold=1500)
tempoEstimation = mm.features.tempo.TempoEstimationProcessor(min_bpm=40, max_bpm=180, fps=100)


rate, samples = scipy.io.wavfile.read('output_02.wav')
# rate, samples = scipy.io.wavfile.read('SunStormWater.wav')
# rate, samples = scipy.io.wavfile.read('Afuera.wav')
# rate, samples = scipy.io.wavfile.read('HipHop.wav')
# rate, samples = scipy.io.wavfile.read('NationalTrust.wav')
# rate, samples = scipy.io.wavfile.read('Snowboarding.wav')

initSeconds = rate*10
diffSecFromInit = rate*2.5  #how many seconds after initSeconds
finalSeconds = np.uint32(initSeconds + diffSecFromInit)

print "Rate: ", rate
print "initSeconds: ", initSeconds
print "finalSeconds: ", finalSeconds

remixSamples = mm.audio.signal.remix(samples[initSeconds:finalSeconds], 1)

print "Total Samples to Process: ", remixSamples.shape

#######Spectogram#########
spec = mm.audio.spectrogram.Spectrogram(remixSamples)

#######Spectral Flux#########
specf = mm.features.onsets.spectral_flux(spec)
tempo = tempoEstimation.process(specf)
print "tempo using Spectral Flux: \n", tempo

#######Super Flux#########
superf = mm.features.onsets.superflux(spec)
tempo = tempoEstimation.process(superf)
print "tempo using Super Flux: \n", tempo

#######RNN Onset#########
proc = mm.features.beats.RNNBeatProcessor()
beats = proc(remixSamples)
tempo = tempoEstimation.process(beats)  # tempo = tempoEstimation.process(beats / beats.max())

print "tempo using RNN: \n ", tempo

# plt.figure()
# plt.imshow(spec[:, :200].T, origin='lower', aspect='auto')
# plt.title("Spectogram")

plt.figure()
plt.plot(remixSamples)
plt.title("remixSamples")

plt.figure()
plt.plot(specf / specf.max())
plt.title("Spectral flux")

plt.figure()
plt.plot(superf / superf.max())
plt.title("Super flux")

plt.figure()
plt.plot(beats/ beats.max())
plt.title("Beats by RNN")



plt.show()
