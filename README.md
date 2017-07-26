# Epub Words Highlighter

Epub Words Highlighter highlights all the words from a provided list of words. Give it a epub file (test/test.epub) and a file (list) containing list of words, and it will make them ***bold and italic*** for you in all the chapters, all the paragraphs. What's more, it will even make those ***CAPS*** so that you do not miss them by any chancce!

There is also the mode to not only highlight, but also to include meanings of the words.
The words should be listed in this this way:

```
aberrant,-,(adjective) markedly different from an accepted norm
aberration,-,(noun) a deviation from what is normal or expected

```

The `,-,` is the delimiter here.

Why? This will probably be useful for English Proficiency Test Participants, like GRE, IELTS and so on.

(This will probably not be supported in near or distant future. I created it on a whim as a weekend pet project with no particular ambition. If you want to fork and improve it - by all means, go for it!)

## Sample

|Previous | After |
| :--- | :--- |
| All the officer patients in the ward were forced to censor letters written by all the enlisted-men patients, who were kept in residence in wards of their own. It was a monotonous job, and Yossarian was disappointed to learn that the lives of enlisted men were only slightly more interesting than the lives of officers. After the first day he had no curiosity at all. To break the monotony he invented games. | All the officer patients in the ward were forced to ***CENSOR*** letters written by all the enlisted-men patients, who were kept in residence in wards of their own. It was a monotonous job, and Yossarian was disappointed to learn that the lives of enlisted men were only slightly more interesting than the lives of officers. After the first day he had no curiosity at all. To break the ***MONOTONY*** he invented games. |
*Sample taken from catch-22 for demonstration*

## Sample with Meaning

|Previous | After |
| :--- | :--- |
| Censoring the envelopes had serious repercussions, produced a ripple of anxiety on some ETHEREAL military echelon that floated a C.I.D. man back into the ward posing as a patient. They all knew he was a C.I.D. man because he kept inquiring about an officer named Irving or Washington and because after his first day there he wouldn't censor letters. | Censoring the envelopes had serious repercussions, produced a ripple of anxiety on some ***ETHEREAL*** [(adjective) characterized by lightness and insubstantiality] military echelon that floated a C.I.D. man back into the ward posing as a patient. They all knew he was a C.I.D. man because he kept inquiring about an officer named Irving or Washington and because after his first day there he wouldn't ***CENSOR*** [(verb) to examine and remove objectionable material] letters. |
*Sample taken from catch-22 for demonstration*

## Requirements

- Python3
- Pygtk-3

And probably Linux. This was created and tested in Linux.