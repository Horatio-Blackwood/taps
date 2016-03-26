import parser

sentence = 'Throw Dirty rock at the mangey goblin'
print("testing input stentence:", sentence)

ip = parser.InputParser()
ip.parse_input(sentence)