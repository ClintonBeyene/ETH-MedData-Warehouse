import re
import logging

# Set up logging
logging.basicConfig(
    filename='../logs/scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_product_name(message):
    """
    Extracts the product name and weight from a given message.
    
    Args:
    message (str): The message containing the product name.
    
    Returns:
    tuple: The extracted product name and weight, or None if no match is found.
    """
    try:
        logging.debug('Extracting product name')
        lines = message.split('\n')
        product_name = lines[0].strip()
        
        # Check if the product name contains a weight
        match = re.search(r'(\d+(?:\.\d+)?(?:mg|g|kg|gm|lbs|oz|ml|l|pieces|tablets|capsules))', product_name)
        
        # Check if the product name contains a price or currency amount
        begin = re.search(r'price amount  birr amount etb ብር', product_name)
        
        if match:
            # If a weight is found, extract it and remove it from the product name
            weight = match.group(0)
            product_name = product_name.replace(weight, '').strip()
        elif begin:
            # If a price or currency amount is found, return None as the product name
            product_name = None
        else:
            # If no weight or price/currency amount is found, return None as the weight
            weight = None
        
        logging.info('Product name and weight extracted successfully')
        return product_name, weight
    except Exception as e:
        logging.error('Error extracting product name: %s', e)
        return None, None

def extract_product_description(message):
    """
    Extracts the product description from a given message.
    
    Args:
    message (str): The message containing the product description.
    
    Returns:
    str: The extracted product description, or None if no match is found.
    """
    try:
        logging.debug('Extracting product description')
        # Regular expression pattern to capture sentences followed by a period or newline
        pattern = r'([A-Za-z\s]+)[.|\n]'
        match = re.search(pattern, message)
        if match:
            logging.info('Product description extracted successfully')
            return match.group(1).strip()
        else:
            logging.info('No product description found')
            return None
    except Exception as e:
        logging.error('Error extracting product description: %s', e)
        return None

def extract_price(message):
    """
    Extracts the price from a given message.
    
    Args:
    message (str): The message containing the price information.
    
    Returns:
    str: The extracted price in birr, or None if no match is found.
    """
    try:
        logging.debug('Extracting price')
        lines = message.split('\n')
        for line in lines:
            match = re.search(r'price ([\d,]+) birr', line)
            if match:
                logging.info('Price extracted successfully')
                return match.group(1)
        logging.info('No price found')
        return None
    except Exception as e:
        logging.error('Error extracting price: %s', e)
        return None

def extract_telegram_address(message):
    """
    Extracts the Telegram address from a given message.
    
    Args:
    message (str): The message containing the Telegram address.
    
    Returns:
    str: The extracted Telegram address, or None if no match is found.
    """
    try:
        logging.debug('Extracting Telegram address')
        # Regular expression pattern to capture Telegram addresses
        pattern = r'https://t.me/\S+'
        match = re.search(pattern, message)
        if match:
            logging.info('Telegram address extracted successfully')
            return match.group(0).strip()
        else:
            logging.info('No Telegram address found')
            return None
    except Exception as e:
        logging.error('Error extracting Telegram address: %s', e)
        return None

def extract_address(message):
    """
    Extracts the address from a given message.
    
    Args:
    message (str): The message containing the address.
    
    Returns:
    str: The extracted address, or None if no match is found.
    """
    try:
        logging.debug('Extracting address')
        lines = message.split('\n')
        for line in lines:
            if "infront of" in line or "near" in line or "address:" in line:
                logging.info('Address extracted successfully')
                return line.strip()
        logging.info('No address found')
        return None
    except Exception as e:
        logging.error('Error extracting address: %s', e)
        return None

def extract_phone_number(message):
    """
    Extracts the phone number from a given message.
    
    Args:
    message (str): The message containing the phone number.
    
    Returns:
    str: The extracted phone number, or None if no match is found.
    """
    # Regular expression pattern to capture phone numbers
    try:
        logging.debug('Extracting Phone Number')
        pattern = r'\b\d{10}\b'
        match = re.search(pattern, message)
        if match:
            logging.info('Phone Number extracted successfully')
            return match.group(0).strip()
        else:
            logging.info('No phone number found')
            return None
    except Exception as e:
        logging.error('Error extracting phone number: %s', e)

def extract_open_day_and_time(message):
    """
    Extracts the open day and time from a given message.
    
    Args:
    message (str): The message containing the open day and time.
    
    Returns:
    str: The extracted open day and time, or None if no match is found.
    """
    try:
        logging.debug('Extracting Open Day and Time')
        lines = message.split('\n')
        for line in lines:
            if "open" in line and "from" in line and "until" in line:
                logging.info('Open day and time extracted Successfully')
                return line.strip()
            elif "ከሰኞ" in line and "እስከ" in line and "ከጧቱ" in line and "ምሽቱ" in line:
                logging.info('Open day and time extracted successfully')
                return line.strip()
        logging.info('Open day and time not found')
        return None
    except Exception as e:
        logging.error('Error extracting open day and time: %s', e)

def extract_delivery_fee(message):
    """
    Extracts the delivery fee from a given message.
    
    Args:
    message (str): The message containing the delivery fee.
    
    Returns:
    str: The extracted delivery fee, or None if no match is found.
    """
    # Regular expression pattern to capture delivery fee
    try:
        logging.debug('Extracting delivery fee')
        pattern = r'for delivery option fees are from ([0-9]+) birr - ([0-9]+) birr'
        match = re.search(pattern, message)
        if match:
            logging.info('Delivery fee extracted successfully')
            return f"{match.group(1)} - {match.group(2)} birr"
        else:
            logging.info('Delivey fee not found')
            return None
    except Exception as e:
        logging.error('Error extracting delivery fee: %s', e)


# Define a function to remove emojis
def remove_emojis(text):
    try:
        logging.debug('Removing emojis')
        emoji_pattern = re.compile(
            "[" 
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+", 
            flags=re.UNICODE
        )
        logging.info('Emoji is removed')
        return emoji_pattern.sub(r'', text)
    except Exception as e:
        logging.error("Errors when removing emojis")