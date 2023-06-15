# Convert datetime object into a string formatted as MM/DD/YY
def format_date(date):
  return date.strftime('%m/%d/%y')

# Removes extraneous info from URL string and leaves only domain name
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# Add s to word if more than 1
def format_plural(amount, word):
  if amount != 1:
    return word + 's'
  
  return word