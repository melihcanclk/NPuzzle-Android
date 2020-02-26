package com.melihcanclk;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.res.AssetFileDescriptor;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.view.GestureDetector;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import org.tensorflow.lite.Interpreter;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.RandomAccess;

import static android.widget.Toast.LENGTH_SHORT;


public class MainActivity extends AppCompatActivity implements GestureDetector.OnGestureListener {

    private static int NUMBER_OF_SHUFFLE;
    private static int columns;
    private static int rows;

    private static String COLUMN_NAME = "com.example.npuzzle/com.melihcanclk.MainActivity - column";
    private static String ROW_NAME = "com.melihcanclk - row";

    public static final int SWIPE_THRESHOLD = 10;
    public static final int SWIPE_VELOCITY_THRESHOLD = 5;

    char [] moves ;

    /**
     * Represents last move that a board did
     */
    protected char _lastMove = 'S';
    /**
     * Represents number of moves that user did so far
     */
    protected static int _numberOfMoves = 0;

    TableLayout table;
    TextView textViewCounter;
    TextView[][] textView;
    Button resetButton;
    Button hintButton;
    Interpreter interpreter;

    private int[] coordinatesOfSpace = new int[2];

    GestureDetector gestureDetector;

    public static Intent makeIntent(Context context,int column, int row) {
        Intent intent = new Intent(context, MainActivity.class);

        intent.putExtra(COLUMN_NAME, column);
        intent.putExtra(ROW_NAME, row);

        return intent;
    }

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        String temp = "LRUD";
        moves = temp.toCharArray();
        setContentView(R.layout.activity_main);

        try {
            interpreter = new Interpreter(loadModelFile("3","3"));
        } catch (IOException e) {
            e.printStackTrace();
        }

        extractDataFromIntent();
        gestureDetector = new GestureDetector(this);

        textViewCounter = (TextView) findViewById(R.id.showNumberOfMoves);
        textViewCounter.setText(String.valueOf(_numberOfMoves));

        resetButton = (Button) findViewById(R.id.resetButton);
        resetButton.setOnClickListener(new View.OnClickListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onClick(View v) {
                reset();
                shuffle(NUMBER_OF_SHUFFLE);

                while(!isSolved()){

                }
            }
        });

        hintButton = (Button) findViewById(R.id.hintButton);
        hintButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                float [] arr = new  float[4];
                List<Integer> convertedTextView = mode(textView);
                arr = doInferance(convertedTextView);
                move(moves[findClosestToOne(arr)]);
                if(isSolved()){

                    Toast.makeText(getApplicationContext(), "Puzzle Solved!!!", LENGTH_SHORT).show();
                    finish();
                }
            }
        });

        createButtons();
        shuffle(NUMBER_OF_SHUFFLE);
    }

    private int findClosestToOne(float[] arr) {
        int myNumber = 1;
        float distance = Math.abs(arr[0] - myNumber);
        int idx = 0;
        for(int c = 1; c < arr.length; c++){
            float cdistance = Math.abs(arr[c] - myNumber);
            if(cdistance < distance){
                idx = c;
                distance = cdistance;
            }
        }
       return idx;

    }

    private float [] doInferance(List<Integer> convertedTextView) {
        float [][][] array= new float[1][1][81];
        for (int i = 0; i< convertedTextView.size();i++)
            array[0][0][i] = convertedTextView.get(i);

        float [][] output = new float[1][4];
        interpreter.run(array,output);

        return output[0];
    }


    public static List<Integer> mode(TextView [][] arr) {
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < 9; i++) {
            // tiny change 1: proper dimensions
            for (int j = 0; j <9; j++) {
                if(i < rows && j < columns){
                    if(arr[i][j].getText().toString().equals(" ")){
                        list.add(-1);
                    }else {
                        int number = Integer.parseInt(arr[i][j].getText().toString());
                        list.add(number);
                    }

                }else{
                    list.add(0);
                }

            }
        }
        return list;
    }


    public boolean isSolved() {
        int index = 1;
        int a = 0;
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < columns; ++j) {
                if(textView[i][j].getText().toString().equals(" ")){
                    a = -1;
                }else{
                    a = Integer.parseInt(textView[i][j].getText().toString());
                }
                if (index == a) {
                }else {
                    if (i != rows - 1 || j != columns - 1) {
                        return false;
                    }
                }
                index++;
            }
        }
        return true;
    }
    private void shuffle(int numberOfShuffle){
        Random random = new Random();
        for (int i = 0; i< numberOfShuffle;++i){
            int randomMove = random.nextInt(moves.length);
            while(!isValid(moves[randomMove]))
                randomMove = random.nextInt(moves.length);
            move(moves[randomMove]);
        }
        _numberOfMoves = 0;
    }

    private void reset(){
        _numberOfMoves = 0;
        textViewCounter.setText(String.valueOf(_numberOfMoves));
        Integer counter = 1;
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < columns; ++j) {
                textView[i][j].setText(counter.toString());
                if (i == rows - 1 && j == columns - 1) {
                    textView[i][j].setText(" ");
                    coordinatesOfSpace[1] = i;
                    coordinatesOfSpace[0] = j;
                }
                ++counter;
            }
        }
    }

    private void extractDataFromIntent() {

        /*Get data from Main_Menu that got from user to create rows and columns*/
        Intent intent = getIntent();
        columns = intent.getIntExtra(COLUMN_NAME, 3);
        rows = intent.getIntExtra(ROW_NAME,3);
        textView = new TextView[rows][columns];
        Random random = new Random();
        NUMBER_OF_SHUFFLE = random.nextInt(rows * columns);
        while (NUMBER_OF_SHUFFLE <= 3){
            NUMBER_OF_SHUFFLE = random.nextInt();
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    @SuppressLint("SetTextI18n")
    private void createButtons() {
        table = (TableLayout) findViewById(R.id.tableForButtons);

        Integer counter = 1;
        for (int i = 0; i < rows; ++i) {
            TableRow tableRow = new TableRow(this);
            tableRow.setLayoutParams(new TableLayout.LayoutParams(
                    TableLayout.LayoutParams.MATCH_PARENT,
                    TableLayout.LayoutParams.MATCH_PARENT,
                    1.0f));
            table.addView(tableRow);
            for (int j = 0; j < columns; ++j) {
                final int FINAL_I = i;
                final int FINAL_J = j;
                TextView tempTextView = new TextView(this);
                tempTextView.setLayoutParams(new TableRow.LayoutParams(
                        TableRow.LayoutParams.MATCH_PARENT,
                        TableRow.LayoutParams.MATCH_PARENT,
                        1.0f));
                tempTextView.setText(counter.toString());
                tempTextView.setGravity(Gravity.CENTER);
                GradientDrawable gd = new GradientDrawable();
                gd.setStroke(2, 0xFF000000);
                tempTextView.setBackground(gd);
                tempTextView.setBackgroundResource(R.color.mutedpink);
               /* tempTextView.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        showMessage(FINAL_J, FINAL_I);
                    }
                });*/
                tableRow.addView(tempTextView);
                if (i == rows - 1 && j == columns - 1) {
                    tempTextView.setText(" ");
                    coordinatesOfSpace[1] = i;
                    coordinatesOfSpace[0] = j;
                }
                textView[i][j] = tempTextView;
                ++counter;
            }
        }


    }

    /**
     * Abstract move method that will be used by subclasses
     *
     * @param direction Direction of movement
     */
    public void move(final char direction) {
        int x, y;
        x = coordinatesOfSpace[0];
        y = coordinatesOfSpace[1];
        if (direction == 'L' || direction == 'l') {
            if (isValid('L')) {
                String temp = textView[y][x - 1].getText().toString();
                textView[y][x - 1].setText(textView[y][x].getText().toString());
                textView[y][x].setText(temp);
                coordinatesOfSpace[0]--;
            }
        } else if (direction == 'R' || direction == 'r') {
            if (isValid('R')) {
                String temp = textView[y][x + 1].getText().toString();
                textView[y][x + 1].setText(textView[y][x].getText().toString());
                textView[y][x].setText(temp);
                coordinatesOfSpace[0]++;
            }
        } else if (direction == 'U' || direction == 'u') {
            if (isValid('U')) {
                String temp = textView[y - 1][x].getText().toString();
                textView[y - 1][x].setText(textView[y][x].getText().toString());
                textView[y][x].setText(temp);
                coordinatesOfSpace[1]--;
            }
        } else if (direction == 'D' || direction == 'd') {
            if (isValid('D')) {
                String temp = textView[y + 1][x].getText().toString();
                textView[y + 1][x].setText(textView[y][x].getText().toString());
                textView[y][x].setText(temp);
                coordinatesOfSpace[1]++;
            }
        }
        if (isValid(direction)) {
            _lastMove = direction;
            System.out.println("Moved to " + direction);
            ++_numberOfMoves;
            textViewCounter.setText(String.valueOf(_numberOfMoves));

        }
    }

    protected boolean isValid(final char direction) {

        if ((direction == 'L' || direction == 'l') && coordinatesOfSpace[0] - 1 >= 0) {
            return true;
            // TODO : size 0 and size 1 add
        } else if ((direction == 'R' || direction == 'r') && coordinatesOfSpace[0] + 1 < columns) {
            return true;
        } else if ((direction == 'U' || direction == 'u') && coordinatesOfSpace[1] - 1 >= 0) {
            return true;
        } else if ((direction == 'D' || direction == 'd') && coordinatesOfSpace[1] + 1 < rows) {
            return true;
        } else {
            return false;
        }
    }

    private void showMessage(int x, int y) {
        Toast.makeText(MainActivity.this, " " + x + "," + y,
                LENGTH_SHORT).show();

    }

    @Override
    public boolean onDown(MotionEvent e) {
        return false;
    }

    @Override
    public void onShowPress(MotionEvent e) {

    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        return false;
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {
        return false;
    }


    @Override
    public void onLongPress(MotionEvent e) {

    }

//onFling Function for being able to imageview swipe
    @Override
    public boolean onFling(MotionEvent downEvent, MotionEvent moveEvent, float velocityX, float velocityY) {
        boolean result = false;
        float diffY = moveEvent.getY() - downEvent.getY();
        float diffX = moveEvent.getX() - downEvent.getX();
        // which was greater?  movement across Y or X?
        if (Math.abs(diffX) > Math.abs(diffY)) {
            // right or left swipe
            if (Math.abs(diffX) > SWIPE_THRESHOLD && Math.abs(velocityX) > SWIPE_VELOCITY_THRESHOLD) {
                if (diffX > 0) {
                    onSwipeLeft();
                } else {
                    onSwipeRight();

                }
                result = true;
            }
        } else {
            // up or down swipe
            if (Math.abs(diffY) > SWIPE_THRESHOLD && Math.abs(velocityY) > SWIPE_VELOCITY_THRESHOLD) {
                if (diffY > 0) {
                    onSwipeTop();
                } else {
                    onSwipeBottom();
                }
                result = true;
            }
        }
        if(isSolved()){
            Toast.makeText(this, "Puzzle Solved!!!", LENGTH_SHORT).show();
            finish();
        }
        return result;
    }

    private void onSwipeTop() {
        Toast.makeText(this, "Swipe Top", LENGTH_SHORT).show();
        move('u');
    }

    private void onSwipeBottom() {
        Toast.makeText(this, "Swipe Bottom", LENGTH_SHORT).show();
        move('d');
    }

    private void onSwipeLeft() {
        Toast.makeText(this, "Swipe Left", LENGTH_SHORT).show();
        move('l');
    }

    private void onSwipeRight() {
        Toast.makeText(this, "Swipe Right", LENGTH_SHORT).show();
        move('r');
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        gestureDetector.onTouchEvent(event);

        return super.onTouchEvent(event);
    }

    private MappedByteBuffer loadModelFile(String size_x, String size_y) throws IOException{
        String filename = "model_" + size_x.toString() + "x" + size_y.toString() + ".tflite";
        AssetFileDescriptor fileDescriptor = this.getAssets().openFd(filename);
        FileInputStream fileInputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = fileInputStream.getChannel();
        long startOffSet = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffSet,declaredLength);

    }

}

