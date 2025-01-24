#!/usr/bin/env python3
"""
Simple I/O Program
Prompts for user name and provides greeting output.
"""

def get_user_name() -> str:
    """
    Get user name from standard input with validation.
    
    Returns:
        str: Validated user name
        
    Raises:
        ValueError: If user enters empty string
    """
    name = input("Please enter your name: ").strip()
    if not name:
        raise ValueError("Name cannot be empty")
    return name

def create_greeting(name: str) -> str:
    """
    Create formatted greeting string.
    
    Args:
        name (str): User's name
        
    Returns:
        str: Formatted greeting
    """
    return f"Hello {name}"

def main():
    """Main program flow."""
    try:
        name = get_user_name()
        greeting = create_greeting(name)
        print(greeting)
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()