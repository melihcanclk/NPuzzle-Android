package com.example.npuzzle;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity {

    private static final int NUM_ROWS = 7;
    private static final int NUM_COLUMNS = 7;

    TableLayout table;
    Button[][] buttons = new Button[NUM_ROWS][NUM_COLUMNS];

    public static Intent makeIntent(Context context) {
        return new Intent(context,MainActivity.class);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        createButtons();
    }

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
                Button button = new Button(this);
                button.setLayoutParams(new TableRow.LayoutParams(
                        TableRow.LayoutParams.MATCH_PARENT,
                        TableRow.LayoutParams.MATCH_PARENT,
                        1.0f));
                button.setText(counter.toString());
                button.setPadding(0, 0, 0, 0);
                button.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        showMessage(FINAL_J, FINAL_I);
                    }
                });
                tableRow.addView(button);
                if (i == NUM_ROWS - 1 && j == NUM_COLUMNS - 1) {
                    button.setText(" ");
                }
                buttons[i][j] = button;
                ++counter;
            }
        }

    }

    private void showMessage(int x, int y) {
        Toast.makeText(MainActivity.this, " " + x + "," + y,
                Toast.LENGTH_SHORT).show();

    }

}
