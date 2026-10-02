class Calculator:
    @staticmethod
    def multiply(a: int, b: int)-> int:
        """
        Multiply two integers:

        Args:
            a (int): The first integer:
            b (int): The Second integer:
        
        Returns:
            int: The product of a and b.
        """
        return a * b


    @staticmethod
    def calculate_tools(*x: float) -> float:
        """
        Calculate the sum of the given list of numbers

        Args:
            x (list): List of floating numbers

        Returns:
            flaot: The sum of numbers in the list x    
        """
        return sum(x)

    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """
        Calculate daily budget
        Args:
            total (flaot): Total cost.
            days (int): Total number of days

        Returns:
            float: Expense for a single day    
        
        """
        return total/days if days > 0 else 0 