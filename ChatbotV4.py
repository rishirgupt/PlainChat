# Travel Chatbot Program V4 - Memory Enabled with NLP and Text-to-Speech 

# Task  Enhancements Summary:
# ================================
# 1. Memory and Context Handling: The chatbot now remembers the last topic discussed and can provide follow-up information when the user asks related questions. This allows for more natural, multi-turn conversations.
# 2. Improved NLP with Stemming: The chatbot uses stemming to better match user input
#    with keywords in the knowledge base, allowing it to understand variations of words (e.g., "arrive", "arriving", "arrival").
# 3. Text-to-Speech Integration: The chatbot can now speak its responses using the
#    pyttsx3 library, providing an auditory response in addition to text.


import csv
from gettext import install
import sys
import subprocess
from collections import defaultdict
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import random
import pyttsx3

# Remove hash comments for installation of required libraries if not already installed

#def install(package):
#    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#install('nltk')
#install('pyttsx3')
#install('punkt_tab')
#install('punkt')
#install('stopwords')
#install('averaged_perceptron_tagger')
#install('sapi5')



class TravelChatbot:
    # Initialize the chatbot with knowledge base from CSV
    def __init__(self, csv_file='KeywordsV6.csv'):
        # Store intent -> keywords and response
        self.knowledge_base = {}
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.load_knowledge_base(csv_file)

        self.memory = {}
        self.turn_counter = 0
        self.MAX_TURNS = 5  
        
    def load_knowledge_base(self, csv_file):
        """Load questions and responses from CSV file"""

        with open(csv_file, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    #Initialize of intent from csv file
                    intent = row['intent'].lower()
                    # Split keywords by '|'
                    keywords = row['keywords'].split('|')
                    # Initialize of response from csv file
                    response = row['response'].split('|')
                    # initialize of reply from csv file
                    reply = row['reply'].split('|')
                    self.knowledge_base[intent] = {
                        'keywords': keywords,
                        'response': response,
                        'reply': reply
                    }
    
    def preprocess_text(self, text):
        # Basic preprocessing: lowercase, tokenization, stopword removal, stemming

        # Convert to lowercase
        text = text.lower()
        tokens = word_tokenize(text)
        
        # Stem the tokens for better keyword matching
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        
        return tokens, stemmed_tokens
    
    def find_matching_intent(self, user_input):
        #Basic keyword matching with scoring system to find best intent match
        tokens, stemmed_tokens = self.preprocess_text(user_input)

        # Converting to tokens for faster lookup
        token_set = set(tokens)
        stemmed_set = set(stemmed_tokens)
        
        best_match = None
        best_score = 0
        
        # Check each intent with score in the knowledge base for keyword matches
        for intent, data in self.knowledge_base.items():
            keywords = data['keywords']
            match_score = 0
            
            # Check each keyword variation for this intent and calculate score
            for keyword in keywords:
                keyword_lower = keyword.lower()
                keyword_stemmed = self.stemmer.stem(keyword_lower)
                
                # Check if keyword is in tokens (direct match)
                if keyword_lower in token_set:
                    match_score += 2
                    
                # Check stemmed matching (word variations)
                elif keyword_stemmed in stemmed_set:
                    match_score += 1
                    
                if match_score > 0:
                        break 
                match_score = 0

            if match_score > best_score:
                best_score = match_score
                best_match = intent
                #print(f"Debug: Intent '{intent}' has match score {match_score}")
                #print(f"Debug: token_set = {token_set}")
                #print(f"Debug: stemmed_set = {stemmed_set}")
                #print(f"Debug: keyword = {keyword}")
            
        # Return intent only if we have a meaningful match
        return best_match if best_score > 0 else None

    def get_response(self, user_input):
        self.turn_counter += 1
        if self.turn_counter > self.MAX_TURNS:
            self.memory.clear()
            self.turn_counter = 0        

        follow_up_tokens = ['when', 'who', 'what', 'time', 'where', 'arrive', 'status','it','how','more','details','information','next']
        tokens, stemmed_tokens = self.preprocess_text(user_input)
        
        # Stem follow-up tokens for matching
        stemmed_follow_up = [self.stemmer.stem(t) for t in follow_up_tokens]
        
        # Check both raw and stemmed tokens
        is_follow_up = bool((set(follow_up_tokens) & set(tokens)) or (set(stemmed_follow_up) & set(stemmed_tokens)))
        #print(f"Debug: is_follow_up = {is_follow_up}, tokens = {tokens}, stemmed = {stemmed_tokens}")
        
        # Find matching intent
        matching_intent = self.find_matching_intent(user_input)
        
        #print(f"Debug: matching_intent = {matching_intent}")
        #print(f"Debug: memory = {self.memory}")
        #print(f"Debug: Checking follow-up - is_follow_up={is_follow_up}, has_memory={'last_intent' in self.memory}")
       
        if is_follow_up and 'last_intent' in self.memory:
            last_topic = self.memory['last_intent']
            acknowledgments = [
                "I’ve got a bit more detail for you:",
                "Here’s the next part:",
                "This should help:",
            ]
            acknowledgment = random.choice(acknowledgments)
            response_text = random.choice(self.knowledge_base[last_topic]['reply'])
            #print(f"Debug: Using memory for follow-up on topic '{last_topic}'")
            return f"{acknowledgment} {response_text}"
        
        if matching_intent is not None:
            # New topic; Save to memory and reset counter
            self.memory['last_intent'] = matching_intent 
            self.turn_counter = 0
            responses = self.knowledge_base[matching_intent]['response']
            #print(f"Debug: Found intent '{matching_intent}'")
            return random.choice(responses)
        
        # Use Memory if it's a follow-up and no new intent was found
        
        # No intent found and not a follow-up
        return "I'm sorry, I don't have information on that. Try asking about check-in, flights, visas, or any other travel-related question! Type 'help' to see available topics."

    def display_help(self):
        #help function to show available topics
        topics = sorted(list(self.knowledge_base.keys()))
        print("\n" + "="*60)
        print("I can help you with these travel topics:")
        print("="*60)
        for i, topic in enumerate(topics, 1):
            print(f"{i:2}. {topic}")
        print("="*60 + "\n")

    def speak_response(self, response):
        # Use pyttsx3 to speak the response
        try:
            engine = pyttsx3.init()
            rate = engine.getProperty('rate')
            # Slow down speech rate for clarity
            #engine.setProperty('rate', int(rate * 3))
            engine.say(response)
            engine.runAndWait()
        except Exception as e:
            print(f"[Warning] Text-to-speech failed: {e}")

def main():
    #NAME and WELCOME MESSAGE
    print("\n" + "="*60)
    print("TRAVEL CHATBOT V4 - Memory-Enabled with NLP and Text-to-Speech")
    print("="*60)
    print("Ask me anything about travel and hospitality!")
    print("Type 'help' to see topics, 'bye' to exit\n")
    
    chatbot = TravelChatbot('KeywordsV6.csv')
    
    # Conversation loop
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'bye':
            print("\nChatbot: Goodbye! Have a wonderful trip! Safe travels!\n")
            break
        
        if user_input.lower() == 'help':
            chatbot.display_help()
            continue
        
        if not user_input:
            print("Chatbot: Please ask a question!\n")
            continue
        
        response = chatbot.get_response(user_input)
        print(f"Chatbot: {response}\n")
        chatbot.speak_response(response)
        #print(f"Debug: Preprocessed text for '{user_input}': {chatbot.preprocess_text(user_input)}")
        
if __name__ == "__main__":
    main()
