package com.example.npuzzle;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
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


public class MainActivity extends AppCompatActivity implements GestureDetector.OnGestureListener {

    private static final int NUM_ROWS = 7;
    private static final int NUM_COLUMNS = 7;

    public static final int SWIPE_THRESHOLD = 100;
    public static final int SWIPE_VELOCITY_THRESHOLD = 100;

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
    TextView[][] textView = new TextView[NUM_ROWS][NUM_COLUMNS];

    private int[] coordinatesOfSpace = new int[2];

    GestureDetector gestureDetector;

    public static Intent makeIntent(Context context) {
        return new Intent(context, MainActivity.class);
    }

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        gestureDetector = new GestureDetector(this);

        textViewCounter = (TextView) findViewById(R.id.showNumberOfMoves);
        textViewCounter.setText(String.valueOf(_numberOfMoves));
        createButtons();
    }

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    @SuppressLint("SetTextI18n")
    private void createButtons() {
        table = (TableLayout) findViewById(R.id.tableForButtons);

        Integer counter = 1;
        for (int i = 0; i < NUM_ROWS; ++i) {
            TableRow tableRow = new TableRow(this);
            tableRow.setLayoutParams(new TableLayout.LayoutParams(
                    TableLayout.LayoutParams.MATCH_PARENT,
                    TableLayout.LayoutParams.MATCH_PARENT,
                    1.0f));
            table.addView(tableRow);
            for (int j = 0; j < NUM_COLUMNS; ++j) {
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
               /* tempTextView.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        showMessage(FINAL_J, FINAL_I);
                    }
                });*/
                tableRow.addView(tempTextView);
                if (i == NUM_ROWS - 1 && j == NUM_COLUMNS - 1) {
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
            _numberOfMoves++;
            System.out.println("Moved to " + direction);
        }
    }

    protected boolean isValid(final char direction) {

        if ((direction == 'L' || direction == 'l') && coordinatesOfSpace[0] - 1 >= 0) {
            return true;
            // TODO : size 0 and size 1 add
        } else if ((direction == 'R' || direction == 'r') && coordinatesOfSpace[0] + 1 < NUM_ROWS) {
            return true;
        } else if ((direction == 'U' || direction == 'u') && coordinatesOfSpace[1] - 1 >= 0) {
            return true;
        } else if ((direction == 'D' || direction == 'd') && coordinatesOfSpace[1] + 1 < NUM_COLUMNS) {
            return true;
        } else {
            return false;
        }
    }

    private void showMessage(int x, int y) {
        Toast.makeText(MainActivity.this, " " + x + "," + y,
                Toast.LENGTH_SHORT).show();

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
                    onSwipeRight();
                } else {
                    onSwipeLeft();
                }
                result = true;
            }
        } else {
            // up or down swipe
            if (Math.abs(diffY) > SWIPE_THRESHOLD && Math.abs(velocityY) > SWIPE_VELOCITY_THRESHOLD) {
                if (diffY > 0) {
                    onSwipeBottom();
                } else {
                    onSwipeTop();
                }
                result = true;
            }
        }
        if(result){
            textViewCounter.setText(String.valueOf(_numberOfMoves));
        }
        return result;
    }

    private void onSwipeTop() {
        Toast.makeText(this, "Swipe Top", Toast.LENGTH_SHORT).show();
        move('u');
    }

    private void onSwipeBottom() {
        Toast.makeText(this, "Swipe Bottom", Toast.LENGTH_SHORT).show();
        move('d');
    }

    private void onSwipeLeft() {
        Toast.makeText(this, "Swipe Left", Toast.LENGTH_SHORT).show();
        move('l');
    }

    private void onSwipeRight() {
        Toast.makeText(this, "Swipe Right", Toast.LENGTH_SHORT).show();
        move('r');
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        gestureDetector.onTouchEvent(event);

        return super.onTouchEvent(event);
    }
}

