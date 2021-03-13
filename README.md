# explorer
tonal music analysis

the midi-to-matrix part is a tonnetz (https://en.wikipedia.org/wiki/Tonnetz) whith fifths in the x-axis and (major) thirds in the y axis.

connect midi input (with aconnect for example) to the analyser and you will see the notes you play in the tonnetz. it can help you to understand music. maybe.

the other part is an experiment to transform mic input into midi notes. it's note very accurate for now because it's mainly do-it-myself

todo: add scipy interpolation to add precision to the mic-to-midi part

add chromatic circle to the matrix part
