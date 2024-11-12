
import pyautogui


if __name__ == "__main__":
    X = 2293
    Y = 1392

    end_x = 92
    end_y = Y

    #x, y =  pyautogui.position()
    pyautogui.moveTo(X, Y)
    pyautogui.mouseDown()

    pyautogui.moveTo(end_x, end_y, duration=10)
    pyautogui.mouseUp()


    #print(x,y)
