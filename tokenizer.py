import tiktoken

enc= tiktoken.encoding_for_model("gpt-4")

text="My name is amrit kumar, here i am trying to tokenize text"

encoded=enc.encode(text)

print("Encoded text:", encoded)

decoded=enc.decode(encoded)

print("Decoded text:", decoded)
