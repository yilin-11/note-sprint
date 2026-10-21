# NoteSprint

A phone-first trainer for reading notes on the treble and bass staff.

**Live demo: https://yilin-11.github.io/note-sprint/**

A note appears on the staff, you tap its name, and the keyboard below lights up the key so the staff and the piano connect in your head. The goal is to name every note in under 2 seconds.

## Features

- **Practice sets that grow with you**: right-hand C position, left-hand C position, both hands, G position, then the whole treble, bass or grand staff. The sets follow the order of most beginner method books.
- **Landmark hints**: when you miss, it tells you how to count from the nearest landmark note (middle C, treble G, bass F, C3, C5).
- **Keyboard view**: every answer lights up the key, with middle C marked.
- **Adaptive**: notes you miss come up more often.
- **Round stats**: accuracy, average time, share answered within 2 seconds, and the notes you missed. Pass a set at 90% accuracy and under 2 seconds on average.
- **Sound**: each answer plays the note (toggle it off for quiet practice).
- **No sign-up, no build step**: one HTML file. Progress is stored in your browser's `localStorage`.

On a computer you can answer with the keys `C D E F G A B`, and press `Enter` to continue after a miss.

## Run it locally

Open `index.html` in a browser. That's it.

## Deploy

The repo is set up for GitHub Pages: Settings → Pages → Deploy from branch → `main` / root.

## License

MIT
