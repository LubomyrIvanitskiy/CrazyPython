from multiline_lambda import multiline, For, If, is_not_empty

sentences = [
    "To be, or not to be, that is the question",
    "Whether 'tis nobler in the mind to suffer",
    "The slings and arrows of outrageous fortune,",
    "Or to take arms against a sea of troubles",
    "And by opposing end them. To die—to sleep,"
]

##################################################
# Filtering out the sentences containing 'or' word
##################################################

filtered = filter(
    multiline(lambda item: (
        words := item.split(),
        result := For(enumerate(words))(lambda i, word: (
            If(
                word.lower().strip() == 'or',
                Then=lambda: False,
                Else=lambda: ...  # means continue
            )
        )),
        result if is_not_empty(result) else True
    )),
    sentences
)

print(list(filtered))

# prints:
# [
#   "Whether 'tis nobler in the mind to suffer",
#   'The slings and arrows of outrageous fortune,',
#   'And by opposing end them. To die—to sleep,'
# ]
