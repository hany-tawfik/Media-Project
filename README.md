# Media-Project

This code which runs on a Raspberry Pi uses Recurrent Neural Networks to estimate in real time the tempo of the music being played in the background and simultaneously get MIDI messages and notes (will then be converted to chords inside the Pi) from a connected MIDI foot controller then triggers loops from a connected arranger keyboard according to estimated tempo and the chosen chords.

### Prerequisites
You will need a Raspberry Pi (model B was used in development), MIDI controller, arranger keyboard, USB to midi cable and a USB microphone.

### Run

Run the run_me.py file on your Pi then choose the preferred scale by pressing the equivalent major tone key on the connected MIDI keyboard.

### Built With

This [video](https://photos.app.goo.gl/2r6bahSFW8lDBydK2) explains and tests the project. This [one](https://photos.app.goo.gl/JfKqiHgg0CiIBAF03) uses the system with real song.
