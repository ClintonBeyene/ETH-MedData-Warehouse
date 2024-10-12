import re

def extract_product_name(message):
    """
    Extracts the product name and weight from a given message.
    
    Args:
    message (str): The message containing the product name.
    
    Returns:
    tuple: The extracted product name and weight, or None if no match is found.
    """
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
    
    return product_name, weight

def extract_product_description(message):
    """
    Extracts the product description from a given message.
    
    Args:
    message (str): The message containing the product description.
    
    Returns:
    str: The extracted product description, or None if no match is found.
    """
    # Regular expression pattern to capture sentences followed by a period or newline
    pattern = r'([A-Za-z\s]+)[.|\n]'
    match = re.search(pattern, message)
    if match:
        return match.group(1).strip()
    else:
        return None

def extract_price(message):
    """
    Extracts the price from a given message.
    
    Args:
    message (str): The message containing the price information.
    
    Returns:
    str: The extracted price in birr, or None if no match is found.
    """
    lines = message.split('\n')
    for line in lines:
        match = re.search(r'price ([\d,]+) birr', line)
        if match:
            return match.group(1)
    return None

def extract_telegram_address(message):
    """
    Extracts the Telegram address from a given message.
    
    Args:
    message (str): The message containing the Telegram address.
    
    Returns:
    str: The extracted Telegram address, or None if no match is found.
    """
    # Regular expression pattern to capture Telegram addresses
    pattern = r'https://t.me/\S+'
    match = re.search(pattern, message)
    if match:
        return match.group(0).strip()
    else:
        return None

def extract_address(message):
    """
    Extracts the address from a given message.
    
    Args:
    message (str): The message containing the address.
    
    Returns:
    str: The extracted address, or None if no match is found.
    """
    lines = message.split('\n')
    for line in lines:
        if "infront of" in line or "near" in line or "address:" in line:
            return line.strip()
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
    pattern = r'\b\d{10}\b'
    match = re.search(pattern, message)
    if match:
        return match.group(0).strip()
    else:
        return None


def extract_open_day_and_time(message):
    """
    Extracts the open day and time from a given message.
    
    Args:
    message (str): The message containing the open day and time.
    
    Returns:
    str: The extracted open day and time, or None if no match is found.
    """
    lines = message.split('\n')
    for line in lines:
        if "open" in line and "from" in line and "until" in line:
            return line.strip()
        elif "ከሰኞ" in line and "እስከ" in line and "ከጧቱ" in line and "ምሽቱ" in line:
            return line.strip()
    return None

def extract_delivery_fee(message):
    """
    Extracts the delivery fee from a given message.
    
    Args:
    message (str): The message containing the delivery fee.
    
    Returns:
    str: The extracted delivery fee, or None if no match is found.
    """
    # Regular expression pattern to capture delivery fee
    pattern = r'for delivery option fees are from ([0-9]+) birr - ([0-9]+) birr'
    match = re.search(pattern, message)
    if match:
        return f"{match.group(1)} - {match.group(2)} birr"
    else:
        return None


# Define a function to remove emojis
def remove_emojis(text):
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
    return emoji_pattern.sub(r'', text)