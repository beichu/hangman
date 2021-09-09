# Hangman Game

- Player 1 chooses a word
- Display an array of asterist (the same length as the word, but separated by space )
- Player 2 guesses a letter
  - if letter in word: replace the underscores where the letter appears.
  - if letter not in word,  counter += 1
  - if counter == 10:
    - player 1 win
  - if all underscores are replaced
    - player 2 win

```python
word = "hangman"
display = "_ "*len(word)

```



