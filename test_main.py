import parser

sentence = 'Throw Dirty rock at that mangey old goblin'
print("testing input stentence:", sentence)

ip = parser.InputParser()
ip.parse_input(sentence)