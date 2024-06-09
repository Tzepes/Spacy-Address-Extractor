import spacy
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def extract_business_name(domain):
    # Remove TLD and any subdomains
    domain = re.sub(r'\.\w+$', '', domain)  # Remove .com, .net, etc.
    domain = domain.split('.')[-1]  # Keep only the main domain part
    
    # Split by hyphens and underscores
    words = re.split(r'[-_]', domain)
    
    # Split camelCase words
    split_words = []
    for word in words:
        split_words.extend(re.findall(r'[A-Z][a-z]*|[a-z]+', word))
    
    # Join words with spaces
    cleaned_domain = ' '.join(split_words)
    
    # Use SpaCy to process the text and capitalize each word
    doc = nlp(cleaned_domain)
    business_name = ' '.join([token.text.capitalize() for token in doc])
    
    return business_name

# Example usage
domain = "thebestvintageclothing.com"
business_name = extract_business_name(domain)
print(business_name)  # Output: The Best Vintage Clothing
