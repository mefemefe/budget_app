class Category:
  
  def __init__(self, category):
    self.category = category
    self.ledger = []
  
  def __str__(self):
    LENGTH = 30
    titlelength = int(LENGTH - len(self.category))
    output = ''
    title = ''
    # determine title
    if titlelength % 2 == 0:
      title = '*' * int(titlelength / 2) + self.category + '*' * int(titlelength / 2)
    else:
      title = '*' * (int(titlelength / 2) + 1) + self.category + '*' * int(titlelength / 2)
    output += title + '\n'
    # determine items 
    for line in self.ledger:
      description = ''
      if len(line.get('description')) > 23:
        description = line.get('description')[:23]
      else:
        description = line.get('description')
      amount = format((line.get('amount')), '.2f')
      if len(amount) > 7:
        amount = '~' + amount[:6]
      space = LENGTH - len(description) - len(amount)
      # add to output
      output += description + ' ' * space + amount + '\n'
    # determine total
    total = format((self.get_balance()), '.2f')
    output += f'Total: {total}'
    #return
    return output
      

  # Deposit 
  def deposit(self, amount, description=''):
    self.ledger.append({'amount': amount, 'description': description})
    return True

  # Withdraw
  def withdraw(self, amount, description=''):
    if self.check_funds(amount) == False:
      return False
    else:
      self.ledger.append({'amount': (0 - amount), 'description': description})
      return True

  # Get balance
  def get_balance(self):
    self.balance = 0
    for line in self.ledger:
      self.balance += line.get('amount')
    return self.balance

  # Transfer 
  def transfer(self, amount, other):
    if self.check_funds(amount) == False:
      return False
    else:
      self.ledger.append({'amount': (0 - amount), 'description': f'Transfer to {other.category}'})
      other.deposit(amount, f'Transfer from {self.category}')
      return True 

  # Check funds 
  def check_funds(self,amount):
    balance = self.get_balance()
    if amount > balance:
      return False
    else:
      return True

  # Total Spent 
  def total_spent(self):
    total = 0
    for line in self.ledger:
      if line.get('amount') < 0:
        total -= line.get('amount')
    return total 


def create_spend_chart(categories):
  totals = []
  total = 0
  number = 0
  percentages = []
  for category in categories:
    totals.append(category.total_spent())
    number += 1
    total += category.total_spent()
  for number in totals:
    percentages.append(int(((number * 100) / total) / 10))
  
  longest_name = ''
  for category in categories:
    if len(category.category) > len(longest_name):
      longest_name = category.category

  # Upper half of chart 
  lines = ['  0| ', ' 10| ', ' 20| ', ' 30| ', ' 40| ', ' 50| ', ' 60| ', ' 70| ', ' 80| ', ' 90| ', '100| ']
  for percentage in percentages:
    for i in range(0,11):
      if percentage >= i:
        lines[i] += 'o  '
      else:
        lines[i] += '   '
  decoration = '    -'
  for category in categories:
    decoration += '---'
  
  # Lower half of chart 
  lower_half = ''
  for i in range(len(longest_name)):
    lower_half += '     '
    for category in categories:
      try:
        lower_half += category.category[i] + '  '
      except:
        lower_half += '   '
    if i == (len(longest_name) - 1):
      pass
    else:  
      lower_half += '\n'

  lines.reverse()
  output = 'Percentage spent by category\n'
  for line in lines:
    output += line + '\n'
  output += decoration + '\n'
  output += lower_half

  return output