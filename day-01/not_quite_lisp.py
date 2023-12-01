
if __name__ == "__main__":
    with open('input.txt') as f:
        # a
        data = f.read()
        
        up = data.count('(')
        down = data.count(')')

        print(f"Floor: {up - down}")

        # b
        pos = 1
        height = 0
        for char in data:
            if char == '(':
                height += 1
            
            elif char == ')':
                height -= 1
                if height == -1:
                    break
            
            pos += 1

        print(f'Position: {pos}')
