import java.io.*;
import java.util.Scanner;

/**
 * Class represents the board configuration
 */
public class NPuzzle {
    /**
     * Represents size of board
     */
    protected int[] size = new int[2];

    private static int[][] arr;
    /**
     * Represents coordinates of empty space which is "bb"
     */
    protected int[] coordinatesOfSpace = new int[2];
    /**
     * Represents number of boards that are created so far
     */
    protected static int _numberOfBoards = 0;
    /**
     * Represents last move that a board did
     */
    protected char _lastMove = 'S';
    /**
     * Represents number of moves that user did so far
     */
    protected static int _numberOfMoves = 0;

    /**
     * Constructor of AbstractBoard class
     */
    public NPuzzle() {

        _numberOfBoards++;
    }

    /**
     * Override toString() method
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.getClass().getName() + "\n");
        for (int i = 0; i < size[1]; i++) {
            for (int j = 0; j < size[0]; j++) {
                int index = cell(j, i);
                stringAppend(index, sb);
                sb.append(" ");
            }
            sb.append("\n");
        }
        return sb.toString();
    }

    /**
     * Method that is used for decide size of board and create that board with that
     * size
     * 
     * @param _number1 X axis size of board
     * @param _number2 Y axis size of board
     */
    public void setSize(final int _number1, final int _number2) {

        size[0] = _number1;
        size[1] = _number2;
        reset();

    }

    /**
     * Abstract reset method that will be used by subclasses
     */
    public void reset() {
        int index = 1;
        arr = new int[size[1]][size[0]];
        for (int i = 0; i < size[1]; i++) {
            for (int j = 0; j < size[0]; j++) {
                assign(i, j, index);
                index++;
            }
        }
        assign(size[1] - 1, size[0] - 1, -1);
        coordinatesOfSpace[0] = size[0] - 1;
        coordinatesOfSpace[1] = size[1] - 1;
    }

    /**
     * Abstract readFromFile method that will be used by subclasses
     */
    protected void readFromFile(String nameOfFile) throws IOException {
        try {
			arr = new int[size[1]][size[0]];
            File file = new File(nameOfFile); // Change this to your file name
            Scanner fileReader = new Scanner(file);
            calculateXandY(file);
            int result = 0;
            while (fileReader.hasNext()) {
                for (int i = 0; i < size[1]; ++i) {
                    for (int j = 0; j < size[0]; ++j) {
                        String word = fileReader.next();
                        if (word.equals("bb")) {
                            result = -1;
                            coordinatesOfSpace[0] = j;
                            coordinatesOfSpace[1] = i;
                        } else {
                            result = Integer.parseInt(word);
                        }
                        assign(i, j, result);
                    }
                }
            }
            fileReader.close();
		} catch (IOException e) {
			System.out.printf("IOException\n");
		}
       
    }

    /**
     * Method for write board to .txt file
     * 
     * @param nameOfFile File Name
     * @throws IOException Exception that is thrown when name of file is false
     */
    public void writeToFile(String nameOfFile) throws IOException {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < size[1]; i++) {
            for (int j = 0; j < size[0]; j++) {
                int index = cell(j, i);
                stringAppend(index, sb);
                if (j != size[0] - 1)
                    sb.append(" ");
            }
            if (i != size[1] - 1)
                sb.append("\n");
        }
        String appendedString = sb.toString();
        FileWriter fileWriter = new FileWriter(nameOfFile);
        fileWriter.write(appendedString);
        fileWriter.close();
    }

    /**
     * Abstract move method that will be used by subclasses
     * 
     * @param direction Direction of movement
     */
    public void move(final char direction) {
        int temp, x, y;
        x = coordinatesOfSpace[0];
        y = coordinatesOfSpace[1];
        if (direction == 'L' || direction == 'l') {
            if (isValid('L')) {
                temp = cell(x - 1, y);
                assign(y, x - 1, cell(x, y));
                assign(y, x, temp);
                coordinatesOfSpace[0]--;
            }
        } else if (direction == 'R' || direction == 'r') {
            if (isValid('R')) {
                temp = cell(x + 1, y);
                assign(y, x + 1, cell(x, y));
                assign(y, x, temp);
                coordinatesOfSpace[0]++;
            }
        } else if (direction == 'U' || direction == 'u') {
            if (isValid('U')) {
                temp = cell(x, y - 1);
                assign(y - 1, x, cell(x, y));
                assign(y, x, temp);
                coordinatesOfSpace[1]--;
            }
        } else if (direction == 'D' || direction == 'd') {
            if (isValid('D')) {
                temp = cell(x, y + 1);
                assign(y + 1, x, cell(x, y));
                assign(y, x, temp);
                coordinatesOfSpace[1]++;
            }
        }
        if (isValid(direction)) {
            _lastMove = direction;
            _numberOfMoves++;
            System.out.println("Moved to " + direction);
        }
    }

    /**
     * Protected function that appends strings
     * 
     * @param index Index of board
     * @param sb    String builder
     */
    protected void stringAppend(int index, StringBuilder sb) {
        if (size[0] * size[1] <= 100) {
            if (index == -1) {
                sb.append("bb");
            } else if (index / 10 == 0) {
                sb.append("0" + index);
            } else if (index / 10 >= 1) {
                sb.append(index);
            }
        } else if (size[0] * size[1] > 100 && size[0] * size[1] <= 1000) {
            if (index == -1) {
                sb.append("bb");
            } else if (index / 10 == 0) {
                sb.append("00" + index);
            } else if (index / 100 == 0) {
                sb.append("0" + index);
            } else if (index / 100 >= 1) {
                sb.append(index);
            }
        }
    }

    /**
     * Abstract move method that will be used by subclasses
     * 
     * @param x X index of board
     * @param y Y index of board
     * @return NULL return
     */
    public int cell(int x, int y) {

		try {
			if (x >= 0 && x < size[0] && y >= 0 && y < size[1]) {
				return arr[y][x];
			}
		} catch (IndexOutOfBoundsException exception) {
			System.exit(0);
		}
		return 0;
	}

    /**
     * Represents number of boards
     * 
     * @return Number of boards
     */
    public int numberOfBoards() {
        return _numberOfBoards;
    }

    /**
     * Represents last move
     * 
     * @return Last move
     */
    public int lastMove() {
        return _lastMove;
    }

    /**
     * Represents number of moves
     * 
     * @return Number of moves
     */
    public int numberOfMoves() {
        return _numberOfMoves;
    }

    /**
     * Method that calculates x and y sizes of a file
     * 
     * @param f File
     * @throws IOException Exception that controls input
     */
    protected void calculateXandY(File f) throws IOException {
        Reader r = new BufferedReader(new InputStreamReader(new FileInputStream(f), "US-ASCII"));
        int countY = 0;
        int countX = 0;
        boolean flag = false;
        try {
            int intchar;
            while ((intchar = r.read()) != -1) {
                char ch = (char) intchar;
                if (intchar == '\n') {
                    countY++;
                    countX++;
                    flag = true;
                } else if (ch == ' ') {
                    countX++;
                    flag = false;
                }
            }
        } finally {
            r.close();
            if (!flag) {
                countY++;
                countX++;
            }
            size[0] = countX / countY;
            size[1] = countY;
        }
    }

    /**
     * Method that do validation of move
     * 
     * @param direction Direction of movement
     * @return If movement valid or not
     */
    protected boolean isValid(final char direction) {

        if ((direction == 'L' || direction == 'l') && coordinatesOfSpace[0] - 1 >= 0
                && cell(coordinatesOfSpace[0] - 1, coordinatesOfSpace[1]) != 0) {
            return true;
        } else if ((direction == 'R' || direction == 'r') && coordinatesOfSpace[0] + 1 < size[0]
                && cell(coordinatesOfSpace[0] + 1, coordinatesOfSpace[1]) != 0) {
            return true;
        } else if ((direction == 'U' || direction == 'u') && coordinatesOfSpace[1] - 1 >= 0
                && cell(coordinatesOfSpace[0], coordinatesOfSpace[1] - 1) != 0) {
            return true;
        } else if ((direction == 'D' || direction == 'd') && coordinatesOfSpace[1] + 1 < size[1]
                && cell(coordinatesOfSpace[0], coordinatesOfSpace[1] + 1) != 0) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * Determine if board solved or not
     * 
     * @return Whether board solved or not
     */
    public boolean isSolved() {
        int index = 1;
        for (int i = 0; i < size[1]; ++i) {
            for (int j = 0; j < size[0]; ++j) {
                int a = cell(j, i);
                if (index == a) {
                } else if (a == 0) {
                    index--;
                } else {
                    if (i != size[1] - 1 || j != size[0] - 1) {
                        return false;
                    }
                }
                index++;
            }
        }
        return true;
    }

    /**
     * Determine if other board equals to this board
     * 
     * @param other Other AbstractBoard
     * @return Whether other board equals to this board
     */
    public boolean equals(NPuzzle other) {
        if (this.size[0] == other.size[0] && this.size[1] == other.size[1]) {
            for (int i = 0; i < size[1]; ++i) {
                for (int j = 0; j < size[0]; ++j) {
                    if (this.cell(j, i) != other.cell(j, i)) {
                        return false;
                    }
                }
            }
            return true;
        }
        return false;
    }

    /**
     * Determine if difference of two boards movement is more than two or not
     * 
     * @param other Other AbstractBoard
     * @return If difference of two boards movement is more than two or not
     */
    protected boolean isDiffTwo(NPuzzle other) {
        int counter = 0;
        if (this.size[0] == other.size[0] && this.size[1] == other.size[1]) {
            for (int i = 0; i < size[1]; ++i) {
                for (int j = 0; j < size[0]; ++j) {
                    if (this.cell(j, i) != other.cell(j, i)) {
                        counter++;
                    }
                }
            }
            if (counter == 2) {
                return true;
            } else {
                return false;
            }
        }
        return false;
    }
/**
 * Assign result to which subclass call that function's array
 * @param i X index of array
 * @param j Y index of array
 * @param result Value that will be assigned
 */
    public void assign(int i, int j, int result) {
        arr[i][j] = result;
    }

    
}