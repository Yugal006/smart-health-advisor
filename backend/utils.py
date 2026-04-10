#backend/utils.py

def generate_avatar(name):
    if not name:
        return "U"
    
    parts = name.strip().split()
    
    if len(parts) == 1:
        return parts[0][0].upper()
    
    return (parts[0][0] + parts[-1][0]).upper()