def box_text(text, padding=1):
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    
    # Top border
    top = '┌' + '─' * (max_length + 2 * padding) + '┐'
    
    # Middle lines
    middle = []
    for line in lines:
        middle.append('│' + ' ' * padding + line.ljust(max_length) + ' ' * padding + '│')
    
    # Bottom border
    bottom = '└' + '─' * (max_length + 2 * padding) + '┘'
    
    # Combine everything into a single string
    return '\n'.join([top] + middle + [bottom])

